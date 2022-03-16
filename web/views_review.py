from django.shortcuts import render, redirect
from django.views import View
from django_request_mapping import request_mapping

from config.settings import UPLOAD_DIR
from web.models import Review, Imgpath


@request_mapping("/review")
class ReviewView(View):

    @request_mapping("/i", method="post")
    def insert(self, request):
        rest = 1
        cust = "id01"
        title = request.POST['title']
        content = request.POST['content']
        s_rating = request.POST['s_rating']
        m_rating = request.POST['m_rating']
        p_rating = request.POST['p_rating']
        menu = request.POST['menu']
        if request.POST['number'] is not '':
            number = request.POST['number']
        else:
            number = 0
        purpose = request.POST['purpose']

        obj1 = Review(rest_id=rest, cust_id=cust, title=title, content=content, s_rating=s_rating,
                      m_rating=m_rating, p_rating=p_rating, menu=menu, number=number, purpose=purpose)
        obj1.save()

        if 'img' in request.FILES:
            for img in request.FILES.getlist('img'):
                imgname = img._name

                f = open('%s/%s' % (UPLOAD_DIR, imgname), 'wb')
                for chunk in img.chunks():
                    f.write(chunk)
                    f.close()

                obj2 = Imgpath(review=obj1, path=imgname)
                obj2.save()
        return redirect('/restDetail')

    @request_mapping("/uv/", method="get")
    def updateview(self, request):
        # 추후에 url에 id 받아서 데이터 받는 것으로 수정
        obj1 = Review.objects.get(id=20)
        obj2 = []
        for obj in Imgpath.objects.filter(review=obj1):
            obj2.append(obj)
        # print(obj2)
        context = {
            'obj1': obj1,
            'obj2': obj2
        }
        return render(request, 'reviewupdate.html', context)

    @request_mapping("/u", method="post")
    def update(self, request):
        id = request.POST['id']
        title = request.POST['title']
        content = request.POST['content']
        s_rating = request.POST['s_rating']
        m_rating = request.POST['m_rating']
        p_rating = request.POST['p_rating']
        menu = request.POST['menu']
        if request.POST['number'] is not '':
            number = request.POST['number']
        else:
            number = 0
        purpose = request.POST['purpose']

        obj1 = Review.objects.get(id=id)
        obj1.title = title
        obj1.content = content
        obj1.s_rating = s_rating
        obj1.m_rating = m_rating
        obj1.p_rating = p_rating
        obj1.menu = menu
        obj1.number = number
        obj1.purpose = purpose

        obj1.save()

        # 사진 파일 : img1_flag, img2_flag를 파일존재 여부 flag로 사용
        # 1. flag=1 일 때,
        #   (1) 파일o: -변경 or -추가
        #   (2) 파일x: 기존사진 유지(아무 것도 안 해줘도 됨)
        # 2. flag=0 일 때,
        #   (1) 파일o: 불가능(아무 것도 안 해줘도 됨)
        #   (2) 파일x: -기존사진 삭제 or -사진없음(아무 것도 안 해줘도 됨)
        img1_flag = request.POST['img1_flag']
        imgpath_id1 = request.POST['imgpath_id1']
        if img1_flag == '1':
            if 'img1' in request.FILES:
                img1 = request.FILES['img1']
                img1name = img1._name

                f = open('%s/%s' % (UPLOAD_DIR, img1name), 'wb')
                for chunk in img1.chunks():
                    f.write(chunk)
                    f.close()

                if imgpath_id1 != '0':
                    obj2 = Imgpath.objects.get(id=imgpath_id1)
                    obj2.path = img1name
                else:
                    obj2 = Imgpath(review=obj1, path=img1name)
                obj2.save()
        elif img1_flag == '0':
            if imgpath_id1:
                obj2 = Imgpath.objects.get(id=imgpath_id1)
                obj2.delete()

        img2_flag = request.POST['img2_flag']
        imgpath_id2 = request.POST['imgpath_id2']
        if img2_flag == '1':
            if 'img2' in request.FILES:
                print("img2 exists")
                img2 = request.FILES['img2']
                img2name = img2._name

                f = open('%s/%s' % (UPLOAD_DIR, img2name), 'wb')
                for chunk in img2.chunks():
                    f.write(chunk)
                    f.close()

                if imgpath_id2 != '0':
                    obj2 = Imgpath.objects.get(id=imgpath_id2)
                    obj2.path = img2name
                else:
                    obj2 = Imgpath(review=obj1, path=img2name)
                obj2.save()
        elif img2_flag == '0':
            if imgpath_id2:
                obj2 = Imgpath.objects.get(id=imgpath_id2)
                obj2.delete()
        return redirect('/restDetail')
