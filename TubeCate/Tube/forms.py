from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Link,Clan,Comment
from django.contrib.auth.models import User
class ClanCreationForm(forms.ModelForm):
    
    class Meta:
        model=Clan
        fields=['name','description','url','tag']

class LinkCreationForm(forms.ModelForm):
    class Meta:
        model=Link
        fields=['title','link','description']  

class RegisterForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['title','content']
        