from django import forms
#myapp/forms.py


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
