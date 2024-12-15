from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .forms import SignupForm, LoginForm, ForumForm
from .models import OTP, Forum
import random
import cloudinary.uploader

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'exists': User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)

def generate_otp():
    return str(random.randint(10000, 99999))

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if 'get_otp' in request.POST:
            if User.objects.filter(email=email).exists():
                otp_code = generate_otp()
                otp, created = OTP.objects.update_or_create(
                    email=email,
                    defaults={'code': otp_code, 'created_at': timezone.now()}
                )
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp_code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return render(request, 'forgot_password.html', {'otp_sent': True, 'email': email})
            else:
                return render(request, 'forgot_password.html', {'error': 'It seems like you are not a user here before.', 'email': email})
        elif 'validate_otp' in request.POST:
            otp = request.POST.get('otp')
            try:
                otp_record = OTP.objects.get(email=email)
                if otp_record.code == otp:
                    if otp_record.is_expired():
                        return render(request, 'forgot_password.html', {'error': 'OTP has expired', 'otp_sent': True, 'email': email})
                    else:
                        return render(request, 'forgot_password.html', {'otp_validated': True, 'email': email})
                else:
                    return render(request, 'forgot_password.html', {'error': 'Invalid OTP', 'otp_sent': True, 'email': email})
            except OTP.DoesNotExist:
                return render(request, 'forgot_password.html', {'error': 'Invalid OTP', 'otp_sent': True, 'email': email})
        elif 'save_changes' in request.POST:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return redirect('login')
            else:
                return render(request, 'forgot_password.html', {'error': 'Passwords do not match', 'otp_validated': True, 'email': email})
    return render(request, 'forgot_password.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if 'get_otp' in request.POST:
            if form.is_valid():
                email = form.cleaned_data['email']
                otp_code = generate_otp()

                # Update or create OTP for the email
                otp, created = OTP.objects.update_or_create(
                    email=email,
                    defaults={'code': otp_code, 'created_at': timezone.now()}
                )
                
                # Send the OTP email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp_code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return render(request, 'signup.html', {'form': form, 'otp_sent': True})
            else:
                return render(request, 'signup.html', {'form': form})
        elif 'signup' in request.POST:
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                otp = form.cleaned_data['otp']

                try:
                    otp_record = OTP.objects.get(email=email)
                    if otp_record.code == otp:
                        if otp_record.is_expired():
                            return render(request, 'signup.html', {
                                'form': form,
                                'error': 'OTP has expired',
                                'otp_sent': True
                            })
                        else:
                            user = User.objects.create_user(
                                username=email,
                                email=email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name
                            )
                            user.save()
                            otp_record.delete()  # Delete OTP after successful signup
                            send_mail(
                                'Welcome to Our Site',
                                'Thank you for signing up!\n\nBest regards,\nNZ Sohit',
                                settings.DEFAULT_FROM_EMAIL,
                                [email],
                                fail_silently=False,
                            )
                            auth_login(request, user)
                            return redirect('index')
                    else:
                        return render(request, 'signup.html', {'form': form, 'error': 'Invalid OTP', 'otp_sent': True})
                except OTP.DoesNotExist:
                    return render(request, 'signup.html', {'form': form, 'error': 'Invalid OTP', 'otp_sent': True})
            else:
                return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

def resend_otp(request):
    email = request.GET.get('email', None)
    if email:
        # Clean up existing OTPs for the email
        OTP.objects.filter(email=email).delete()

        # Generate a new OTP
        otp_code = generate_otp()
        OTP.objects.create(email=email, code=otp_code)

        # Send the OTP email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def guest_login(request):
    # Create or get a guest user
    guest_user, created = User.objects.get_or_create(username='guest_user')
    if created:
        guest_user.set_unusable_password()
        guest_user.save()
    
    # Log in the guest user
    auth_login(request, guest_user)
    return redirect('index')  # Redirect to the index view

@login_required
def index(request):
    if request.method == 'POST':
        form = ForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum_post = form.save(commit=False)
            if 'photo' in request.FILES:
                upload_result = cloudinary.uploader.upload(
                    request.FILES['photo'],
                    use_filename=True,
                    unique_filename=False,
                    folder='myapp/forum_photos'
                )
                forum_post.photo = upload_result['url']
            forum_post.save()
            return render(request, 'index.html', {'form': ForumForm(), 'success': True})
        else:
            return render(request, 'index.html', {'form': form, 'success': False})
    else:
        form = ForumForm()
    return render(request, 'index.html', {'form': form})