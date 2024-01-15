from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import RegistrationSerializer,UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import UserAccount
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    
# class UserRegistrationView(FormView):
#     template_name = 'accounts/user_registration.html'
#     form_class = UserRegistrationForm
#     serializer_class = RegistrationSerializer
    
#     def form_valid(self, form):
#         user = form.save()
#         messages.success(self.request, "After registration, Login successfully")
#         return redirect('login')
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             print("Registration", user)
#             token = default_token_generator.make_token(user)
#             print("token", token)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             print("uid", uid)
#             confirm_link = f'http://127.0.0.1:8000/accounts/active/{uid}/{token}'
#             print("confirm_link", confirm_link)
#             email_subject = "Confirm Your Email"
#             email_body = render_to_string('accounts/confirm_email.html',{'confirm_link': confirm_link})
#             send_email = EmailMultiAlternatives(email_subject, '',to=[user.email])
#             send_email.attach_alternative(email_body, "text/html")
#             send_email.send()
#             return Response("Check your email address for confirmation")
#         return Response(serializer.errors)

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login') 

    def form_valid(self, form):
        user = form.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f'http://127.0.0.1:8000/accounts/activate/{uid}/{token}'
        email_subject = "Confirm Your Email"
        email_body = render_to_string('accounts/confirm_email.html', {'confirm_link': confirm_link})
        send_email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        send_email.attach_alternative(email_body, "text/html")
        send_email.send()

        messages.success(self.request, "Check your email for confirmation.")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

def activate(request, uid64, token):
    print("uid64:", uid64)
    print("token:", token)
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        User = get_user_model()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is now activated. You can log in.')
        return redirect('login')
    messages.error(request, 'Invalid activation link. Please try again or contact support.')
    return redirect('register') 

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        messages.success(self.request, "Login successfully")
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        messages.success(self.request, "Logout successfully")
        return reverse_lazy('home')

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'

class UserRegistrationApiView(APIView):
    serializer_class = RegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print("Registration", user)
            token = default_token_generator.make_token(user)
            print("token", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid", uid)
            confirm_link = f'http://127.0.0.1:8000/accounts/active/{uid}/{token}'
            print("confirm_link", confirm_link)
            email_subject = "Confirm Your Email"
            email_body = render_to_string('accounts/confirm_email.html',{'confirm_link': confirm_link})
            send_email = EmailMultiAlternatives(email_subject, '',to=[user.email])
            send_email.attach_alternative(email_body, "text/html")
            send_email.send()
            return Response("Check your email address for confirmation")
        return Response(serializer.errors)

# def activate(request, uid64, token):
#     try:
#         uid = urlsafe_base64_decode(uid64).decode()
#         user = User._default_manager.get(pk=uid)
#     except(User.DoesNotExist):
#         user = None
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return redirect('login')
#     else:
#       return redirect('register')  
        # return HttpResponse('Activation link is invalid or expired.')  


class UserLoginApiView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user:
                token, created = Token.objects.get_or_create(user=user)
                print(token)
                print(created)
                login(request,user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': 'Invalid username or password'})
        return Response(serializer.errors)
                
class UserLogoutApiView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')