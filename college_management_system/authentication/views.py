import logging
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .forms import CustomLoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import PasswordResetToken
from core.models import Users

# Set up logger
logger = logging.getLogger('authentication')

def login_view(request):
    """
    Custom login view with remember me functionality
    """
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)

    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # If remember me is checked, set a longer session expiry
                if remember_me:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                else:
                    request.session.set_expiry(0)  # Session expires when browser is closed
                
                logger.info(f"User {username} logged in successfully")
                return redirect_based_on_role(user)
            else:
                messages.error(request, 'Invalid email or password')
                logger.warning(f"Failed login attempt for email: {username}")
        else:
            logger.warning(f"Invalid form submission: {form.errors}")
    else:
        form = CustomLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    """
    Logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')

def forgot_password_view(request):
    """
    View for requesting a password reset
    """
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                
                # Generate a unique token
                token = str(uuid.uuid4())
                
                # Save the token
                PasswordResetToken.objects.create(
                    user=user,
                    token=token
                )
                
                # Send email with reset link
                reset_url = request.build_absolute_uri(
                    reverse('reset_password', kwargs={'token': token})
                )
                
                subject = 'Password Reset Request'
                message = f"""
                Hello {user.username},
                
                You've requested to reset your password. Please click the link below to reset your password:
                
                {reset_url}
                
                If you didn't request this, please ignore this email.
                
                Thank you,
                College Management System
                """
                
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                
                messages.success(request, 'Password reset link has been sent to your email')
                logger.info(f"Password reset email sent to {email}")
                return redirect('login')
            except User.DoesNotExist:
                logger.warning(f"Password reset requested for non-existent email: {email}")
                # Still show success message to prevent email enumeration
                messages.success(request, 'If your email exists in our system, you will receive a password reset link')
        else:
            logger.warning(f"Invalid form submission: {form.errors}")
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'authentication/forgot_password.html', {'form': form})

def reset_password_view(request, token):
    """
    View for resetting password using a token
    """
    try:
        # Find the token and ensure it's not used and not expired (valid for 24 hours)
        reset_token = PasswordResetToken.objects.get(
            token=token,
            is_used=False,
            created_at__gt=timezone.now() - timedelta(hours=24)
        )
        
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                user = reset_token.user
                user.set_password(form.cleaned_data.get('new_password'))
                user.save()
                
                # Mark the token as used
                reset_token.is_used = True
                reset_token.save()
                
                messages.success(request, 'Your password has been reset successfully. You can now login.')
                logger.info(f"Password reset successful for user: {user.email}")
                return redirect('login')
        else:
            form = ResetPasswordForm()
        
        return render(request, 'authentication/reset_password.html', {'form': form})
    
    except PasswordResetToken.DoesNotExist:
        logger.warning(f"Invalid or expired password reset token: {token}")
        messages.error(request, 'The password reset link is invalid or has expired')
        return redirect('forgot_password')

def redirect_based_on_role(user):
    """
    Helper function to redirect users based on their role
    """
    try:
        user_profile = Users.objects.get(user=user)
        role = user_profile.role
        
        if role == 'admin':
            return redirect('admin_dashboard')
        elif role == 'hod':
            return redirect('hod_dashboard')
        elif role == 'faculty':
            return redirect('faculty_dashboard')
        elif role == 'lab_assistant':
            return redirect('lab_assistant_dashboard')
        elif role == 'student':
            return redirect('student_dashboard')
        else:
            logger.error(f"Unknown role for user: {user.email}")
            return redirect('login')
    except Users.DoesNotExist:
        logger.error(f"User profile not found for user: {user.email}")
        return redirect('login')