from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from time import gmtime, strftime
import json
import random

from models import *

# Create your views here.


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
            image_list = list(xrange(max_score))
            random.shuffle(image_list)
            list_string = ""

            for i in image_list:
                list_string += str(i) + ":"

            for opponent in opponents:
                if opponent.email != email:
                    other_user = RunUser.objects.filter(email=opponent.email)[0]
                    opponent_name = other_user.name
            RunUser(name=name, email=email, opponent_name=opponent_name, max_score=max_score, online=online, random_array=list_string[:-1]).save()
            Online(email=email).save()
            if opponent_name == "":
                return JsonResponse({"wait": -100, "opponent_name": opponent_name})
            else:
                other_user.opponent_name = name
                other_user.opponent_score = -1
                other_user.save()
                start_time = strftime("%M:%S", gmtime())
                print  start_time
                min = int(start_time.split(":")[0])
                sec = int(start_time.split(":")[1])
                print min
                print sec
                if sec < 45:
                    sec += 15
                else:
                    sec -= 45
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
        data = json.loads(request.body.decode('utf-8'))
        email = data[u'email']
        user = RunUser.objects.get(email=email)
        if user.score == user.max_score:
            user.win = 1
        elif user.opponent_score == user.max_score:
            user.win = -1
        user.save()
        num_photos = Images.objects.all().count()
        return JsonResponse({"score": user.score, "opponent_score": user.opponent_score, "win": user.win, "total_photos": num_photos})


def photo(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data[u'email']
    user = RunUser.objects.get(email=email)
    user.score += 1
    user.save()
    num = 0
    selected_photo_url = ""
    if user.score < user.max_score:
        str_list = user.random_array.split(":")
        final_list = []
        for i in str_list:
            final_list.append(int(i))
        selected_photo_num = final_list[user.score]
        all_photos = Images.objects.all()
        selected_photo_url = all_photos[selected_photo_num].url
        num = all_photos.count()
    else:
        user.win = 1
        user.save()

    return JsonResponse({"photo_url": selected_photo_url, "total_photos": num, "win": user.win})


def end(request):
    if request.method == "POST":
        StartTime.objects.all().delete()
        Online.objects.all().delete()
        RunUser.objects.all().delete()
    return HttpResponse("Game Over!")