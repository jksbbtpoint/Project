from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


from datetime import datetime
from django.db.models.signals import post_save
# Create your models here.

CATEGORIES = (  
    ('Hindi', 'Hindi'),
    ('English', 'English'),
)
TYPE = (  
    ('Academics', 'Academics'),
    ('Network Marketing', 'Network Marketing'),
    ('Self Help', 'Self Help'),
    ('Leadership', 'Leadership'),
    ('Ebook','Ebook'),
    ('Accounts', 'Accounts')

)
RATING=(
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10)
    


    )
#class User(AbstractUser):
    #class Meta:

        #unique_together = ('email',)

class book(models.Model):
    isbn=models.CharField(max_length=15)
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=40)
    lang=models.CharField(max_length=8, choices=CATEGORIES, default='English')
    Category=models.CharField(max_length=30, choices=TYPE,default='Self Help',blank=True,null=True)
    pic=models.FileField(upload_to='pic', default='/static/na.jpg')  
    stock=models.IntegerField(blank = True, null=True)
    price=models.IntegerField(blank = True, null=True)
    desc=models.TextField(max_length=20000,blank=True)
    review=models.CharField(max_length=500,blank=True, null=True)
    
    
    def __unicode__(self):
        return unicode(self.isbn)

class preimg(models.Model):
    fkbook=models.ForeignKey(book)
    pic1=models.FileField(upload_to='pic',blank=True, null=True)
    pic2=models.FileField(upload_to='pic',blank=True, null=True)
    def __unicode__(self):
        return unicode(self.fkbook.title)

class blog(models.Model):
    title=models.CharField(max_length=60)
    author=models.CharField(max_length=30)
    post=models.CharField(max_length=20000)
    date_created=models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __unicode__(self):
        return self.title

class comment(models.Model):
    bg=models.ForeignKey(blog)
    comments=models.CharField(max_length=200)
    name=models.CharField(max_length=80, null=True, blank=True, default='Sachin')
    datecreate=models.DateTimeField(auto_now=True, blank=True, null=True)
    def __unicode__(self):
        return self.comments

class likesonpost(models.Model):
    bg=models.ForeignKey(blog)
    name=models.CharField(max_length=80, null=True, blank=True, default='Sachin')
    like=models.IntegerField()
    class Meta:

        unique_together = ('bg', 'name')
    def __unicode__(self):
    
        return unicode(self.like)
    

class cart(models.Model):
    fkbook=models.ForeignKey(book)
    name=models.CharField(max_length=80, blank=True, default='Sachin')
    qty=models.IntegerField(blank = True, default='1')
    price=models.IntegerField(blank = True, default='1')
    stock=models.IntegerField(blank = True, default='1')
    Purchasedate=models.DateTimeField(blank=True, null=True)
    Returndate=models.DateTimeField(blank=True, null=True)
    orderno=models.IntegerField(blank=True,null=True)
    def __unicode__(self):
        return unicode(self.orderno)

class invoice(models.Model):
    bookisbn=models.IntegerField(blank = True, default='1')
    name=models.CharField(max_length=80, blank=True, default='Sachin')
    qty=models.IntegerField(blank = True, default='1')
    price=models.IntegerField(blank = True, default='1')
    stock=models.IntegerField(blank = True, default='1')
   
    
    
    def __unicode__(self):
        return self.name



class Profile(models.Model):
    user=models.OneToOneField(User)
    location=models.CharField(max_length=300,null=True,blank=True)
    occupation=models.CharField(max_length=50,null=True,blank=True)
    pic =models.FileField(upload_to='pic',blank=True, null=True)
    aadhar=models.BigIntegerField(default='123456789')
    wallet=models.IntegerField(default='0')
    sponsorid=models.IntegerField(default='0', null=True)
    myid=models.IntegerField(default='0')

    def __unicode__(self):
        return str(self.user)

class Selectadd(models.Model):
    name=models.CharField(max_length=100,null=True)
    select=models.IntegerField(null=True)
    payment=models.CharField(max_length=50, null=True,blank=True)
    def __unicode__(self):
        return unicode(self.name)
    
class resetpass(models.Model):
    serialid=models.IntegerField(null=True, blank=True)
    user=models.CharField(max_length=60)
    email=models.EmailField()
    create_date=models.DateTimeField(default=datetime.now,blank=True, null=True)
    def __unicode__(self):
        return unicode(self.user)

class Shipping(models.Model):
    user=models.ForeignKey(User)
    username=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100)
    address=models.TextField(max_length=300)
    pincode=models.IntegerField()
    state=models.CharField(max_length=25,default="Delhi")
    mob=models.IntegerField()



    def __unicode__(self):
        return str(self.username)

class returnbook(models.Model):
    order_no=models.IntegerField(blank=True,null=True)
    isbn=models.CharField(max_length=15)
    rate=models.IntegerField(choices=RATING,default='1')
    comment=models.TextField(max_length=20000,blank=True)
    user=models.CharField(max_length=50)
    class Meta:

        unique_together = ('order_no', 'isbn')

    def __unicode__(self):
        return unicode(self.rate)
    

    
class bookauthor(models.Model):
    name=models.CharField(max_length=60)
    about=models.TextField(max_length=20000)
    pic =models.FileField(upload_to='pic',blank=True, null=True)
    def __unicode__(self):
        return unicode(self.name)

class donate(models.Model):
    name=models.CharField(max_length=80)
    email=models.EmailField()
    ContactNo=models.IntegerField()
    pic1 =models.FileField(upload_to='pic',blank=True, null=True)
    pic2 =models.FileField(upload_to='pic',blank=True, null=True)
    YourPrice=models.IntegerField()
    def __unicode__(self):
        return unicode(self.name)

class verify(models.Model):
    email=models.EmailField()
    otp=models.IntegerField(null=True, blank=True)
    def __unicode__(self):
        return unicode(self.email)
    


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

 
