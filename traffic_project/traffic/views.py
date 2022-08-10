from django.db import models
from django.db.models.aggregates import Count
from django.db.models.fields import NullBooleanField
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render 
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile , Stream , parking , towing , speedLot
from django.contrib import auth
from .form import RegisterForm , LoginForm , FeedBackForm
from django.contrib.auth import authenticate, login, logout
from .filter import ParkingFilter , TowingFilter , SpeedLotFilter
from django.contrib import messages

#首頁
def index(request):
    count1 = Stream.objects.count()
    try: 
        mes1 = Stream.objects.get(id=count1)
        mes2 = Stream.objects.get(id=(count1-1))
        mes3 = Stream.objects.get(id=(count1-2))
        mes4 = Stream.objects.get(id=(count1-3))
        mes5 = Stream.objects.get(id=(count1-4))
    except:
        errormessage = "(讀取錯誤!)"
    return render(request,'traffic/index.html',locals())

#註冊
def enroll(request):
    if request.method == "POST":
        form = RegisterForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect("/welcome")
        else:
            return render(request, 'traffic/enroll.html', {'form':form})
    else:
        form = RegisterForm()
        context = {'form':form}
    return render(request, 'traffic/enroll.html', context)

#回饋
def feedback(request):
    if request.method == "POST":
        form = FeedBackForm(request.POST) 
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return redirect("/index")
        else:
            return render(request, 'traffic/feedback.html', {'form':form})
    else:
        form = FeedBackForm()
        context = {'form':form}
    return render(request,'traffic/feedback.html',locals())

#會員
def member(request):
    if request.user.is_authenticated:
        first_name = request.user.get_short_name()
        username = request.user.get_username()
    if request.method == "POST":
        return redirect("/member_fix")
    return render(request,'traffic/member.html',locals())

#會員資料修改
def member_fix(request):
    if request.user.is_authenticated:
        first_name = request.user.get_short_name()
    if request.method == "POST":
        newpassword = request.POST.get("newpassword")
        chkpassword = request.POST.get("chkpassword")
        if newpassword == chkpassword:
            if len(newpassword) <= 16 and len(newpassword) >= 1:
                request.user.password = request.user.set_password(newpassword)
                return redirect("/index")
            else:
                return render(request,'traffic/member_fix.html',locals())
    return render(request,'traffic/member_fix.html',locals())

#登入
def welcome(request):
    form = LoginForm()
    context = {'form':form}
    if request.user.is_authenticated:
        return redirect('/index')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/index') 
    return render(request,'traffic/welcome.html',context)

#編輯
def edit(request):
    if request.method == "POST":
        inputType = request.POST.get("inputType")
        content = request.POST.get("content")
        name = request.POST.get("name")
        if inputType == "停車場":
            inputContent = parking.objects.create(adress=content, name=name)
            inputContent.save()
        elif inputType == "測速照相":
            inputContent = speedLot.objects.create(adress=content, name=name)
            inputContent.save()
        elif inputType == "拖吊場":
            inputContent = towing.objects.create(situation=content, roadsection=name)
        elif inputType == "請選擇類別":
            return render(request,'traffic/edit.html',locals())
    return render(request,'traffic/edit.html',locals())

#查詢
def search(request):
    parkings = parking.objects.all()
    towings = towing.objects.all()
    speedLots = speedLot.objects.all()
    parkingFilter = ParkingFilter(queryset=parkings)
    towingFilter = TowingFilter(queryset=towings)
    speedLotFilter = SpeedLotFilter(queryset=speedLots)
    if request.method == "POST":
        if "choice" in request.POST:
            searchType = request.POST.get("searchType")
        if "parkingSubmit" in request.POST:
            parkingFilter = ParkingFilter(request.POST, queryset=parkings)
        elif "towingSubmit" in request.POST:
            towingFilter = TowingFilter(request.POST, queryset=towings)
        elif "speedLotSubmit" in request.POST:
            speedLotFilter = SpeedLotFilter(request.POST, queryset=speedLots)

    return render(request, 'traffic/search.html', locals())