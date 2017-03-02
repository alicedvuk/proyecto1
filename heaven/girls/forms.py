from django import forms
from captcha.fields import ReCaptchaField

class RecruitmentForm(forms.Form):
	contact_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control '}), required=True)
	phone = forms.CharField( widget=forms.TextInput(attrs={'class' : 'form-control '}),max_length=40, required=True)
	contact_email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'form-control '}),required=True)
	postcode = forms.CharField( widget=forms.TextInput(attrs={'class' : 'form-control '}),max_length=40, required=True)
	flat = forms.CharField( widget=forms.TextInput(attrs={'class' : 'form-control '}),max_length=40, required=True)
	address = forms.CharField( widget=forms.TextInput(attrs={'class' : 'form-control '}),max_length=140, required=True)
	tube_station = forms.CharField( widget=forms.TextInput(attrs={'class' : 'form-control '}),max_length=40, required=False)
	captcha = ReCaptchaField()

	content = forms.CharField(
		required=True,
		widget=forms.Textarea,

	)

    # the new bit we're adding
	def __init__(self, *args, **kwargs):
		super(RecruitmentForm, self).__init__(*args, **kwargs)
		self.fields['contact_name'].label = "Your name:"
		self.fields['phone'].label = "Your phone number:"
		self.fields['contact_email'].label = "Your email:"
		self.fields['postcode'].label = "Your postcode:"
		self.fields['flat'].label = "Your flat number:"
		self.fields['address'].label = "Your address:"
		self.fields['tube_station'].label = "Your tube station:"
		self.fields['content'].label = "Additional information, talk about you"