from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class DocumentProcessView(APIView):
    def post(self, request, *args, **kwargs):
        # get the file from the request
        file = request.FILES["file"]
        # 判断文件类型必须是图片
        if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            return Response(
                {"error": "file type must be image"}, status=status.HTTP_400_BAD_REQUEST)
        # read the file
        file_data = file.read()
        # decode the file
        file_data = file_data.decode("utf-8")
        # split the file by new line

