from django.db.models import Avg
from django.shortcuts import render, redirect
from django.views import View
from django_request_mapping import request_mapping

from config.settings import UPLOAD_DIR
from web.models import Rest, Review, Menu, Imgpath


@request_mapping("/restEdit")
class RestView(View):

    @request_mapping("/<int:pk>", method="get")
    def restEdit(self, request, pk):
        rest = Rest.objects.get(id=pk);
        menu = Menu.objects.filter(rest=1);
        context = {
            'rest': rest,
            'menu': menu
        };
        return render(request, 'restEdit.html', context);

    @request_mapping("/u", method="post")
    def restEditU(self, request):
        id = request.POST['id'];
        rest_name = request.POST['rest_name'];
        phone = request.POST['phone'];
        cate_id = request.POST['cate_id'];
        openhour = request.POST['openhour'];
        breakhour = request.POST['breakhour'];
        restindex = request.POST['restindex'];
        address = request.POST['address'];

        rest = Rest.objects.get(id=id);
        rest.rest_name = rest_name;
        rest.phone = phone;
        rest.cate_id = cate_id;
        rest.openhour = openhour;
        rest.breakhour = breakhour;
        rest.restindex = restindex;
        rest.address = address;
        rest.save()

        if 'img' in request.FILES:
            for img in request.FILES.getlist('img'):
                imgname = img._name

                f = open('%s/%s' % (UPLOAD_DIR, imgname), 'wb')
                for chunk in img.chunks():
                    f.write(chunk)
                    f.close()

                imgpath = rest.restimg;
                imgpath = imgname + ' ' + imgpath;
                rest.restimg = imgpath;
                rest.save()
        return redirect('/restDetail')

    @request_mapping("/delimg/<int:pk>", method="get")
    def delImg(self, request, pk):
        rest = Rest.objects.get(id=pk);
        imgpath = rest.restimg;
        path = imgpath.split(' ');
        del path[len(path)-1];
        imgpath = ' '.join(path);
        rest.restimg = imgpath;
        rest.save();
        return redirect('/restDetail')

    @request_mapping("/menu/<int:pk>", method="get")
    def menu(self, request, pk):
        menu = Menu.objects.get(id=pk);
        context = {
            'menu': menu
        };
        return render(request, 'menu.html', context);

    @request_mapping("/menu/d/<int:pk>", method="get")
    def menudelete(self, request, pk):
        obj = Menu.objects.get(id=pk);
        rest = obj.rest.id
        obj.delete();
        return redirect('/restEdit/'+str(rest));

    @request_mapping("/menu/uv/<int:pk>", method="get")
    def menuUpdateveiw(self, request, pk):
        menu = Menu.objects.get(id=pk);
        context = {
            'center': 'guest/update.html',
            'menu': menu
        };
        return render(request, 'menuUpdate.html', context);

    @request_mapping("/menu/u", method="get")
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

    @request_mapping("/menu/iv/<int:pk>", method="get")
    def menuInsertview(self, request, pk):
        rest = Rest.objects.get(id=pk);
        context = {
            'rest': rest
        };
        return render(request, 'menuInsert.html', context);

    @request_mapping("/menu/i/<int:pk>", method="get")
    def menuInsert(self, request, pk):
        name = request.GET['name'];
        price = request.GET['price'];
        obj = Menu.objects.get(id=pk);
        rest = obj.rest.id
        obj = Menu(name=name, price=price, rest=obj.rest);
        obj.save();
        return redirect('/restEdit/'+str(rest));