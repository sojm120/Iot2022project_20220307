from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
import json

from web.models import Rest, Review, Menu, Imgpath, Cate


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

    @request_mapping("/register", method="get")
    def register(self, request):
        return render(request, 'register.html');

    @request_mapping("/restDetail", method="get")
    def restDetail(self, request):
        return render(request, 'restDetail.html');

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


