from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Users

@login_required
def student_dashboard(request):
    """
    Student dashboard view
    """
    # Check if the user has student role
    try:
        user_profile = Users.objects.get(user=request.user)
        if user_profile.role != 'student':
            return redirect('login')
    except Users.DoesNotExist:
        return redirect('login')
    
    context = {
        'title': 'Student Dashboard',
        'user_profile': user_profile
    }
    return render(request, 'student_portal/dashboard.html', context)