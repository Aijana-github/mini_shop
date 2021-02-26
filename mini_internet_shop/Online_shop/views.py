from email.headerregistry import Group

from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from .forms import RegistrationForm, UserProfileForm
from .models import Products
from .tokens import account_activation_token


def registration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
             user = form.save(commit=False)
             user.is_active = False
             user.save()
             current_site = get_current_site (request)
             mail_subject = 'Активируйте свою учетную запись.'
             message = render_to_string('accounts/acc_active_email.html', {
                 'user': user,
                 'domain': current_site.domain,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user),
             })
             to_email = form.cleaned_data.get('email')
             email = EmailMessage(
                 mail_subject, message, to=[to_email]
             )
             email.send()
             return HttpResponse('Подтвердите свой адрес электронной почты для завершения регистрации')
        else:
            form = RegistrationForm()
    return render(request, 'accounts/user_create.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Спасибо за подтверждение по электронной почте. Теперь вы можете войти в свою учетную запись !')
    else:
        return HttpResponse('Ссылка для активации недействительна!')



def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect()
    context = {}
    return render(request,'accounts/login.html',context)

@login_required(login_url=['login'])
def CreateUser(request):
    user = request.user.userprofile
    form = UserProfileForm(instance= user)
    if request.method =='POST':
        form = UserProfileForm(request.POST,request.FILES,instance=user)
        form.save()
    context = {'form':form}
    return render(request,'accounts/accounts.html',context)



def productList(request):
    products = Products.objects.all()

    context = {'products': products}
    return render (request, 'accounts/products.html', context)