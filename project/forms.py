from django import forms
from project.models import BandFile


class UserCreateForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(render_value=False))
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)

class InvitedUserCreateForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(render_value=False))
    email = forms.EmailField() # needs to be disabled
    phone = forms.CharField(max_length=20, required=False)

class UserEditForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    new_password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(render_value=False), required=False)
    new_password_confirm = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(render_value=False), required=False)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)

class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))

class BandCreateForm(forms.Form):
    name = forms.CharField(max_length=20)
    bio = forms.CharField(label='Bio', widget=forms.Textarea(), required=False)
    url = forms.URLField(label='Website', required=False)

class BandEditForm(forms.Form):
    name = forms.CharField(max_length=20)
    bio = forms.CharField(label='Band Bio', widget=forms.Textarea(), required=False)
    url = forms.URLField(label='Your Web site', required=False)

class UploadBandFileForm(forms.ModelForm):
    class Meta:
        model = BandFile
        fields = ('description', 'file')
        
class ContactBandForm(forms.Form):
    name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=20)
    service = forms.BooleanField(label="Service?")
    cost = forms.DecimalField(min_value = 0, max_digits = 6, decimal_places = 2)

class UnavailabilityEntryForm(forms.Form):
    all_day = forms.BooleanField(label="All day?", required=False)
    date_start = forms.DateField()
    date_end = forms.DateField()
    time_start = forms.TimeField(widget=forms.TimeInput(), input_formats=["%H:%M"])
    time_end = forms.TimeField(widget=forms.TimeInput(), input_formats=["%H:%M", "%H:%M:%S"])
    
class RehearsalEntryForm(forms.Form):
    date_start = forms.DateField(label="Date")
    time_start = forms.TimeField(widget=forms.TimeInput(), input_formats=["%H:%M"])
    time_end = forms.TimeField(widget=forms.TimeInput(), input_formats=["%H:%M"])
    place = forms.CharField(max_length=30)
    costs = forms.DecimalField(max_digits=10, decimal_places=2)

class GigEntryForm(forms.Form):
    date_start = forms.DateField(label="Date start")
    date_end = forms.DateField(label="Date end")
    time_start = forms.TimeField(widget=forms.TimeInput(), input_formats=["%H:%M"])
    time_end = forms.TimeField(widget=forms.TimeInput(), input_formats=["%H:%M"])
    place = forms.CharField(label="Place/Venue", max_length=30)
    costs = forms.DecimalField(label="Band Total Costs", min_value = 0, max_digits=10, decimal_places=2)
    ticket = forms.DecimalField(label="Ticket Cost", min_value = 0, max_digits=10, decimal_places=2)
