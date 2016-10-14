from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.http import require_POST
from incidents.models import BusinessLine

import json

from fir_async.models import NotificationPreference
from fir_async.registry import registry
from fir_async.forms import NotificationPreferenceFormset


@login_required
def preferences(request):

    class NotificationPreferenceForm(forms.ModelForm):
        event = forms.ChoiceField(choices=registry.get_event_choices(), disabled=True, widget=forms.HiddenInput())
        method = forms.ChoiceField(choices=registry.get_method_choices(), disabled=True, widget=forms.HiddenInput())
        business_lines = forms.ModelMultipleChoiceField(BusinessLine.authorization.for_user(request.user,
                                                                                            'incidents.view_incidents'),
                                                        required=False)

        class Meta:
            fields = "__all__"

    formset = forms.inlineformset_factory(User, NotificationPreference,
                                          formset=NotificationPreferenceFormset,
                                          form=NotificationPreferenceForm)
    if request.method == 'POST':
        fs = formset(request.POST, instance=request.user)
        if fs.is_valid():
            fs.save()
        return redirect('user:profile')
    else:
        fs = formset(instance=request.user)

    return render(request, "fir_async/preferences.html", {'formset': fs})


@require_POST
@login_required
def method_configuration(request, method):
    method_object = registry.methods.get(method, None)
    if method is None:
        return redirect('user:profile')
    form = method_object.form(request.POST, user=request.user)
    if form.is_valid():
        form.save()
    return redirect('user:profile')
