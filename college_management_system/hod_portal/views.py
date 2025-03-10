from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Users

@login_required
def hod_dashboard(request):
    """
    HOD dashboard view
    """
    # Check if the user has HOD role
    try:
        user_profile = Users.objects.get(user=request.user)
        if user_profile.role != 'hod':
            return redirect('login')
    except Users.DoesNotExist:
        return redirect('login')
    
    context = {
        'title': 'HOD Dashboard',
        'user_profile': user_profile
    }
    return render(request, 'hod_portal/dashboard.html', context)