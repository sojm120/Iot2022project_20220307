from django.contrib import admin

from web.models import Cust, Cate, Rest, Review, Imgpath, Board, Menu


class CustAdmin(admin.ModelAdmin):
    list_display = ('id', 'pwd', 'name', 'birth', 'gender', 'email', 'address', 'phone', 'host_flag')


admin.site.register(Cust, CustAdmin)


class CateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Cate, CateAdmin)


class RestAdmin(admin.ModelAdmin):
    list_display = ('id', 'cust_id', 'cate_id', 'rest_name', 'reg_num', 'host_name', 'address',
                    'restindex', 'phone', 'openhour', 'breakhour', 'restimg')


admin.site.register(Rest, RestAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'rest_id', 'cust_id', 'title', 'content', 'regdate',
                    's_rating', 'm_rating', 'p_rating', 'menu', 'number', 'purpose')


admin.site.register(Review, ReviewAdmin)


class ImgpathAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_id', 'path')


admin.site.register(Imgpath, ImgpathAdmin)


class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'cust_id', 'title', 'content')


admin.site.register(Board, BoardAdmin)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'rest_id', 'name', 'price', 'menuimg')


admin.site.register(Menu, MenuAdmin)