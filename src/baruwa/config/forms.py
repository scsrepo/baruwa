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
#

from django import forms
from baruwa.accounts.models import UserAddresses
from baruwa.config.models import MailHost
from baruwa.utils.regex import dom_re

class MailHostForm(forms.ModelForm):
    "Mail host add form"
    address = forms.RegexField(regex=dom_re, widget=forms.TextInput(attrs={'size':'50'}))
    useraddress = forms.ModelChoiceField(queryset=UserAddresses.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = MailHost
        exclude = ('id')

class EditMailHost(forms.ModelForm):
    "Edit Mail host form"
    address = forms.RegexField(regex=dom_re, widget=forms.TextInput(attrs={'size':'50'}))
    class Meta:
        model = MailHost
        exclude = ('id', 'useraddress')
        
class DeleteMailHost(forms.ModelForm):
    "Delete a mail host form"
    id = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = MailHost
        fields = ('id',)