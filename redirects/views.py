from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

import pygsheets

from redirects.utils.auth_utils import create_user

bot_name = settings.BOT_NAME

def index(request):

    try: 
        tg_id = create_user(request)
        return redirect("https://t.me/{}?start=".format(bot_name)+tg_id)
    except Exception as e:
        return HttpResponse(e)


# Create your views here.
