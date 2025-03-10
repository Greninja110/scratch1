from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Users

@login_required
def admin_dashboard(request):
    """
    Admin dashboard view
    """
    # Check if the user has admin role
    try:
        user_profile = Users.objects.get(user=request.user)
        if user_profile.role != 'admin':
            return redirect('login')
    except Users.DoesNotExist:
        return redirect('login')
    
    context = {
        'title': 'Admin Dashboard',
        'user_profile': user_profile
    }
    return render(request, 'admin_portal/dashboard.html', context)