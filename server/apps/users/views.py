from django.db import DatabaseError
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout

# Create your views here.
from django import views
import re
from django import http
from . import models
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from constant import RETCODE


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
            user = models.User.objects.create_user(
                username=username, password=password, mobile=mobile
            )
        except DatabaseError:
            return http.JsonResponse({"msg": "注册失败"})

        # 登入用户，实现状态保持
        login(request, user)

        response = http.JsonResponse({"msg": "创建成功"})
        # 用户名存入cookie
        response.set_cookie("username", user.username, max_age=3600 * 24 * 15)
        return response


class UsernameCountView(APIView):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """判断用户名是否重复注册

        Args:
            request (_type_): 请求对象
            username (str): 用户名

        Returns:
            JSON: JSON
        """
        count = models.User.objects.filter(username=username).count()
        return http.JsonResponse({"code": RETCODE.OK, "msg": "OK", "count": count})


class MobileCountView(APIView):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        count = models.User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({"code": RETCODE.OK, "msg": "OK", "count": count})


class LoginView(APIView):
    def post(self, request):
        """登录逻辑

        Args:
            request (_type_): 请求对象
        """
        # 接受参数
        username = request.data.get("username")
        password = request.data.get("password")
        remembered = request.data.get("remembered")

        # 校验参数
        # 判断参数是否齐全
        if not all([username, password]):
            return http.HttpResponseForbidden("缺少必传参数")

        # 判断用户名是否是5-20个字符
        if not re.match(r"^[a-zA-Z0-9_-]{5,20}$", username):
            return http.HttpResponseForbidden("请输入正确的用户名或手机号")

        # 判断密码是否是8-20个数字
        if not re.match(r"^[0-9A-Za-z]{8,20}$", password):
            return http.HttpResponseForbidden("密码最少8位，最长20位")

        # 认证登录用户
        # 
        user = authenticate(request, username=username, password=password)
        if user is None:
            return http.JsonResponse(
                {
                    "code": RETCODE.OK,
                    "msg": "未注册或账号密码错误",
                }
            )

        # 实现状态保持
        login(request, user)

        # 设置状态保持的周期
        if remembered != "on":
            # 没有记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户：None表示两周后过期
            request.session.set_expiry(None)
        # 注册时用户名写入到cookie，有效期15天
        response = http.JsonResponse(
            {
                "code": RETCODE.OK,
                "msg": "登录成功",
            }
        )
        # 用户名存入cookie
        response.set_cookie("username", user.username, max_age=3600 * 24 * 15)
        # 响应登录结果
        return response


class LogoutView(APIView):
    """退出登录"""

    def get(self, request):
        """实现退出登录逻辑"""
        # 清理session
        logout(request)
        # 退出登录，重定向到登录页
        response = http.JsonResponse(
            {
                "code": RETCODE.OK,
                "msg": "退出成功",
            }
        )
        # 退出登录时清除cookie中的username
        response.delete_cookie("username")

        return response


class UserInfoView(APIView):
    def get(self, request):
        context = {
            "username": request.user.username,
            "mobile": request.user.mobile,
            "email": request.user.email,
        }
        response = http.JsonResponse(context)
        return response
