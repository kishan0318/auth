from django.shortcuts import render

# Create your views here.
# from tkinter.tix import Tree
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import generics
from .models import *

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
# from .models import Appointment, Department, Contact,Beds
from django.views.generic import ListView,View,CreateView,DetailView,DeleteView,TemplateView
from django.contrib.auth import authenticate, login,logout
from .forms import Logform,Register
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse_lazy,reverse


class SignupAPIView(APIView):
    permission_classes =[AllowAny,]

    def post(self,request):
        serializer=SignupSer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            return Response({'Success':'user created successfully','data':data},status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView): 
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSer(data=request.data)
        if serializer.is_valid():
            return Response({'Success': 'login successfully', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'Error': 'login unsuccesfull', 'data': serializer.data},status=HTTP_400_BAD_REQUEST)

class ActiveLogin(View):
    def get(self, request):
        f=Logform(None)
        k={'data':f}
        return render(request,'login.html',k)
    def post(self,request):
        f=Logform(request.POST)
        k={'data':f}
        if f.is_valid():
            u=f.cleaned_data.get('username')
            p=f.cleaned_data.get('password')
            ur=authenticate(username=u,password=p)
            nxt=request.GET.get('next')
            if ur:
                login(request,ur)
                if nxt:
                    return redirect(nxt)
                else:
                     return redirect('home')
        return render(request,'login.html',k)

class Signup(View): 
    def get(self,request):
        f=Register(None)
        return render(request,'signup.html',{"data":f})
    def post(self,request):
        f=Register(request.POST)
        if f.is_valid():
            data=f.save(commit=False)
            p=f.cleaned_data.get('password') 
            data.set_password(p)
            data.save()
            return redirect('login')
        return render(request,'signup.html',{"data":f})