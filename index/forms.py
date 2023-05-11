from django import forms

class MyForm(forms.Form):
    text_input = forms.CharField()
    csv_upload = forms.FileField(required=False)
    check_box = forms.BooleanField(required=False)