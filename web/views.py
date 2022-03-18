import json
import logging

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django_request_mapping import request_mapping

from web.models import Cust, Board

from config.settings import UPLOAD_DIR
from web.models import Rest, Review, Menu, Imgpath



@request_mapping("")
class MyView(View):

    @request_mapping("/", method="get")
    def home(self, request):
        rest = Rest.objects.all();
        star_rating = Review.objects.all();
        imgpath = Imgpath.objects.all();
        context = {
            'rest': rest,
            'star_rating': star_rating,
            'imgpath': imgpath
        };
        return render(request, 'home.html', context);

    @request_mapping("/search", method="get")
    def search(self,request):
        return render(request, 'search.html');

    @request_mapping("/login", method="get")
    def login(self, request):
        return render(request, 'login.html');

    @request_mapping("/restDetail/<int:pk>", method="get")
    def restDetail(self, request, pk):
        # home에서 클릭한 id 가져오기
        rest = Rest.objects.get(id=pk);
        star_avg = Review.objects.filter(rest=pk).aggregate(s_avg=Avg('s_rating'), m_avg=Avg('m_rating'),
                                                           p_avg=Avg('p_rating'));
        menu = Menu.objects.filter(rest=pk);
        review = Review.objects.filter(rest=pk).order_by('-id');  # 내림차순 정렬
        imgpath = Imgpath.objects.all();
        cust = Cust.objects.get(id=request.session['sessionid']);
        context = {
            'rest': rest,
            'cust': cust,
            'star_avg': star_avg,
            'menu': menu,
            'review': review,
            'imgpath': imgpath,
            'reviewlist': 'reviewlist.html'
        };
        return render(request, 'restDetail.html', context);

    @request_mapping("/register", method="get")
    def register(self, request):
        return render(request, 'register.html');

    @request_mapping("/profile/<str:pk>", method="get")
    def profile(self, request, pk):
        profile = Cust.objects.get(id=pk);
        try:
            Rest.objects.get(cust_id=pk);
            restprf = Rest.objects.get(cust_id=pk);
        except:
            restprf = '';
        context = {
            'Cust': profile,
            'Rest': restprf
        };
        return render(request, 'profile.html',context);

    @request_mapping("/profileupdate/<str:pk>", method="get")
    def profileupdate(self, request, pk):
        profile = Cust.objects.get(id=pk);
        restprf = Rest.objects.get(cust_id=pk);
        context = {
            'Cust': profile,
            'Rest': restprf
        };
        return render(request, 'profileupdate.html', context);

    @request_mapping("/profileupdateimpl/<str:pk>", method="post")
    def profileupdateimpl(self, request, pk):
        name = request.POST['name'];
        birth = request.POST['birth'];
        gender = request.POST['gender'];
        email = request.POST['email'];
        phone = request.POST['phone'];
        address = request.POST['address'];

        cust = Cust.objects.get(id=pk);
        cust.name = name;
        cust.birth = birth;
        cust.gender = gender;
        cust.email = email;
        cust.phone = phone;
        cust.address = address;
        cust.save()

        hrest = request.POST['hrest'];
        hname = request.POST['hname'];
        hreg = request.POST['hreg'];
        hphone = request.POST['hphone'];
        haddr = request.POST['haddr'];
        hopen = request.POST['hopen'];
        hbreak = request.POST['hbreak'];
        hindex = request.POST['hindex'];

        rest = Rest.objects.get(cust_id=pk)
        rest.rest_name = hrest;
        rest.host_name = hname;
        rest.reg_num = hreg;
        rest.phone = hphone;
        rest.address = haddr;
        rest.openhour = hopen;
        rest.breakhour = hbreak;
        rest.restindex = hindex;
        rest.save()

        return redirect('/profile/'+str(pk));


    @request_mapping("/registerimpl", method="post")
    def registerimpl(self, request):
        host_flag = int(request.POST['host_flag']);
        id = request.POST['custid'];
        pwd = request.POST['custpw'];
        name = request.POST['custname'];
        birth = request.POST['birth'];
        gender = request.POST['gender'];
        email = request.POST['custemail'];
        address1 = request.POST['address1'];
        address2 = request.POST['address2'];
        phone = request.POST['custphone'];
        imgname = '';
        if 'custimg' in request.FILES:
            img = request.FILES['custimg'];
            imgname = img._name;
            f = open('%s/%s' % (UPLOAD_DIR, imgname), 'wb')
            for chunk in img.chunks():
                f.write(chunk);
                f.close();
        profile = Cust(id=id, pwd=pwd, name=name, birth=birth, gender=gender, email=email,
                       address=address1 + address2,
                       phone=phone, host_flag=host_flag, custimg=imgname);
        profile.save();

        if host_flag==1:
            reg_num = request.POST['reg_num'];
            rest_name = request.POST['rest_name'];
            host_name = request.POST['host_name'];
            address3 = request.POST['address3'];
            address4 = request.POST['address4'];
            restindex = request.POST['restindex'];
            hostphone = request.POST['hostphone'];
            openhour = request.POST['openhour'];
            breakhour = request.POST['breakhour'];
            cate_id = request.POST['cate_id']
            imgname2 = '';

            if 'restimg' in request.FILES:
                img = request.FILES['restimg'];
                imgname2 = img._name;
                f = open('%s/%s' % (UPLOAD_DIR, imgname2), 'wb')
                for chunk in img.chunks():
                    f.write(chunk);
                    f.close();
            restprf = Rest(cust=profile, reg_num=reg_num, rest_name=rest_name, host_name=host_name, address=address3 + address4,
                            restindex=restindex, phone=hostphone, openhour=openhour, breakhour=breakhour, cate_id=cate_id, restimg=imgname2);
            restprf.save();
        return render(request, 'home.html');

    @request_mapping("/loginimpl", method="post")
    def loginimpl(self, request):
        # id, pwd 를 프로그램을 확인 한다.
        id = request.POST['custid'];
        pwd = request.POST['custpw'];
        try:
            cust = Cust.objects.get(id=id);
            if cust.pwd == pwd:
                request.session['sessionid'] = cust.id;
                request.session['sessionname'] = cust.name;
                request.session['sessionimg'] = cust.custimg;
            else:
                raise Exception;
        except:
            return redirect('/login');
        return redirect('/');


    @request_mapping("/logout", method="get")
    def logout(self, request):
        if request.session['sessionid'] != None:
            del request.session['sessionid'];
        return redirect('/');

    @request_mapping("/faq", method="get")
    def faq(self, request):
        return render(request, 'faq.html');

    @request_mapping("/live_chat", method="get")
    def live_chat(self, request):
        return render(request, 'live_chat.html');
