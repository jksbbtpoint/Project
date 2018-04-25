from django import forms
from .models import *
from django.contrib.auth.models import User
from django.forms import ModelForm


class mybooks(forms.ModelForm):
    desc = forms.CharField( widget=forms.Textarea (attrs={'class':'form-control'}),
                             required=True)
    buy = forms.URLField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             required=False)
    pic = forms.FileField()
    
    title=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=100,
                             required=True)
    isbn=forms.IntegerField(widget=forms.TextInput
                             (attrs={'class':'form-control'}))
    author=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)
    stock=forms.IntegerField(widget=forms.TextInput
                             (attrs={'class':'form-control'}))
    
    price=forms.IntegerField(widget=forms.TextInput
                             (attrs={'class':'form-control'}))
    class Meta:
        model=book
        fields='__all__'

class likesform(forms.ModelForm):
    class Meta:
        fields='__all__'

class Selectaddform(forms.ModelForm):
    class Meta:
        model=Selectadd
        fields=[]
        
class resetpassform(forms.ModelForm):
    user=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username'}),max_length=30, required=True)
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your Email',}),max_length=30, required=True)
    
    class Meta:
        model=resetpass
        fields=['user','email']

class verifyform(forms.ModelForm):
    class Meta:
        model=verify
        fields=['email']    

class returnform(forms.ModelForm):
    isbn=forms.IntegerField(widget=forms.TextInput
                             (attrs={'class':'form-control'}))
    order_no=forms.IntegerField(widget=forms.TextInput
                             (attrs={'class':'form-control'}))
    comment = forms.CharField( widget=forms.Textarea (attrs={'class':'form-control'}),
                             required=True)
    
    class Meta:
        model=returnbook
        fields=['order_no','isbn','rate','comment']

class authorform(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=60,
                             required=True)
    pic = forms.FileField()
    about=forms.CharField(widget=forms.Textarea
                             (attrs={'class':'form-control'}),
                             max_length=20000,
                             required=True)
    class Meta:
        model=bookauthor
        fields=['name','pic','about']
class commentform(forms.ModelForm):

    comments = forms.CharField( widget=forms.TextInput (attrs={'class':'form-control'}),
                             required=True)
    class Meta:
        model=comment
        fields=['comments']


class myblog(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=100,
                             required=True)
    
    post=forms.CharField(widget=forms.Textarea
                             (attrs={'class':'form-control'}),
                             max_length=20000,
                             required=True)
    
    #apic=forms.FileField(required=False)
    class Meta:
        model=blog
        fields=['title','post']

class cartform(forms.ModelForm):
   
    class Meta:
        model=cart
        fields=['qty']
    
class invoiceform(forms.ModelForm):
   
    class Meta:
        model=invoice
        fields='__all__'
    

        
class Regforms(forms.ModelForm):

    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),max_length=30, required=True)
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),max_length=30, required=True)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),max_length=30, required=True)
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email',}),max_length=30, required=True)
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','pattern':'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}'}),max_length=30, required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password',}),max_length=30, required=True)  
    
    
    class Meta:
        model=User
        fields=['first_name','last_name','username', 'email', 'password','confirm_password']
    def clean(self):
        cleaned_data = super(Regforms, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class ProfileForm(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)

    last_name=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)

    location=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=300,
                             required=True)
    occupation= forms.CharField(widget=forms.TextInput
                            (attrs={'class': 'form-control'}),
                            max_length=30,
                            required=True)
    


    email=forms.CharField(widget=forms.EmailInput
                             (attrs={'class':'form-control'}),
                             max_length=30,)
    pic=forms.FileField(initial='pic/photo.jpg',required=False)
    
    aadhar=forms.IntegerField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),required=True)
    class Meta:
        model=User
        fields=['first_name','last_name','location','occupation','email','pic','aadhar']

class shipform(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)
    mob=forms.IntegerField(widget=forms.TextInput
                             (attrs={'class':'form-control'}))
    address=forms.CharField(widget=forms.Textarea
                             (attrs={'class':'form-control'}),
                             max_length=300,
                             required=True)
    
    class Meta:
        model=Shipping
        fields=['name','mob','address','pincode','state']

class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(
        widget = forms.PasswordInput(attrs={'class':'form'}),
        label="Old Password",
        required=True)


    new_password = forms.CharField(
        widget = forms.PasswordInput(attrs={'class':'form'}),
        label="New Password",
        required=True)




    confirm_password = forms.CharField(
        widget = forms.PasswordInput(attrs={'class':'form'}),
        label="Confirm your Password",
        required=True)


    class Meta:
            model=User
            fields=['old_password','new_password','confirm_password']

class resetpasswordForm(forms.ModelForm):
    


    new_password = forms.CharField(
        widget = forms.PasswordInput(attrs={'class':'form'}),
        label="New Password",
        required=True)




    confirm_password = forms.CharField(
        widget = forms.PasswordInput(attrs={'class':'form'}),
        label="Confirm your Password",
        required=True)


    class Meta:
            model=User
            fields=['new_password','confirm_password']
    
