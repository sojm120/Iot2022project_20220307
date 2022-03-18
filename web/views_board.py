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


@request_mapping("/board")
class BoardView(View):

    @request_mapping("/", method="get")
    def board(self, request):
        count = Board.objects.all().count()
        context = {
            'count': count
        }
        return render(request, 'list.html', context)

    @request_mapping("/listview/<int:idx>/<int:getcnt>", method="get")
    def listview(self, request, idx, getcnt):
        objs = Board.objects.all().order_by('-id')[idx:idx+getcnt]
        data = []
        for obj in objs:
            datum = dict()
            datum['id'] = str(obj.id)
            datum['title'] = str(obj.title)
            datum['cust_id'] = str(obj.cust.id)
            datum['regdate'] = str(obj.regdate)
            data.append(datum)
        return HttpResponse(json.dumps(data), content_type='application/json')

    @request_mapping("/iv", method="get")
    def insertview(self, request):
        return render(request, 'boardreg.html')

    @request_mapping("/i", method="get")
    def insert(self, request):
        title = request.GET['title']
        content = request.GET['content']
        objs = Board(cust_id=request.session['sessionid'], title=title, content=content)
        objs.save()
        return redirect('/board')

    @request_mapping("/g/<int:pk>", method="get")
    def get(self, request, pk):
        objs = Board.objects.get(id=pk)
        context = {
            'objs': objs
        }
        return render(request, 'boardget.html', context)

    @request_mapping("/uv/<int:pk>", method="get")
    def updateview(self, request, pk):
        objs = Board.objects.get(id=pk)
        context = {
            'objs': objs
        }
        return render(request, 'boardupdate.html', context)

    @request_mapping("/u/<int:pk>", method="get")
    def update(self, request, pk):
        # 임의로 url 입력하여 접근 시 에러 화면 대신 게시판 목록으로 이동
        try:
            objs = Board.objects.get(id=pk, cust_id=request.session['sessionid'])
        except:
            return redirect('/board')
        title = request.GET['title']
        content = request.GET['content']
        objs.title = title
        objs.content = content
        objs.save()
        return redirect('/board/g/'+str(pk))

    @request_mapping("/d/<int:pk>", method="get")
    def delete(self, request, pk):
        # 해당 리뷰가 로그인된 사람이 쓴 것일 경우에만 삭제 실행, 아닌 경우 게시판 목록으로 이동
        try:
            obj = Board.objects.get(id=pk, cust_id=request.session['sessionid'])    # 로그인 기능 추가시 sessionid로 변경
        except:
            return redirect('/board')
        obj.delete()
        return redirect('/board')