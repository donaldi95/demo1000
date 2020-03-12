from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .admin import UserCreationForm
from campaign.models import Campaign
from user_activities.models import Campaign_enrollment,Peak_annotations
from .models import MyUser
from django.views.defaults import page_not_found
from django.http import HttpResponseForbidden,HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import (
    UpdateView,
    )
from .forms import UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.user.is_authenticated:
        return render(request, 'users/profile.html' )

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
    actualUser_enrolledTo = list(Campaign_enrollment.objects.filter(user_id = request.user.id).values())
    enrolledTo            = Campaign_enrollment.objects.filter(user_id = request.user.id)
    campaigns             = Campaign.objects.filter( id__in  = [x['campaign_id_id'] for x in actualUser_enrolledTo])
    annotations           = Peak_annotations.objects.filter(user_id  = request.user.id )
    #print(campaigns)
    logged_in_user_posts  = Campaign.objects.filter(user_id=request.user)
    #form = EditProfileForm(instance=request.user.profile)
    #if request.method == 'POST':
        #check if the submited form is the right one
    form = PasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
        if 'updatePassowrd' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, 'Please correct the error below.')
        elif 'profiledata' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                               request.FILES,
                               instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
    else:
        form = PasswordChangeForm(request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    return render(request, 'users/profile.html', {'u_form': u_form, 'p_form': p_form,'form':form,'campaigns': logged_in_user_posts,'campaigns_enrolled':campaigns,'annotations':annotations})


def index(request):
    return render(request,'users/index.html')
#get the campaign for each user


###############
#error templates
###############
def error_404(request, exception):
    data = {}
    return render(request,'users/404.html', data)

def error_500(request):
    data = {}
    return render(request,'users/500.html', data)

def error_403(request,  exception):
    data = {}
    return render(request,'users/403.html', data)