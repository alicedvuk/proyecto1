# -*- encoding: utf8 -*-
import os
import re
import random
import string
import zipfile
import json

import mimetypes
import xml.etree.ElementTree as ET
import requests

from configparser import ConfigParser
from uuid import uuid5, UUID

from urllib.parse import quote, urljoin, urlencode
from urllib.request import urlopen
from collections import OrderedDict
from email.mime.image import MIMEImage
from PIL.ImageColor import colormap
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import get_random_string
from django.utils.encoding import iri_to_uri
from filelock import FileLock


def find_geocode(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    url += quote(address.encode('utf8'))

    try:
        result = json.load(urlopen(url))
    except Exception:
        return None

    if result['status'] != 'OK':
        return None

    try:
        geo = result['results'][0]['geometry']['location']
        return float(geo['lat']), float(geo['lng'])
    except (KeyError, ValueError):
        return None


def geo_query_address(street=None, zip=None, city=None, state=None, country=None):
    """
               result = find_geocode(geo_query_address(street=partner.street,
                                                zip=partner.zip,
                                                city=partner.city,
                                                state=partner.state_id.name,
                                                country=partner.country_id.name))
    :param street:
    :param zip:
    :param city:
    :param state:
    :param country:
    :return:
    """
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        # put country qualifier in front, otherwise GMap gives wrong results,
        # e.g. 'Congo, Democratic Republic of the' => 'Democratic Republic of the Congo'
        country = '{1} {0}'.format(*country.split(',', 1))

    return ', '.join(filter(None, [street,
                                   ("%s %s" % (zip or '', city or '')).strip(),
                                   state,
                                   country]))


def zip_dir(path, stream, include_dir=True, fnct_sort=None):  # TODO add ignore list
    """
    : param fnct_sort : Function to be passed to "key" parameter of built-in
                        python sorted() to provide flexibility of sorting files
                        inside ZIP archive according to specific requirements.
    """
    path = os.path.normpath(path)
    len_prefix = len(os.path.dirname(path)) if include_dir else len(path)

    if len_prefix:
        len_prefix += 1

    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for dirpath, dirnames, filenames in os.walk(path):
            filenames = sorted(filenames, key=fnct_sort)
            for fname in filenames:
                bname, ext = os.path.splitext(fname)
                ext = ext or bname
                if ext not in ['.pyc', '.pyo', '.swp', '.DS_Store']:
                    path = os.path.normpath(os.path.join(dirpath, fname))
                    if os.path.isfile(path):
                        zipf.write(path, path[len_prefix:])


def preflight(content):
    from django.conf import settings

    content = '<body>{}</body>'.format(content)

    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        pass
    else:
        for child in root.iter():
            if child.tag in ['p', 'h1', 'h2', 'h3', 'span', 'strong', 'em', 'td', 'th', 'li']:
                child.set('style', ';'.join([
                    'font-family: Helvetica, Arial, sans-serif  !important',
                    'font-size: 16px  !important',
                    'color: #222'
                ]))
            elif child.tag in ['a']:
                child.set('style', ';'.join([
                    'font-family: Helvetica, Arial, sans-serif !important',
                    'font-size: 16px !important',
                    'color: #2DA0E3',
                    'text-decoration: none',
                ]))
            elif child.tag in ['pre']:
                child.set('style', ';'.join([
                    'font-family: Consolas !important',
                    'font-size: 14px !important',
                    'padding: 20px',
                    'background-color: #efefef',
                    'color: #222'
                ]))
            elif child.tag in ['img']:
                child.set('border', 0)
                child.set('style', ';'.join([
                    'display: block',
                    'outline: none',
                    '-ms-interpolation-mode: bicubic'
                ]))
            elif child.tag in ['body']:
                child.set('style', ';'.join([
                    'margin: 0 !important',
                    'padding: 10px !important',
                    '-webkit-text-size-adjust: 100%',
                    '-ms-text-size-adjust: 100%',
                ]))
        content = ET.tostring(root).decode('utf-8')

    content = re.sub(settings.MEDIA_URL, build_absolute_uri(settings.MEDIA_URL), content)

    return content


def get_headers(request):
    wsgi_env = list(sorted(request.META.items()))
    return OrderedDict(
        (k.replace('_', ' '), v) for (k, v) in wsgi_env if k.startswith('HTTP_') or k.startswith('REMOTE_'))


def render_from_string(content, context):
    from django.template import Context, Template

    context = Context(context)
    tpl = Template(content)
    return tpl.render(context)


def send_mail(subject, content, from_email, recipient_list,
              extra_context=None, attachments=None):
    from django.core.mail import EmailMultiAlternatives
    from django.template import Context, Template

    context = dict()
    context.setdefault('subject', subject)
    context.setdefault('recipient_list', recipient_list)

    if extra_context:
        context.update(extra_context)

    context = Context(context)

    tpl_content = Template(content)
    content = tpl_content.render(context)

    tpl_subject = Template(subject)
    subject = tpl_subject.render(context).strip()

    html_message = preflight(content)

    msg = EmailMultiAlternatives(subject, html_message, from_email, recipient_list)
    msg.content_subtype = "html"

    if attachments:
        for _n, filename in enumerate(attachments, 1):
            if any(filename.endswith(ext) for ext in ['.png', '.jpg', '.gif']):
                with open(filename, 'rb') as f:
                    attachment = MIMEImage(f.read())
                    mimetype, _ = mimetypes.guess_type(filename)
                    attachment.add_header('Content-Disposition', 'inline', name=filename)
                    attachment.add_header('Content-Type', mimetype, name=filename)
                    attachment.add_header('Content-ID', '<img{0}>' % _n)
                    msg.attach(attachment)
            else:
                msg.attach_file(filename)

    msg.send()


def slackpost(channel, username, text, attachments=None, icon_emoji=':baby::skin-tone-3:'):
    from vv.configuration.models import SiteConfiguration

    config = SiteConfiguration.get_solo()
    webhook = config.slack_webhook

    if webhook:
        data = {
            'channel': channel,
            'username': username,
            'text': text,
            'icon_emoji': icon_emoji,
        }

        if attachments:
            data['attachments'] = []

            for key, value in attachments.items():
                data['attachments'].append({'title': key, 'value': '%s' % value, 'short': True})

        requests.post(webhook, json.dumps(data))


class FilePermissionError(Exception):
    """The key file permissions are insecure."""
    pass


VALID_KEY_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits


def load_environment_file(envfile, key_length=64):
    config = None
    lock = FileLock(os.path.abspath(envfile) + ".lock")

    with lock:
        if not os.path.exists(envfile):
            # Create empty file if it doesn't exists

            old_umask = os.umask(0o177)  # Use '0600' file permissions
            config = ConfigParser()
            config.add_section('django')
            config['django']['secret_key'] = get_random_string(key_length, VALID_KEY_CHARS)

            with open(envfile, 'w') as configfile:
                config.write(configfile)
            os.umask(old_umask)

        if (os.stat(envfile).st_mode & 0o777) != 0o600:
            raise FilePermissionError("Insecure environment file permissions for %s!" % envfile)

        if not config:
            config = ConfigParser()
            config.read_file(open(envfile))

        if not config.has_section('django'):
            raise ImproperlyConfigured('Missing `django` section in the environment file.')

        if not config.get('django', 'secret_key', fallback=None):
            raise ImproperlyConfigured('Missing `secret_key` in django section in the environment file.')

        # Register all keys as environment variables
        for key, value in config.items('django'):
            ENVNAME = 'DJANGO_%s' % key.upper()
            if ENVNAME not in os.environ:  # Don't replace existing defined variables
                os.environ[ENVNAME] = value


FINGERPRINT_PARTS = [
    'HTTP_ACCEPT_ENCODING',
    'HTTP_ACCEPT_LANGUAGE',
    'HTTP_USER_AGENT',
    'HTTP_X_FORWARDED_FOR',
    'REMOTE_ADDR']

UUID_NAMESPACE = UUID('611d2fd8-bc08-11e5-845d-60a44cb01ca6')


def get_client_id(request):
    parts = [request.META.get(key, '') for key in FINGERPRINT_PARTS]
    return uuid5(UUID_NAMESPACE, '_'.join(parts))


def get_random_color():
    return random.sample(colormap.keys(), 1).pop()


absolute_http_url_re = re.compile(r'^https?://', re.I)


def build_absolute_uri(location, dict = None, is_secure=False):
    from django.contrib.sites.models import Site

    site = Site.objects.get_current()
    host = site.domain
    params = '?%s' % urlencode(params) if params else ''

    if not absolute_http_url_re.match(location):
        current_uri = '%s://%s' % ('https' if is_secure else 'http', host)
        location = urljoin(current_uri, location)

    return iri_to_uri(location) + params


def get_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip:
        ip = ip.split(', ')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip
