from django import forms

class SearchForm(forms.Form):
    task = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={
            'placehoder':'キーワードを入力'
        })
    )
