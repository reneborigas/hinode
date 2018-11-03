from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from .forms import contactForm
# Create your views here.
def contact(request):
    title='Contacts'
    form=contactForm(request.POST or None)  
    context = {'title':title,'form': form,}

    if form.is_valid():
        name=form.cleaned_data['name']
        comment=form.cleaned_data['comment']
        subject='Email from JLPT Review Program'
        message='%s %s' %(comment, name)
        emailFrom=form.cleaned_data['email']
        emailTo=[settings.EMAIL_HOST_USER]
        send_mail(subject,message,emailFrom,emailTo,fail_silently=True,)
        title = "Thanks"
        confirm_message = "Thanks for the message. We will get right back to you."
        context = {'title':title,'confirm_message':confirm_message}

    # context=locals()
    template='contact.html'
    return render(request,template,context) 