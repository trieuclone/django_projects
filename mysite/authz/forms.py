from django import forms
from django.core import validators
from django.forms import ModelForm
from authz.models import Author, Book

class BasicForm(forms.Form):
    name = forms.CharField(validators=[validators.MinLengthValidator(2, "Ít nhất 2 ký tự trỏ lên")])
    age = forms.IntegerField()
    birth_date = forms.DateField()

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'