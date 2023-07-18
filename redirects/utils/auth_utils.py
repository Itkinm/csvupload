import requests
import json
import google.oauth2.credentials

from django.conf import settings

from redirects.models import GoogleUser

domain = settings.DOMAIN
client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET


def register(tg_id):
    gu = GoogleUser.objects.filter(tg_id = tg_id).update(registered=True)


def check_registration(tg_id):
    try:
        return GoogleUser.objects.get(tg_id = tg_id).registered
    except:
        return False


def make_auth_url(channel_id):
    auth_url = 'https://accounts.google.com/o/oauth2/auth?response_type=code'
    auth_url += '&client_id={}'.format(client_id)
    auth_url += '&redirect_uri={}redirects'.format(domain)
    auth_url += '&scope=https://www.googleapis.com/auth/drive'
    auth_url += '&access_type=offline'
    auth_url += '&state={}'.format(channel_id)

    return auth_url


def get_access_token(refresh_token):
    url = 'https://www.googleapis.com/oauth2/v4/token'

    params = json.dumps({
        "refresh_token":refresh_token,
        "client_id":client_id,
        "client_secret":client_secret,
        "grant_type":"refresh_token"
    })

    headers={"content-type":"application/json"}

    result = requests.post(url, data=params, headers=headers)
    access_token = json.loads(result.text)["access_token"]

    return access_token


def create_credentials(tg_id):

    gu = GoogleUser.objects.get(tg_id=tg_id)
    access_token = get_access_token(gu.refresh_token)

    credentials = google.oauth2.credentials.Credentials(
    access_token,
    refresh_token=gu.refresh_token,
    token_uri='{}redirects'.format(domain),
    client_id=client_id,
    client_secret=client_secret)

    return credentials


def get_refresh_token(code):

    url = "https://www.googleapis.com/oauth2/v4/token"

    params = json.dumps({
        "code":code,
        "redirect_uri":"{}redirects".format(domain),
        "client_id":client_id,
        "client_secret":client_secret,
        "grant_type":"authorization_code"
    })

    headers={"content-type":"application/json"}

    result = requests.post(url, data=params, headers=headers)

    refresh_token = json.loads(result.text)["refresh_token"]

    return refresh_token


def get_id_from_request(request):
     state = request.GET.get("state", "")
     if state.startswith('tg_id'):
          return state[5:]


def create_user(request):
    tg_id = get_id_from_request(request)
    refresh_token = get_refresh_token(request.GET.get("code", ""))
    gu, created = GoogleUser.objects.update_or_create(
        tg_id = tg_id, 
        defaults={"refresh_token": refresh_token})
    return tg_id





