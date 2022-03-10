from django.shortcuts import render, redirect
from django.views import View
from django_request_mapping import request_mapping

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

                # 파일 저장소 정해지면 주석 없애고 수정
                # f = open('%s/%s' % (UPLOAD_DIR, img1name), 'wb')
                # for chunk in img1.chunks():
                #     f.write(chunk);
                #     f.close();

                obj2 = Imgpath(review=obj1, path=imgname)
                obj2.save()
        return redirect('/restDetail')
