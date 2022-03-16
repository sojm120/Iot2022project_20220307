from django.db.models import Avg
from django.shortcuts import render, redirect
from django.views import View
from django_request_mapping import request_mapping

from web.models import Cust

from config.settings import UPLOAD_DIR
from web.models import Rest, Review, Menu, Imgpath



@request_mapping("")
class MyView(View):

    @request_mapping("/", method="get")
    def home(self,request):
        return render(request, 'home.html');

    @request_mapping("/search", method="get")
    def search(self,request):
        return render(request, 'search.html');

    @request_mapping("/login", method="get")
    def login(self, request):
        return render(request, 'login.html');

    @request_mapping("/restDetail", method="get")
    def restDetail(self, request):
        # home에서 클릭한 id 가져오기
        rest = Rest.objects.get(id=1);
        star_avg = Review.objects.filter(rest=1).aggregate(s_avg=Avg('s_rating'), m_avg=Avg('m_rating'), p_avg=Avg('p_rating'));
        menu = Menu.objects.filter(rest=1);
        review = Review.objects.filter(rest=1).order_by('-id'); # 내림차순 정렬
        imgpath = Imgpath.objects.all();
        context = {
            'rest': rest,
            'star_avg': star_avg,
            'menu': menu,
            'review': review,
            'imgpath': imgpath,
            'reviewlist': 'reviewlist.html'
        };
        return render(request, 'restDetail.html', context);

    @request_mapping("/list", method="get")
    def list(self, request):
        return render(request, 'list.html');

    @request_mapping("/view", method="get")
    def view(self, request):
        return render(request, 'view.html');

    @request_mapping("/write", method="get")
    def write(self, request):
        return render(request, 'write.html');

    @request_mapping("/edit", method="get")
    def edit(self, request):
        return render(request, 'edit.html');

    @request_mapping("/register", method="get")
    def register(self, request):
        return render(request, 'register.html');

    @request_mapping("/profile", method="get")
    def profile(self, request):
        return render(request, 'profile.html');

    @request_mapping("/profileupdate", method="get")
    def profileupdate(self, request):
        return render(request, 'profileupdate.html');

    @request_mapping("/ownerupdate", method="get")
    def ownerupdate(self, request):
        return render(request, 'ownerupdate.html');

    @request_mapping("/registerimpl", method="post")
    def registerimpl(self, request):
        id = request.POST['custid'];
        pwd = request.POST['custpw'];
        name = request.POST['custname'];
        birth = request.POST['birth'];
        gender = request.POST['gender'];
        email = request.POST['custemail'];
        address1 = request.POST['address1'];
        address2 = request.POST['address2'];
        phone = request.POST['custphone'];
        host_flag = int(request.POST['host_flag']);

        print(id,pwd,name,birth,gender,email,address1+ address2,phone,host_flag);
        context = {};
        try:
            Cust.objects.get(id = id);
            context['center'] = 'register.html';
        except:
            Cust(id=id, pwd=pwd, name=name, birth=birth, gender=gender, email=email, address=address1+address2, phone=phone, host_flag=host_flag).save();
            context['center'] = 'registerok.html';
            context['rname'] = name;
        return render(request, 'home.html', context);

    @request_mapping("/loginimpl", method="post")
    def loginimpl(self, request):
        # id, pwd 를 프로그램을 확인 한다.
        id = request.POST['custid'];
        pwd = request.POST['custpw'];
        context = {};
        try:
            cust = Cust.objects.get(id=id);
            if cust.pwd == pwd:
                request.session['sessionid'] = cust.id;
                request.session['sessionname'] = cust.name;
                context['center'] = 'loginok.html';
            else:
                raise Exception;
        except:
            context['center'] = 'loginfail.html';

        return render(request, 'home.html', context);

    @request_mapping("/logout", method="get")
    def logout(self, request):
        if request.session['sessionid'] != None:
            del request.session['sessionid'];
        return render(request, 'home.html');

    @request_mapping("/faq", method="get")
    def faq(self, request):
        return render(request, 'faq.html');
