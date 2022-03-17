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
        return render(request, 'list.html', context);

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

    @request_mapping("/view", method="get")
    def view(self, request):
        return render(request, 'view.html');

    @request_mapping("/write", method="get")
    def write(self, request):
        return render(request, 'write.html');

    @request_mapping("/edit", method="get")
    def edit(self, request):
        return render(request, 'edit.html');