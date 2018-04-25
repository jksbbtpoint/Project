from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(book)
admin.site.register(blog)
admin.site.register(comment)
admin.site.register(cart)
admin.site.register(invoice)
admin.site.register(Shipping)
admin.site.register(bookauthor)
admin.site.register(preimg)
admin.site.register(likesonpost)
admin.site.register(returnbook)
admin.site.register(donate)
admin.site.register(verify)
admin.site.register(resetpass)
admin.site.register(Selectadd)
