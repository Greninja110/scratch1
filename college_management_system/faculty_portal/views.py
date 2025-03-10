from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Users

@login_required
def faculty_dashboard(request):
    """
    Faculty dashboard view
    """
    # Check if the user has faculty role
    try:
        user_profile = Users.objects.get(user=request.user)
        if user_profile.role != 'faculty':
            return redirect('login')
    except Users.DoesNotExist:
        return redirect('login')
    
    context = {
        'title': 'Faculty Dashboard',
        'user_profile': user_profile
    }
    return render(request, 'faculty_portal/dashboard.html', context)