import json
import urllib.request

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .settings import ServerIP
from .settings import ServerPort


def getUrl(part):
    return "http://" + ServerIP + ":" + ServerPort + "/" + part


def login_site(request):
    if request.method == 'POST':

        secret = {'token': request.POST['secret']}
        url = getUrl("user/admin/login")
        res = requests.post(url, json=secret)

        if json.loads(res.text)["code"] == 200:
            return HttpResponseRedirect('manageQuestion')
    return render(request, 'login.html')


def manageQuestion(request):
    if request.method == 'GET':
        with urllib.request.urlopen(getUrl("question/list/1/100")) as f:
            data = json.loads(f.read().decode('utf-8'))
            if data["code"] == 200:
                context = {'data': data["data"]["content"]}
                return render(request, 'manageQuestion.html', context)
    return render(request, 'manageQuestion.html')


def detail(request, param):
    if request.method == 'POST':
        qid = param
        context = {}
        with urllib.request.urlopen(getUrl("question/questionInfo/" + qid)) as f:
            data = json.loads(f.read().decode('utf-8'))
            if data["code"] == 200:
                context['info'] = data["data"]

        with urllib.request.urlopen(getUrl("question/" + qid + "/answers/1/100")) as f:
            data = json.loads(f.read().decode('utf-8'))
            if data["code"] == 200:
                context['data'] = data["data"]["content"]

        return render(request, 'detail.html', context)
    return render(request, 'manageQuestion.html')


@csrf_exempt
def delAnswer(request, param):
    if request.method == 'POST':
        qid = param
        url = getUrl("answer/delete/") + qid
        res = requests.post(url)
        print(res.text)
