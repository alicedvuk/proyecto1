from django.dispatch import receiver
from django.conf import settings
#from accounts.signals import user_signup


#@receiver(user_signup, dispatch_uid="send_welcome_email")
#def send_welcome_email(sender, **kwargs):
#    user = kwargs['user']

#    from vv.configuration.models import SiteConfiguration

#    config = SiteConfiguration.get_solo()

#    user.send_mail(
#        subject=config.account_register_welcome_subject,
#        content=config.account_register_welcome_email,
#        from_email=settings.DEFAULT_FROM_EMAIL)
