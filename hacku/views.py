from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from time import gmtime, strftime
import json

from models import *

# Create your views here.


def index(request):
    return HttpResponse("Akash Trehan")


def start(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        name = data[u'name']
        email = data[u'email']
        print RunUser.objects.filter(email=email)
        if not RunUser.objects.filter(email=email):
            max_score = Images.objects.all().count()
            online = 1
            opponents = Online.objects.all()
            opponent_name = ""
            other_user = ""
            for opponent in opponents:
                if opponent.email != email:
                    other_user = RunUser.objects.filter(email=opponent.email)[0]
                    opponent_name = other_user.name
            RunUser(name=name, email=email, opponent_name=opponent_name, max_score=max_score, online=online).save()
            Online(email=email).save()
            if opponent_name == "":
                return JsonResponse({"wait": -100, "opponent_name": opponent_name})
            else:
                other_user.opponent_name = name
                other_user.opponent_score = 0
                other_user.save()
                start_time = strftime("%M:%S", gmtime())
                min = int(start_time.split(":")[0])
                sec = int(start_time.split(":")[1])
                if sec < 45:
                    sec += 15
                else:
                    sec -= - 45
                    min += + 1
                StartTime(time=(str(min)+":"+str(sec))).save()

                # TODO Delete from start time when it ends

                return JsonResponse({"wait": -100, "opponent_name": opponent_name})
        else:
            user = RunUser.objects.get(email=email)
            if user.opponent_name == "":
                return JsonResponse({"wait": -100, "opponent_name": ""})
            else:
                now = strftime("%M:%S", gmtime())
                min_now = str(now.split(":")[0])
                sec_now = str(now.split(":")[1])
                final = StartTime.objects.all()[0].time
                min_fin = str(final.split(":")[0])
                sec_fin = str(final.split(":")[1])
                print (int(min_fin) - int(min_now))*60
                wait = (int(min_fin) - int(min_now))*60 + int(sec_fin) - int(sec_now)
                return JsonResponse({"wait": wait, "opponent_name": user.opponent_name})


def refresh(request):
    if request.method == "POST":
        print json.loads(request.body.decode('utf-8'))[u'name']
        return HttpResponse("lolololo")