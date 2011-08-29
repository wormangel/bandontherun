from django import forms

class BandCreateForm(forms.Form):
    name = forms.CharField(max_length=20)
    bio = forms.CharField(label='Band Bio',widget=forms.Textarea())
    url = forms.URLField(label='Your Web site', required=False)

class BandEditForm(forms.Form):
    name = forms.CharField(max_length=20)
    bio = forms.CharField(label='Band Bio',widget=forms.Textarea())
    url = forms.URLField(label='Your Web site', required=False)
