"""Books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from newbooks.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
    
    
    
    url(r'^admin/', admin.site.urls),
    url(r'^home/$',home),
    
    url(r'^cod/(\d+)/$',cod),
    url(r'^resetpass/([\w|\W]+)/([\w|\W]+)/$',resetpassword),
    url(r'^forgot/$',forgot),
    url(r'^$',home),
    url(r'^ret/(\d+)/(\d+)/$',ret),
    url(r'^deleteadd/(\d+)/$',deleteadd),
    url(r'^jks/$',jks),
    url(r'^login/$',login),
    url(r'^aboutus/$',aboutus),
    url(r'^books/$',books),
    url(r'^register/$',register,name='reg'),
    
    url(r'^auth_check/$',auth_view,name='check'),
    url(r'^logged_in/$',loggedin),
    url(r'^logout/$',logout),
    url(r'^sachin/$',addbook),
    url(r'^detail/(\d+)/$',det,name='detail'),
    url(r'^wpost/$',newpost),
    url(r'^allpost/$',allpost),
    url(r'^mypost/$',mypost),
    url(r'^authpost/([\w|\W]+)/$',authpost),
    url(r'^delete/(\d+)/$',delete),
    url(r'^delcomm/(\d+)/$',delcomm),
    url(r'^profile/$',user_profile),
    url(r'^password/$',password),
    url(r'^store/$',bstore),
    url(r'^catstore/([\w|\W]+)/$',catstore),
    url(r'^comm/([\w|\W]+)/$',com),
    url(r'^authdet/([\w|\W]+)/$',authordetails),
    url(r'^cart/([\w|\W]+)/$',add2cart),
    url(r'^qv/([\w|\W]+)/$',quickview),
    url(r'^like/([\w ]+)/$',likes),
    url(r'^likes/([\w|\W]+)/$',like),
    url(r'^det/(\d+)/$',det),
    url(r'^mycart/(\d+)/$',qtycart),
    url(r'^mycart/$',mycart),
    url(r'^del/(\d+)/$',delmycart),
    url(r'^check/$',ship),
    url(r'^bauth/([\w|\W]+)/$',bauthordet), #W for special character %
    url(r'^invoice/$',invoice),
    url(r'^search_query/$',search),
    url(r'^searchorder/$',searchorders),
    url(r'^T&C/(\d+)/$',terms),
    url(r'^(\d+)/$',myinvoices),
    url(r'^empty/([\w|\W]+)/$',emptycart),
    url(r'^orders/$',orders),
    url(r'^verifyem/$',verifyfun),
]+ static(settings.MEDIA_URL,
         document_root=settings.MEDIA_ROOT)
