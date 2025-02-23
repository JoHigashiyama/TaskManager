from django import forms

class RegisterUser(forms.Form):
    username = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder':'User'
        })
    )
    password = forms.CharField(
        label='',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Password'
        })
    )