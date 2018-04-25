from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import *
from .forms import *
from django.http import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from instamojo_wrapper import Instamojo
from datetime import datetime
from datetime import date
import datetime
import random
from dateutil.relativedelta import relativedelta
# Create your views here.







def jks(request):
    price=0
    user=Profile.objects.get(user=request.user)
    
    for s in cart.objects.filter(Q(name=request.user.first_name)&Q(Purchasedate__isnull=True)):
        price=price+s.price
    ttl = price-user.wallet
    z=Selectadd.objects.all().last()
    z.payment='Online Transaction'
    z.save()
    j=Shipping.objects.get(id=z.select)

    api = Instamojo(api_key="256d500434abba8c46c315cd4d4af62a", auth_token="f05c078a76da2779dd48aa41b500c964");
    #api = Instamojo(api_key="275e4ff7e86e210380002c746c924996", auth_token="a5385ca1e629f99be6ebd5af74104adb", endpoint='https://test.instamojo.com/api/1.1/');

    
    response = api.payment_request_create(
      purpose= 'Buying Books',
      amount= ttl,
      buyer_name= request.user.get_full_name(),
      email= request.user.email,
      phone= j.mob,
      redirect_url= 'http://127.0.0.1:8000/invoice',
      send_email= 'False',
      send_sms= 'False',
      webhook= 'http://www.example.com/webhook/',
      allow_repeated_payments= 'False',
    )
    a=response['payment_request']['longurl']
    print response['payment_request']['status']
    
    return HttpResponseRedirect(response['payment_request']['longurl'])
    
def home(request):
    
    a=book.objects.filter(Category='Ebook')
    b=book.objects.filter(~Q(Category='Ebook'))
    return render(request,'Home.html',{'a':a,'b':b})
    

def login(request):
    
    return render(request,'Login.html')

@login_required
def books(request):
    a=book.objects.all()
    return render(request,'Books.html',{'record':a})

@login_required
def ret(request,on,isno):
    if request.method=='POST':
        forms = returnform(request.POST)
        ordernoquery=request.POST['order_no']
        isbnquery=request.POST['isbn']
        jks=cart.objects.filter(Q(Returndate=None)&Q(orderno=ordernoquery)&Q(fkbook__isbn=isbnquery)&Q(name=request.user.first_name))
        if jks:
            
            if forms.is_valid():
                retbook = forms.save(commit=False)
                retbook.user=request.user.first_name
                for s in cart.objects.filter(Q(name=request.user.first_name)&Q(Returndate__isnull=True)&Q(orderno=ordernoquery)&Q(fkbook__isbn=isbnquery)):
                    if s.fkbook.Category == 'Ebook':
                        messages.error(request, 'You cannot return an Ebook.')
                        return HttpResponseRedirect('/ret')
                    else:
                        s.Returndate=datetime.datetime.now()
                        
                        s.save()
                        
                        rdate= s.Returndate.date()
                        pdate= s.Purchasedate.date()
                        
                        rent = rdate-pdate
                        print rent.days
                        if rent.days <= 17:
                            refund='75%'
                            money =int(s.fkbook.price*0.75)
                        elif rent.days <=32 and rent.days >17:
                            refund='65%'
                            money =int(s.fkbook.price*0.65)
                        elif rent.days <=45 and rent.days >32:
                            refund='55%'
                            money =int(s.fkbook.price*0.55)
                        else:
                            refund = '40% maximum'
                            money = 'dependent on the condition of the book'
                            
                        html_content="You will get %s as refund which is INR %s"%(refund,money)
                        notification="You have to refund %s as refund which is INR %s to %s. Order No. %s"%(refund,money,request.user.email,s.orderno)
                        send_mail('Order Confirmation',html_content, settings.EMAIL_HOST_USER,[request.user.email],fail_silently=False)
                        send_mail('Order Confirmation',notification, settings.EMAIL_HOST_USER,['info@bbtpoint.com'],fail_silently=False)
                        
                        forms.save()
                return HttpResponseRedirect('/orders')

    else:
        forms=returnform()
        
    return render(request,'return.html',{'forms':forms,'Order':on,'ISBN':isno})

def bstore(request):
   
    
    a=book.objects.all()
    if request.user.is_anonymous():
        return render(request,'store.html',{'record':a})
        
    else:
        n=cart.objects.filter(Q(name=request.user.first_name)&Q(Purchasedate=None)).count()
        return render(request,'store.html',{'record':a,'countcart':n})
        
    
        
def catstore(request,d):
    print d
    a=book.objects.filter(Category=d)
    return render(request,'store.html',{'record':a})

def searchorders(request):
    if request.method=='POST':
        squery=request.POST['search_box']
        if squery:
            a=cart.objects.filter(Q(orderno__icontains=squery)&Q(name=request.user.first_name))
            if a:
                return render(request,'myorders.html',{'order':a})
            else:
                messages.error(request, 'No order exist with this order no.')
                return HttpResponseRedirect('/orders')
        else:
            return HttpResponseRedirect('/orders')
    

def search(request):
    if request.method=='POST':
        squery=request.POST['search_box']
        if squery:
            a=book.objects.filter(Q(title__icontains=squery)|Q(isbn__icontains=squery)|Q(author__icontains=squery)|Q(lang__icontains=squery)|Q(Category__icontains=squery))
            if a:
                return render(request,'store.html',{'record':a})
            else:
                messages.error(request, 'No match found.')
                return HttpResponseRedirect('/store')
        else:
            return HttpResponseRedirect('/store')
    

def aboutus(request):
    return render(request,'Aboutus.html')

def register(request):
    return render(request,'Signup.html')

def register(request):
    if request.method == 'POST':
        otp=request.POST.get('otp')
        
        email=request.POST.get('email',False)
        print otp
        print email
        form = Regforms(request.POST)
        if form.is_valid():
            if verify.objects.filter(Q(email=email)&Q(otp=otp)):
                form = User.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    
                          
                )
                          
            else:
                messages.success(request, 'OTP is wrong.')
            
            return HttpResponseRedirect('/profile')
    else:
        form=Regforms()
    return render(request,'Signup.html',{'form':form})

def verifyfun(request):
    if request.method == "POST":
        form = verifyform(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            try:
                form.save()
                for s in verify.objects.filter(Q(email=email)&Q(otp__isnull=True)):
                    s.otp=random.randint(99,99999)
                    if verify.objects.filter(Q(otp=s.otp)):
                        continue
                    else:
                        s.save()
                    html_content="Your One Time Password: %s \n http://127.0.0.1:8000/register/"%(s.otp)
                    notification="Verify your email"
                    send_mail('Verify email',html_content, settings.EMAIL_HOST_USER,[email],fail_silently=True)
                messages.success(request,'Enter OTP received on mail.')
                return HttpResponseRedirect('/register')
            except:
                return render(request,'verify.html')
    else:
        form = verifyform()
        
    return render(request,'verify.html',{'form':form})

def auth_view(request):
    username = password = ''
    username=request.POST['username'] #name in login.html file
    password=request.POST['password'] #name in login.html file
    if username=='sachin':
        user=auth.authenticate(username=username, password = password) #password is stored in hash form we need key to decode. (== not allowed)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/sachin/')
        else:
            messages.error(request, 'Username or password is wrong.')
            return HttpResponseRedirect('/login/')
    else:
        user=auth.authenticate(username=username, password = password) #password is stored in hash form we need key to decode. (== not allowed)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/store/')
        else:
            messages.error(request, 'Username or password is wrong.')
            return HttpResponseRedirect('/login/')
        


def loggedin(request):
    
    if request.user.is_authenticated():
        a = book.objects.all()
        return render(request,'home.html',{'record':a})
    else:
        return HttpResponse('Login Required')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/home/')

@login_required
def addbook(request):
    
    if request.user.username=='sachin':
        if request.method=='POST':
            forms = mybooks(request.POST, request.FILES)
            if forms.is_valid():
                book=forms.save(commit=False)
                book.total=1*book.price
                book=book.save()
                
                return HttpResponseRedirect('/sachin')   
        else:
            forms=mybooks()
        return render(request,'addbook.html',{'forms':forms})
    else:
        return HttpResponse('You are not allowed to add books.')
    

def det(request,d):
    n=book.objects.get(id=d)
    try:
        pre=preimg.objects.get(fkbook__isbn=n.isbn)
        return render(request,'detail.html',{'data':n,'pre':pre})
    except:
        return render(request,'detail.html',{'data':n})
@login_required
def newpost(request):
    if request.method=='POST':
        forms = myblog(request.POST, request.FILES)
        if forms.is_valid():
            blog = forms.save(commit=False)
            blog.author = request.user.username
            blog =blog.save()
            return HttpResponseRedirect('/allpost')   
    else:
        forms=myblog()
        
    return render(request,'wnewpost.html',{'forms':forms})


def allpost(request):
    n=blog.objects.order_by('-date_created')
    j=comment.objects.all().order_by('-datecreate')
    k=User.objects.all()
    s=likesonpost.objects.all()
    return render(request, 'viewpost.html',{'all':n,'jks':j,'k':k,'s':s})

@login_required
def likes(request,d):
    try:
        n=blog.objects.get(title=d)
        p=likesonpost(bg=n, name=request.user.username, like=1)
        p.save()
        return HttpResponseRedirect('/allpost')
    except:
        messages.success(request,'You have liked this post already.')
        return HttpResponseRedirect('/allpost')


def like(request,d):
    p=likesonpost.objects.filter(bg__title=d)
    print p
    k=User.objects.all()
    return render(request, 'modal1.html',{'p':p,'k':k})
    

@login_required
def mypost(request):
    n=blog.objects.filter(author=request.user).order_by('-date_created')
    j=User.objects.get(Q(username=request.user))
    comm=comment.objects.all().order_by('-datecreate')
    return render(request, 'myposts.html',{'my':n,'jks':j,'comm':comm})
@login_required
def authpost(request,d):
    n=blog.objects.filter(author=d).order_by('-date_created')
    j=User.objects.get(Q(username=d) | Q(first_name=d))
    comm=comment.objects.all().order_by('-datecreate')
    return render(request, 'myposts.html',{'my':n,'jks':j,'comm':comm})

@login_required
def com(request,d):
    
    n=blog.objects.get(title=d)
    if request.method=="POST":
        forms=commentform(request.POST)
        if forms.is_valid():
            
            
            osc=forms.save(commit=False)
            osc.bg=n
            osc.name=request.user
            forms.save()
            return HttpResponseRedirect('/home')
    else:
        forms=commentform()
        n=blog.objects.get(title=d)
        j=comment.objects.all()
        k=User.objects.all()
    return render(request, 'comment.html', {'forms':forms,'post':n, 'comm':j,'k':k})

@login_required
def add2cart(request,d):
    
    user=request.user.first_name
    n=book.objects.get(isbn=d)
    k=cart.objects.filter(Q(fkbook__isbn=d)&Q(name =request.user.first_name)&Q(Purchasedate = None))
    if not k:
        if request.method=="POST":
            forms=cartform(request.POST)
            if forms.is_valid():
                qty=forms.cleaned_data.get('qty')
                print qty
                if qty<1:
                    messages.success(request,'Enter a valid quantity.')
                    return HttpResponseRedirect('/cart/%s'%d)
                else:                   
                    a2c=forms.save(commit=False)
                    a2c.fkbook=n
                    a2c.price=int(qty)*a2c.fkbook.price
                    a2c.name=request.user.first_name
                    a2c.stock=a2c.fkbook.stock
                    forms.save()
                    return HttpResponseRedirect('/mycart/')
                
                    
        else:
            forms=cartform()
            details= book.objects.get(isbn=d)
            n=book.objects.all()
            cartno=cart.objects.filter(Q(name=request.user.first_name)&Q(Purchasedate=None)).count()
            try:
                pre=preimg.objects.get(fkbook__isbn=d)
                return render(request, 'store.html', {'forms':forms,'details':details,'n':n,'countcart':cartno,'pre':pre})
            except:
                return render(request, 'store.html', {'forms':forms,'details':details,'n':n,'countcart':cartno})
    elif k:
        messages.success(request, 'Book already exist in your cart.')
        return HttpResponseRedirect('/mycart/')
        
    
    
    
        

@login_required    
def delcomm(request,d):
    delcomm=comment.objects.get(id=d)
    delcomm.delete()
    return HttpResponseRedirect('/allpost')

@login_required
def delete(request,d):
    delpost=blog.objects.get(id=d)
    delpost.delete()
    return HttpResponseRedirect('/allpost')

@login_required
def user_profile(request):
    user=request.user
    sponsorid=request.POST.get('sponsorid')
    print sponsorid
    jks=Profile.objects.get(user=user)
    if request.method=='POST':
        forms=ProfileForm(request.POST, request.FILES, instance=jks)
        if forms.is_valid():
            user.first_name=forms.cleaned_data.get('first_name')
            user.last_name=forms.cleaned_data.get('last_name')
            user.email=forms.cleaned_data.get('email')
            user.profile.occupation=forms.cleaned_data.get('occupation')
            user.profile.location=forms.cleaned_data.get('location')
            user.profile.pic=forms.cleaned_data.get('pic')
            user.profile.aadhar=forms.cleaned_data.get('aadhar')
            user.profile.sponsorid=sponsorid
            user.save()
            return HttpResponseRedirect('/home')
            
    else:
        forms=ProfileForm(instance=user,initial={'occupation':user.profile.occupation,
                                                'location': user.profile.location,
                                                'pic':user.profile.pic,
                                                'aadhar':user.profile.aadhar
                                                
                                                })
    return render(request, 'profile.html',{'forms':forms,'jks':jks})

@login_required
def password(request):
    user=request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password=form.cleaned_data['old_password']
            if user.check_password(old_password):
                new_password=form.cleaned_data['new_password']
                confirm_password=form.cleaned_data['confirm_password']
                if new_password==confirm_password:
                    user.set_password(new_password)
                    user.save()
                else:
                    messages.success(request, 'Password does not match.')
            else:
                messages.success(request, 'Enter correct password')    
            return HttpResponseRedirect('/password')

    else:
        form = ChangePasswordForm()
    return render(request,'password.html',{'form':form})

def resetpassword(request,k,d):
    user=User.objects.get(username=k)
    try:
        if resetpass.objects.get(Q(serialid=d)&Q(user=k)):
            if request.method == "POST":
                form = resetpasswordForm(request.POST)
                if form.is_valid():
                    new_password=form.cleaned_data['new_password']
                    confirm_password=form.cleaned_data['confirm_password']
                    if new_password==confirm_password:
                        user.set_password(form.cleaned_data['new_password'])
                        user.save()
                    else:
                        messages.success(request, 'Password does not match.')
                        return HttpResponseRedirect('/resetpass/%s/%s'%(k,d))
                    return HttpResponseRedirect('/login')

            else:
                form = resetpasswordForm()
            return render(request,'resetpass.html',{'form':form})
    except:
        messages.success(request, 'Check your mail and go to that link.')
        return render(request,'resetpass.html')

def forgot(request):
    if request.method == "POST":
        form = resetpassform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            email=form.cleaned_data['email']
            jks=date.today()
            try:
                user = User.objects.get(Q(email=email)&Q(username=username))
                form.save()
                for s in resetpass.objects.filter(Q(email=email)&Q(user=username)&Q(serialid__isnull=True)):
                    s.serialid=random.randint(99,999)
                    if resetpass.objects.filter(Q(serialid=s.serialid)):
                        continue
                    else:
                        s.save()
                    html_content="http://127.0.0.1:8000/resetpass/%s/%s/"%(s.user,s.serialid)
                    notification="Change Password/Forgot Password"
                    send_mail('Forgot Password',html_content, settings.EMAIL_HOST_USER,[email],fail_silently=False)
                messages.success(request, 'Check your mail & Click on the link.')
                return HttpResponseRedirect('/forgot')
            except:
                messages.success(request, 'Credentials do not match with each other.')
                return render(request,'forgot.html')
    else:
        form = resetpassform()
    return render(request,'forgot.html',{'form':form})

def authordetails(request,d):
    n=User.objects.get(Q(username=d) | Q(first_name=d))
    return render(request,'modal2.html',{'data':n})

@login_required
def qtycart(request,isbn):
    if request.method == "POST":
        forms=cartform(request.POST)
        if forms.is_valid():
            n=cart.objects.get(Q(fkbook__isbn=isbn) & Q(name=request.user.first_name)&Q(Purchasedate=None))
            n.qty=forms.cleaned_data['qty']
            if n.qty<1:
                messages.success(request,'Enter a valid quantity.')
                return HttpResponseRedirect('/mycart')
            else:
                n.fkbook.total=(n.qty)*(n.fkbook.price)
                n.price= n.fkbook.total
                n.save()
                prod=cart.objects.filter(Q(name=request.user.first_name)&Q(Purchasedate=None))
                j=book.objects.all()
                return render(request,'mycart.html',{'cart':prod,'n':j})
        
@login_required   
def mycart(request):
    prod=cart.objects.filter(Q(name=request.user.first_name)&Q(Purchasedate=None))
    for i in cart.objects.filter(Q(name=request.user.first_name)&Q(Purchasedate=None)):
        if i.fkbook.stock<1:
            messages.success(request, '%s is Out of stock.'%i.fkbook.title)
            i.delete()
    n=book.objects.all()
    jks=Profile.objects.get(user=request.user)
    print jks.wallet
    return render(request,'mycart.html',{'cart':prod,'n':n,'jks':jks})

@login_required    
def delmycart(request,d):
    user=request.user.first_name
    prod=cart.objects.get(id=d)
    prod.delete()
    return HttpResponseRedirect('/mycart')

@login_required
def emptycart(request,d):
    prod=cart.objects.filter(name=request.user.first_name)
    prod.delete()
    return HttpResponseRedirect('/store')
    
@login_required
def ship(request):
    
        #insert into invoice values(t.name=s.name, t.qty=s.qty, t.stock=s.stock, t.bookisbn=s.fkbook.isbn)
            
            
    print datetime.date.today()
    if request.user.is_authenticated():
        try:
            add=Shipping.objects.filter(username__icontains=request.user)
            print add
            if request.method=='POST':
                forms = shipform(request.POST, instance=add)
                if forms.is_valid():
                    
                    ship = forms.save(commit=False)
                    ship.username=request.user
                    ship.user = request.user
                    ship =ship.save()
                    return HttpResponseRedirect('/check')   
            elif Shipping.objects.filter(username__icontains=request.user):
                return render(request,'Ship.html',{'item':Shipping.objects.filter(username__icontains=request.user),'forms':shipform()})
            else:
                items=Shipping.objects.get(username__icontains=request.user)
                forms=shipform(initial={'name': items.name,'address':items.address,'mob':items.mob,'pincode':items.pincode,'state':items.state}) 
                return render(request,'Ship.html',{'forms':forms})
                
        except:
            if request.method=='POST':
                forms = shipform(request.POST)
                if forms.is_valid():
                    
                    ship = forms.save(commit=False)
                    ship.user = request.user
                    ship.username=request.user
                    ship =ship.save()
                    
                    return HttpResponseRedirect('/check')
            else:
                forms=shipform()
                return render(request,'Ship.html',{'forms':forms})
    else:
        return render(request,'login.html')

def deleteadd(request,d):
    address=Shipping.objects.filter(Q(id=d)&Q(username=request.user))
    address.delete()
    return HttpResponseRedirect('/check')
        
@login_required
def invoice(request):
    
    if request.user:
        dravid=cart.objects.latest('orderno')
            
        jks=dravid.orderno+1
        for s in cart.objects.filter(Q(name=request.user.first_name)&Q(Purchasedate__isnull=True)):
            s.Purchasedate=datetime.datetime.now()
            s.orderno=jks
            print s.orderno
            s.save()

        
        
       
        n=cart.objects.filter(orderno=jks)
        z=Selectadd.objects.filter(name=request.user.username).last()
        j=Shipping.objects.get(id=z.select)
        for k in cart.objects.filter(orderno=jks):
            for i in book.objects.filter(isbn=k.fkbook.isbn):
                i.stock=i.stock-k.qty
                i.save()
                
        html_content="Your order no is %s \n\nShipping address: %s, %s, \n\nMobile No. %s, Payment %s\n\nInvoice: http://127.0.0.1:8000/%s\n\nContact Us: info@bbtpoint.com"%(jks, j.address, j.pincode, j.mob, z.payment, jks)
        notification="Name: %s %s,   Order no is %s     Shipping address: %s, %s,   Mobile No. %s, Payment %s"%(request.user.first_name, request.user.last_name,jks, j.address, j.pincode, j.mob, z.payment)
        send_mail('Order Confirmation',html_content, settings.EMAIL_HOST_USER,[request.user.email],fail_silently=False)
        send_mail('Order Confirmation',notification, settings.EMAIL_HOST_USER,['info@bbtpoint.com'],fail_silently=False)
        return render(request,'invoice.html',{'n':n,'j':j,'z':z})
        pyautogui.hotkey('ctrl', 'p')
    else:
        return HttpResponse('Error 404 PageNotFound')
        

    
    
    
    
    

def bauthordet(request,d):
    try:
        author=bookauthor.objects.get(name__icontains=d)
        return render(request,'bauthor.html',{'author':author})
    except:
        return HttpResponse('Details not exist in our database.')

@login_required
def terms(request,d):
    s = Selectadd(name=request.user,select=d)
    s.save()
    pin = Shipping.objects.get(id=d)
    return render(request,'T&C.html',{'pin':pin,'d':d})

def cod(request,d):
    z=Selectadd.objects.filter(name=request.user.username).last()
    z.payment='Cash On Delivery'
    z.save()
    pin = Shipping.objects.get(id=d)
    
    return render(request,'cod.html',{'pin':pin})


@login_required
def orders(request):
    
    order=cart.objects.filter(name=request.user.first_name, orderno__isnull=False).order_by('-Purchasedate')
    return render(request,'myorders.html',{'order':order})

@login_required
def myinvoices(request, d):
    inv=cart.objects.filter(Q(orderno=d)&Q(name=request.user.first_name))
    if inv:
        return render(request,'oldinvoice.html',{'inv':inv})
        
        
    else:
        messages.error(request, 'No order exist with this order no.')
        return HttpResponseRedirect('/orders')
        

def quickview(request, d):
    qv=book.objects.get(isbn=d)
    return render(request,'modal.html',{'qv':qv})
        
    


