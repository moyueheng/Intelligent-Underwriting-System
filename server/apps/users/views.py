from django.shortcuts import render

# Create your views here.
from django import views
import re
from django import http
from . import models
import json

from rest_framework.views import APIView
from rest_framework.response import Response


class RegisterView(APIView):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        # 获取参数
        username = request.data.get("username")
        password = request.data.get("password")
        password2 = request.data.get("password2")
        mobile = request.data.get("mobile")
        allow = request.data.get("allow")

        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden("缺少必传参数")
        # 判断用户名是否是5-20个字符
        if not re.match(r"^[a-zA-Z0-9_-]{5,20}$", username):
            return http.HttpResponseForbidden("请输入5-20个字符的用户名")
        # 判断密码是否是8-20个数字
        if not re.match(r"^[0-9A-Za-z]{8,20}$", password):
            return http.HttpResponseForbidden("请输入8-20位的密码")
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden("两次输入的密码不一致")
        # 判断手机号是否合法
        if not re.match(r"^1[3-9]\d{9}$", mobile):
            return http.HttpResponseForbidden("请输入正确的手机号码")
        # 判断是否勾选用户协议
        if allow != "on":
            return http.HttpResponseForbidden("请勾选用户协议")

        try:
            models.User.objects.create_user(
                username=username, password=password, mobile=mobile
            )
        except:
            return http.JsonResponse({"msg": "注册失败"})

        return http.JsonResponse({"msg": "创建成功"})
