from django.shortcuts import render

# Create your views here.
from django import views

class RegisterView(views.View):

    def get(self, request):
        return render(request, 'register.html')