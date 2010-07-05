# 
# Baruwa - Web 2.0 MailScanner front-end.
# Copyright (C) 2010  Andrew Colin Kissa <andrew@topdog.za.net>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, AdminPasswordChangeForm
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME, logout
from django.contrib.auth.models import User
from baruwa.accounts.forms import UserProfileForm, UserCreateForm, UserAddressForm, \
OrdUserProfileForm, UserUpdateForm, AdminUserUpdateForm, EditAddressForm, \
DeleteAddressForm, DeleteUserForm
from baruwa.accounts.profile import set_user_addresses
from baruwa.accounts.models import UserAddresses, UserProfile
from baruwa.utils.decorators import onlysuperusers, authorized_users_only, only_admins

def login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    login
    """
    from django.conf import settings
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            set_user_addresses(request)
            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()
    return render_to_response('accounts/login.html', {'form': form,redirect_field_name: redirect_to,},
        context_instance=RequestContext(request))

@login_required
@only_admins
def index(request, page=1, direction='dsc', order_by='id'):
    """
    index
    """
    if request.user.is_superuser:
        users = User.objects.all()
    else:
        domains = request.session['user_filter']['addresses']
        q = Q(id=request.user.id)
        for domain in domains:
            q = q | Q(username__endswith=domain)
        users = User.objects.filter(q)
        
    return object_list(request, template_name='accounts/index.html', 
        queryset=users, paginate_by=10, page=page, extra_context={'app':'accounts', 'list_all':1})
        
@login_required
@onlysuperusers
def create_account(request, template_name='accounts/create_account.html'):
    """
    create_account
    """  
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('user-profile', args=[user.id]))
    else:
        form = UserCreateForm()
    for name in ['username', 'first_name', 'last_name', 'email', 'password']:
        form.fields[name].widget.attrs['size'] = '45'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@login_required
@authorized_users_only
def update_account(request, user_id, template_name='accounts/update_account.html'):
    """update_account"""
    user_account = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        if request.user.is_superuser:
            form = AdminUserUpdateForm(request.POST, instance=user_account)
        else:
            form = UserUpdateForm(request.POST, instance=user_account)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user-profile', args=[user_id]))
    else:
        if request.user.is_superuser:
            form =  AdminUserUpdateForm(instance=user_account)
            form.fields['username'].widget.attrs['size'] = '45'
        else:
            form = UserUpdateForm(instance=user_account)
    for name in ['first_name', 'last_name', 'email']:
        form.fields[name].widget.attrs['size'] = '45'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@authorized_users_only
def delete_account(request, user_id, template_name='accounts/delete_account.html'):
    """delete_account"""
    user_account = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = DeleteUserForm(request.POST, instance=user_account)
        if form.is_valid():
            if user_account.id == request.user.id:
                return HttpResponseRedirect(reverse('user-profile', args=[user_id]))
            else:
                try:
                    user_account.delete()
                    return HttpResponseRedirect(reverse('accounts'))
                except:
                    return HttpResponseRedirect(reverse('user-profile', args=[user_id]))
    else:
        form = DeleteUserForm(instance=user_account)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    
@login_required
@onlysuperusers
def add_address(request, user_id, template_name='accounts/add_address.html'):
    """
    Adds an address to a user profile.
    """
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user-profile', args=[user_id]))
    else:
        form = UserAddressForm()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@onlysuperusers
def edit_address(request, address_id, template_name='accounts/edit_address.html'):
    """
    Edit an address
    """
    a = get_object_or_404(UserAddresses, pk=address_id)
    if request.method == 'POST':
        form = EditAddressForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user-profile', args=[a.user.id]))
    else:
        form = EditAddressForm(instance=a)
    user_id = a.user.id
    a = None
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@onlysuperusers
def delete_address(request, address_id, template_name='accounts/delete_address.html'):
    """Delete address"""
    a = get_object_or_404(UserAddresses, pk=address_id)
    if request.method == 'POST':
        id = a.user.id
        a.delete()
        return HttpResponseRedirect(reverse('user-profile', args=[id]))
    else:
        form = DeleteAddressForm(instance=a)
    address = a.address
    a = None
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@onlysuperusers
def change_password(request, user_id, template_name='accounts/change_pw.html'):
    """
    Admin change users password
    """
    user_account = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user_account, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user-profile', args=[user_id]))
    else:
        form = AdminPasswordChangeForm(user_account)
    user_account = None
    form.fields['password1'].widget.attrs['size'] = '45'
    form.fields['password2'].widget.attrs['size'] = '45'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
@authorized_users_only
def user_profile(request, user_id, template_name='accounts/user_profile.html'):
    """
    Displays user profiles.
    """
    addresses = None
    account_info = get_object_or_404(User, pk=user_id)            
    account_profile = account_info.get_profile()
    if not account_info.is_superuser:
        addresses = UserAddresses.objects.filter(user=account_info)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def profile(request):
    """
    Redirects to current users profile page
    """
    return HttpResponseRedirect(reverse('user-profile', args=[request.user.id]))
    
@login_required
@authorized_users_only
def update_profile(request, user_id, template_name='accounts/update_profile.html'):
    """
    Updates a user profile.
    """
    user_account = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user_account)

    if request.method == 'POST':
        if request.user.is_superuser:
            form = UserProfileForm(request.POST, instance=user_profile)
        else:
            form = OrdUserProfileForm(request.POST, instance=user_profile)
            
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user-profile', args=[user_id]))
    else:
        if request.user.is_superuser:
            form = UserProfileForm(instance=user_profile)
        else:
            form = OrdUserProfileForm(instance=user_profile)
            
    user_account = None
    user_profile = None
    form.fields['user_id'].widget.attrs['value'] = user_id
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))