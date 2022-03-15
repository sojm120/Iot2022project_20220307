from django.db.models import Avg
from django.shortcuts import render, redirect
from django.views import View
from django_request_mapping import request_mapping

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
        review = Review.objects.filter(rest=1);
        imgpath = Imgpath.objects.all();
        context = {
            'rest': rest,
            'star_avg': star_avg,
            'menu': menu,
            'review': review,
            'imgpath': imgpath
        };
        return render(request, 'restDetail.html', context);

    @request_mapping("/reviewreg", method="get")
    def reviewreg(self, request):
        return render(request, 'reviewreg.html');

    @request_mapping("/restEdit/<int:pk>", method="get")
    def restEdit(self, request, pk):
        rest = Rest.objects.get(id=pk);
        menu = Menu.objects.filter(rest=1);
        context = {
            'rest': rest,
            'menu': menu
        };
        return render(request, 'restEdit.html', context);

    @request_mapping("/restEdit/u", method="get")
    def restEditU(self, request):
        id = request.GET['id'];
        rest_name = request.GET['rest_name'];
        phone = request.GET['phone'];
        cate_id = request.GET['cate_id'];
        openhour = request.GET['openhour'];
        breakhour = request.GET['breakhour'];
        restindex = request.GET['restindex'];
        address = request.GET['address'];

        rest = Rest.objects.get(id=id);
        rest.rest_name = rest_name;
        rest.phone = phone;
        rest.cate_id = cate_id;
        rest.openhour = openhour;
        rest.breakhour = breakhour;
        rest.restindex = restindex;
        rest.address = address;
        rest.save()

        # menu = Menu.objects.filter(rest=1, );
        # menu_name = request.GET['menu_name'];
        # menu_price = request.GET['menu_price'];
        #
        # if 'img' in request.FILES:
        #     for img in request.FILES.getlist('img'):
        #         imgname = img._name
        #
        #         f = open('%s/%s' % (UPLOAD_DIR, imgname), 'wb')
        #         for chunk in img.chunks():
        #             f.write(chunk)
        #             f.close()
        #
        #         obj2 = Imgpath(review=obj1, path=imgname)
        #         obj2.save()
        return redirect('/restDetail')

    @request_mapping("/restEdit/menu/<int:pk>", method="get")
    def menu(self, request, pk):
        menu = Menu.objects.get(id=pk);
        context = {
            'menu': menu
        };
        return render(request, 'menu.html', context);

    @request_mapping("/restEdit/menu/d/<int:pk>", method="get")
    def menudelete(self, request, pk):
        obj = Menu.objects.get(id=pk);
        rest = obj.rest.id
        obj.delete();
        return redirect('/restEdit/'+str(rest));

    @request_mapping("/restEdit/menu/uv/<int:pk>", method="get")
    def menuUpdateveiw(self, request, pk):
        menu = Menu.objects.get(id=pk);
        context = {
            'center': 'guest/update.html',
            'menu': menu
        };
        return render(request, 'menuUpdate.html', context);

    @request_mapping("/restEdit/menu/u", method="get")
    def menuUpdate(self, request):
        name = request.GET['name'];
        price = request.GET['price'];
        id = request.GET['id'];
        obj = Menu.objects.get(id=id);
        rest = obj.rest.id
        obj.name = name;
        obj.price = price;
        obj.save();
        return redirect('/restEdit/'+str(rest));

    @request_mapping("/restEdit/menu/iv/<int:pk>", method="get")
    def menuInsertview(self, request, pk):
        rest = Rest.objects.get(id=pk);
        context = {
            'rest': rest
        };
        return render(request, 'menuInsert.html', context);

    @request_mapping("/restEdit/menu/i/<int:pk>", method="get")
    def menuInsert(self, request, pk):
        name = request.GET['name'];
        price = request.GET['price'];
        obj = Menu.objects.get(id=pk);
        rest = obj.rest.id
        obj = Menu(name=name, price=price, rest=obj.rest);
        obj.save();
        return redirect('/restEdit/'+str(rest));

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