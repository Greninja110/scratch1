from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Users

@login_required
def lab_assistant_dashboard(request):
    """
    Lab Assistant dashboard view
    """
    # Check if the user has lab_assistant role
    try:
        user_profile = Users.objects.get(user=request.user)
        if user_profile.role != 'lab_assistant':
            return redirect('login')
    except Users.DoesNotExist:
        return redirect('login')
    
    context = {
        'title': 'Lab Assistant Dashboard',
        'user_profile': user_profile
    }
    return render(request, 'lab_assistant_portal/dashboard.html', context)