from django.shortcuts import render, redirect, render_to_response
from django.template.loader import get_template
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template import Context, RequestContext

from .forms import RecruitmentForm



# our view
def RecruitmentView(request):
	form_class = RecruitmentForm
    # new logic!
	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			try:
				contact_name = request.POST.get('contact_name', '')
				contact_email = request.POST.get('contact_email', '')
				phone = request.POST.get('phone', '')
				postcode = request.POST.get('postcode', '')
				flat = request.POST.get('flat', '')
				address = request.POST.get('address', '')
				tube_station = request.POST.get('tube_station', '')
				form_content = request.POST.get('content', '')

				# Email the profile with the 
				# contact information

				template = get_template('pages/recruitment.txt')
				context = Context({
					'contact_name': contact_name,
					'contact_email': contact_email,
					'phone': phone,
					'postcode': postcode,
					'flat': flat,
					'address': address,
					'tube_station': tube_station,
					'form_content': form_content,
				})

				content = template.render(context)
				mail = EmailMultiAlternatives(
					subject = "New Job Application On Website",
					body = content,
					from_email = " Recruitment <123.aqua.uk@gmail.com>",
					to = ["londoneragency@gmail.com"],
					headers = {'Reply-To': contact_email }
				)
				#mail.attach(pic.name, pic.read(), pic.content_type)
				#send_mail('New Girl For Recritment', content , '123.aqua.uk@gmail.com', ['londoneragency@gmail.com'], fail_silently=False)
				#mail.attach_alternative("<p>This is a simple HTML email body</p>", "text/html")
				mail.send()
				return redirect('/')
			except:
				pass
	else:
		form =RecruitmentForm()


	return render_to_response( 'pages/recruitment.html', 
		{'form': form},
		context_instance=RequestContext(request))






