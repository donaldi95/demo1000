from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .admin import UserCreationForm
from campaign.models import Campaign

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required(login_url='/login/')
def profile(request):
    logged_in_user_posts = Campaign.objects.filter(user_id=request.user)
    return render(request, 'users/profile.html', {'campaigns': logged_in_user_posts})

#get the campaign for each user