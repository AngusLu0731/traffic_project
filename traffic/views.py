from django.db import models
from django.db.models.aggregates import Count
from django.db.models.fields import NOT_PROVIDED, NullBooleanField
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render ,reverse
from django.contrib.auth.forms import UserCreationForm
from django.urls import conf
from requests.sessions import RequestsCookieJar
from .models import UserProfile , Stream , parking , towing , speedLot
from django.contrib import auth
from .form import RegisterForm , LoginForm , FeedBackForm
from django.contrib.auth import authenticate, login, logout
from .filter import ParkingFilter , TowingFilter , SpeedLotFilter
from django.contrib import messages
import folium
from django.http import JsonResponse
import requests

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
        editType = request.POST.get("editType")
        editText = request.POST.get("editText")
        name = request.POST.get("name")
        if editType == "停車場":
            inputContent = parking.objects.create(address=editText, name=name)
            inputContent.save()
        elif editType == "測速照相":
            inputContent = speedLot.objects.create(situation=editText, roadsection=name)
            inputContent.save()
        elif editType == "拖吊場":
            inputContent = towing.objects.create(address=editText, name=name)
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
#路線規劃
def gps(request):
    endPos = request.GET.get("endPos")
    if request.method == "POST":
        try:
            # ---------抓取座標及前往地點---------
            nowLocationLat = request.POST.get("nowLocationLat")
            nowLocationLng = request.POST.get("nowLocationLng")
            endName = request.POST.get("endName")

            fmap = makeMap(endLocName=endName,nowLat=nowLocationLat,nowLng=nowLocationLng)

        except:
            return render(request, 'traffic/tmp.html', locals())
    return render(request, 'traffic/tmp.html', locals())

def makeMap(endLocName,nowLat,nowLng):
    nowLocation = str(nowLat) + ',' + str(nowLng)
    nowLocationArray = [nowLat , nowLng]
    endLoc = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + endLocName +'&key=AIzaSyDTPsRpUFtxGQeCmV2m_3wgqEf24zUUOo4')
    result = endLoc.json()["results"][0]["geometry"]["location"]
    endLocationLat = result["lat"]
    endLocationLng = result["lng"]
    endLocation = str(endLocationLat) + ',' + str(endLocationLng)
    endLocationArray = [endLocationLat , endLocationLng]
    s_list = [[25.043135226562843, 121.50879648391546],[25.038346054622917, 121.5302215974085],[25.049384360113525, 121.5166843803886],[25.041715027654064, 121.53736107843596],[25.04327067365064, 121.51902823632972]
,[25.03915524410227, 121.50764674279932],[25.03485704658262, 121.51666899740856],[25.04479319272896, 121.52334751405252],[25.028530326873096, 121.51574643064359],[25.02035771923586, 121.52253858506043],[25.029079252309323, 121.51215056373829],[25.027327005445223, 121.51603645507961],[25.119874556137468, 121.55300352962891],[25.07746437012625, 121.60038521987174],[25.059697049082796, 121.58629026741893],[25.053302664564175, 121.5778637820662],[25.06071575924033, 121.58304152624451],[25.0742506194474, 121.59002797836811],[25.081780188412555, 121.56999624912164],[25.083113375717335, 121.60429168360497],[25.073787873534336, 121.57917821580116],[25.066079221372416, 121.59045744314493],[25.08647669169678, 121.56906356961905],[25.08312521675387, 121.56347232609964],[25.055529769917555, 121.57920716821707],[25.071219478071466, 121.60408731598085],[25.021536371440558, 121.57735115721549],[25.000675759020385, 121.58962074932117],[24.991839148103182, 121.55159469770462],[24.984933107328313, 121.5541836977044],[24.992582292865812, 121.54061795286795],[25.009541394853688, 121.5578020888111],[25.00150347714372, 121.53905081908466],[24.989941862432026, 121.53971190998378],[25.165189551571558, 121.54356812111615],[25.130378350856713, 121.49678256908848]]



    #Making a get request
    response = requests.get('https://maps.googleapis.com/maps/api/directions/json?language=en&origin='+ nowLocation +'&destination='+ endLocation +'&key=AIzaSyAESYPbwIbstl-MhKtLP4mVhXqX7bT2of4')
        
    #轉彎的完整資料
    stepsData = response.json()["routes"][0]["legs"][0]["steps"]

    #總共幾個轉彎
    stepLen = len(response.json()["routes"][0]["legs"][0]["steps"])

    #轉彎點
    my_list = []
    for index ,i in enumerate(stepsData):
        startLat = i["start_location"]["lat"]
        startLng = i["start_location"]["lng"]
        my_list.append([startLat, startLng])
        if(index == (stepLen - 1)):
            endLat = i["end_location"]["lat"]
            endLng = i["end_location"]["lng"]
            my_list.append([i["end_location"]["lat"], i["end_location"]["lng"]])


    #建立地圖與設定位置
    fmap = folium.Map(location = nowLocationArray, zoom_start=16)

    #起點Mark
    fmap.add_child(folium.Marker(location = nowLocationArray,
                                popup = "起點"))

    #終點Mark
    fmap.add_child(folium.Marker(location = endLocationArray,
                                popup = endLocName))
    for s in s_list:
        fmap.add_child(folium.Marker(location = s,
                                popup = "相機",icon=folium.Icon(color='red',icon_color='#FFFF00')))
    #轉彎點
    points = my_list

    fmap.add_child(folium.PolyLine(locations=points, # 座標List
                                weight=8)) # 線條寬度
    
    sl = speedLot.objects.values_list('x', flat=True)
    sl_list = list(sl)
    sl_list = list(filter(None,sl_list))

    fmap = fmap._repr_html_()
    return fmap