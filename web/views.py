import logging
import json

import cust as cust
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
from web.models import Cust

@request_mapping("")
class MyView(View):
# home
    @request_mapping("/", method="get")
    def home(self,request):
        return render(request,'home.html');


# iot 장비에서 요청
    @request_mapping("/iot", method="get")
    def iot(self, request):
        id = request.GET['id'];
        temp = request.GET['temp'];
        el = request.GET['el'];
        # -------------------------------------------
        el_logger = logging.getLogger('el_file');
        el_logger.debug(id + ',' + temp + ',' + el);
        # -------------------------------------------
        return render(request, 'ok.html');

    # login
    @request_mapping("/login", method="get")
    def login(self,request):
        context = {
            'center': 'login.html'
        }
        return render(request, 'home.html', context);

    @request_mapping("/logout", method="get")
    def logout(self, request):
        if request.session['sessionid'] != None:
            del request.session['sessionid']
        return render(request, 'home.html');

    @request_mapping("/register", method="get")
    def register(self,request):
        context = {
            'center': 'register.html'
        }
        return render(request, 'home.html', context);

    @request_mapping("/loginimpl", method="post") #method는 post로 변경
    def loginimpl(self, request):
        #id와 pwd를 확인한다.
        id = request.POST['id'];
        pwd = request.POST['pwd'];
        #id를 이용하여 db에 사용자 정보 조회
        #id가 존재하면 pwd 검사
        #pwd가 틀리면 실패
        #pwd가 맞으면 성공
        context = {};

        try:
            cust = Cust.objects.get(id=id);
            if cust.pwd == pwd:
                request.session['sessionid'] = cust.id;
                request.session['sessionname'] = cust.name;
                context['center'] = 'loginok.html';
                # context['rid'] = id
            else:
                raise Exception;
        except:
            context['center'] = 'loginfail.html';

        return render(request, 'home.html', context);

# page

    @request_mapping("/registerimpl", method="post")
    def registerimpl(self, request):
        id = request.POST['id'];
        pwd = request.POST['pwd'];
        name = request.POST['name'];
        context = {};
        try:
            Cust.objects.get(id=id);
            context['center'] = 'registerfail.html'  # 입력한 id가 없거나, 빈칸이면
        except:
            Cust(id=id, pwd=pwd, name=name).save();
            context['center'] = 'registerok.html'
            context['rname'] = name

        return render(request, 'home.html', context);


    @request_mapping("/geo", method="get")
    def geo(self, request):
        context = {
            'center': 'geo.html'
        };
        return render(request, 'home.html', context);


    @request_mapping("/geo2", method="get")
    def geo2(self, request):
        context = {
            'center': 'geo2.html'
        };
        return render(request, 'home.html', context);

        # iot 장비에서 요청
    @request_mapping("/ajax", method="get")
    def ajax(self, request):
        context = {
            'center': 'ajax.html'
        };
        return render(request, 'home.html', context);

    @request_mapping("/ajaximpl", method="get")
    def ajaximpl(self, request):
        data = [];
        for i in range(1, 10):
            dic = {};
            dic['id'] = 'id' + str(i);
            dic['name'] = 'james' + str(i);
            dic['age'] = i;
            data.append(dic);
        return HttpResponse(json.dumps(data), content_type='application/json')


    @request_mapping("/geoimpl", method="get")
    def geoimpl(self, request):
        data = []

        dic1 = {}
        dic1['content'] = '<div>kakao</div>'
        dic1['lat'] = 35.085971
        dic1['lng'] = 129.032359
        dic1['target'] = 'http://www.naver.com'
        data.append(dic1)

        dic2 = {}
        dic2['content'] = '<div>googlegoogle</div>'
        dic2['lat'] = 35.09
        dic2['lng'] = 129.025359
        dic2['target'] = 'http://www.google.com'
        data.append(dic2)

        dic3 = {}
        dic3['content'] = '<div>daumdaum</div>'
        dic3['lat'] = 35.081971
        dic3['lng'] = 129.04
        dic3['target'] = 'http://www.daum.net'
        data.append(dic3)

        dic4 = {}
        dic4['content'] = '<div>msnmsn</div>'
        dic4['lat'] = 35.1
        dic4['lng'] = 129.1
        dic4['target'] = 'http://www.msn.com'
        data.append(dic4)

        return HttpResponse(json.dumps(data), content_type='application/json')


    # chart
    @request_mapping("/chart1", method="get")
    def chart1(self,request):
        context = {
            'center': 'chart1.html'
        }
        return render(request, 'home.html', context);

    # chart
    @request_mapping("/chart1impl", method="get")
    def chart1impl(self,request):
        data = [];
        content1 = {};
        content2 = {};

        content1['name'] = 'Installation';
        content1['data'] = [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175];
        data.append(content1);

        content2['name'] = 'Manufacturing';
        content2['data'] = [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434];
        data.append(content2);

        # content1['name'] = 'Project Developmen';
        # content1['data'] = [null, null, 7988, 12169, 15112, 22452, 34400, 34227];
        # data.append(content1);
        #
        # content1['name'] = 'Other';
        # content1['data'] = [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111];
        # data.append(content1);
        # data.append(content1);
        # data.append(content2);

        return HttpResponse(json.dumps(data), content_type='application/json')


        # try:
        #     con = Db().getConnection();
        #     cursor = con.cursor();
        #     cursor.execute(Sql.cartavg);
        #     result = cursor.fetchall();
        #     for o in result:
        #         print(o[0])
        # except:
        #     print('Error');
        # finally:
        #     Db().close(con, cursor)



from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django_request_mapping import request_mapping
import json

from web.models import Rest, Review, Menu, Imgpath, Cate, Cust
from config.settings import UPLOAD_DIR

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
    def search(self, request):
        return render(request, 'search.html');

    @request_mapping("/login", method="get")
    def login(self, request):
        return render(request, 'login.html');

    @request_mapping("/restDetail", method="get")
    def restDetail(self, request):
        # home에서 클릭한 id 가져오기
        rest = Rest.objects.get(id=1);
        star_avg = Review.objects.filter(rest=1).aggregate(s_avg=Avg('s_rating'), m_avg=Avg('m_rating'),
                                                           p_avg=Avg('p_rating'));
        menu = Menu.objects.filter(rest=1);
        review = Review.objects.filter(rest=1).order_by('-id');  # 내림차순 정렬
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

        print(id, pwd, name, birth, gender, email, address1 + address2, phone, host_flag);
        context = {};
        try:
            Cust.objects.get(id=id);
            context['center'] = 'register.html';
        except:
            Cust(id=id, pwd=pwd, name=name, birth=birth, gender=gender, email=email, address=address1 + address2,
                 phone=phone, host_flag=host_flag).save();
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

    # def rest_list(request):
    #     paginate_by = 15
    #     context = {}
    #
    #     context['is_paginated'] = True
    #     rest = Rest.objects.all()
    #     paginator = Paginator(rest, paginate_by)
    #     page_number_range = 8
    #     current_page = int(request.GET.get('page', 1))
    #     context['current_page'] = current_page
    #
    #     start_index = int((current_page - 1) / page_number_range) * page_number_range
    #     end_index = start_index + page_number_range
    #
    #     current_page_group_page = paginator.page_range[start_index: end_index]
    #     print("current_page_group_page", current_page_group_page)
    #
    #     start_page = paginator.page(current_page_group_page[0])
    #     end_page = paginator.page(current_page_group_page[-1])
    #
    #     has_previous_page = start_page.has_previous()
    #     has_next_page = end_page.has_next()
    #
    #     context['current_page_group_range'] = current_page_group_page
    #     if has_previous_page:
    #         context['has_previous_page'] = has_previous_page
    #         context['previous_page'] = start_page.previous_page_number
    #
    #     if has_next_page:
    #         context['has_next_page'] = has_next_page
    #         context['next_page'] = end_page.next_page_number
    #
    #     e = paginate_by * current_page
    #     s = e - paginate_by
    #     print("내용 index", s, e)
    #     rest_list = Rest.objects.all()[s:e]
    #
    #     # 태그리스트
    #     tag_list = Cate.objects.all()
    #     context['tag_list'] = tag_list
    #
    #     # 별점순
    #     star_rating = []
    #     for rest in rest_list:
    #         max_rating = [Review.s_rating]
    #         max_rating = max([p for p in max_rating if p is not 0])
    #         star_rating.append(max_rating)
    #
    #     context['rest_highest_rating'] = zip(rest_list, star_rating)
    #
    #     return render(request, 'search.html', context)
    #
    # def rest_search(request):
    #     paginate_by = 15
    #     context = {}
    #     rest_list = Rest.objects.all()
    #
    #     b = request.GET.get('b', '')
    #     f = request.GET.getlist('f')
    #     rating = request.GET.get('rating', '')
    #     print(rating)
    #
    #     if b:
    #         print(b)
    #         rest_list = rest_list.filter(Q(rest_name__icontains=b) | Q(name__icontains=b))
    #     if f:
    #         print(f)
    #         query = Q()
    #         for i in f:
    #             query = query | Q(name__icontains=i)
    #             rest_list = rest_list.filter(query)
    #
    #     if rating == 0:
    #         rest_list = rest_list.filter(rating__gt=0)
    #     elif rating == 1:
    #         rest_list = rest_list.filter(rating__lte=1)
    #     elif rating == 2:
    #         rest_list = rest_list.filter(rating__lte=2)
    #     elif rating == 3:
    #         rest_list = rest_list.filter(rating__lte=3)
    #     elif rating == 4:
    #         rest_list = rest_list.filter(rating__lte=4)
    #     else:
    #         rest_list = rest_list.filter(rating__gt=5)
    #
    #
    #     context['is_paginated'] = True
    #     paginator = Paginator(rest_list, paginate_by)
    #     page_number_range = 8
    #     current_page = int(request.GET.get('page', 1))
    #     context['current_page'] = current_page
    #
    #     start_index = int((current_page - 1) / page_number_range) * page_number_range
    #     end_index = start_index + page_number_range
    #
    #     current_page_group_page = paginator.page_range[start_index: end_index]
    #     print("current_page_group_page", current_page_group_page)
    #
    #     start_page = paginator.page(current_page_group_page[0])
    #     end_page = paginator.page(current_page_group_page[-1])
    #
    #     has_previous_page = start_page.has_previous()
    #     has_next_page = end_page.has_next()
    #
    #     context['current_page_group_range'] = current_page_group_page
    #     if has_previous_page:
    #         context['has_previous_page'] = has_previous_page
    #         context['previous_page'] = start_page.previous_page_number
    #
    #     if has_next_page:
    #         context['has_next_page'] = has_next_page
    #         context['next_page'] = end_page.next_page_number
    #
    #     e = paginate_by * current_page
    #     s = e - paginate_by
    #     print("내용 index", s, e)
    #     rest_list = Rest.objects.all()[s:e]
    #
    #     # 태그리스트
    #     tag_list = Cate.objects.all()
    #     context['tag_list'] = tag_list
    #
    #     # 별점순
    #     star_rating = []
    #     for rest in rest_list:
    #         max_rating = [Review.s_rating]
    #         max_rating = max([p for p in max_rating if p is not 0])
    #         star_rating.append(max_rating)
    #
    #     context['rest_highest_rating'] = zip(rest_list, star_rating)
    #
    #     return render(request, 'search.html', context)
    @request_mapping("/post_list", method="get")
    def post_list(request):
        rest = Rest.objects.all()
        q = request.GET.get('q', '')
        if q:
            rest = rest.filter(rest_name__icontains=q)
        context = {
            'rest': rest,
            'q': q

        }
        return render(request, 'search.html', context)


