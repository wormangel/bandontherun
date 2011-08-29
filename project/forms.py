from django import forms

class UserForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(render_value=False))
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    

class BandForm(forms.Form):
    band_name = forms.CharField(max_length=20)
    shortcut_name = forms.CharField(max_length=20)
    bio = forms.CharField(label='Band Bio')
    url = forms.URLField(label='Your Web site', required=False)
    

class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    
