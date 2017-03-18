from oauth2client.client import OAuth2WebServerFlow
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from oauth2client import client, crypt
from rest_framework_jwt.settings import api_settings
from .models import GoogleUserProfiles as UserProfiles

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def getRedirectUrlFromRequest(request):
    return request.build_absolute_uri(reverse('google-auth-step-two'))

def getFlow(redirect_url, scope):
    return OAuth2WebServerFlow(client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
                               client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                               scope=' '.join(scope),
                               redirect_uri=redirect_url)

def getGoogleAPIAuthURI(redirect_url, scope=settings.GOOGLE_API_SCOPE):
    flow = getFlow(redirect_url, scope)
    return flow.step1_get_authorize_url()

def getGoogleCredentials(code, redirect_url, scope=settings.GOOGLE_API_SCOPE):
    flow = getFlow(redirect_url, scope)
    credentials = flow.step2_exchange(code)
    return credentials

def getUserFromIdInfo(idinfo):
    if not idinfo['email_verified']:
        return None

    u = User.objects.filter(email=idinfo['email'])
    if len(u) != 0:
        return u[0]
    elif not settings.FREE_USER_REGISTRATION:
        return None
    else:
        return createUserFromGoogleIdInfo(idinfo)

def getIdInfoFromRawIdToken(id_token):
    idinfo = None
    try:
        idinfo = client.verify_id_token(id_token, settings.GOOGLE_OAUTH2_CLIENT_ID)
        # Or, if multiple clients access the backend server:
        # idinfo = client.verify_id_token(token, None)
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #    raise crypt.AppIdentityError("Unrecognized client.")

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        return None
    return idinfo

def getUserFromRawIdToken(id_token):
    idinfo = getIdInfoFromRawIdToken(id_token)
    if idinfo is None:
        return None
    return getUserFromIdInfo(idinfo)


def createUserFromGoogleIdInfo(idinfo):
    new_user = User(
        is_active = True,
        username = idinfo['email'],
        email = idinfo['email'],
        first_name = idinfo['given_name'],
        last_name = idinfo['family_name']
    )
    new_user.save()
    return new_user

def createUserFromGoogleCredentials(credentials):
    return createUserFromGoogleIdInfo(credentials.id_token)

def getUserJWTToken(current_user):
    new_payload = jwt_payload_handler(current_user)
    return jwt_encode_handler(new_payload)


def getUserProfile(user):
    try:
        profile = UserProfiles.objects.get(user=user)
    except:
        profile = UserProfiles(user=user)
        profile.save()
    return profile

def updateUserImageUrl(user, url):
    profile = getUserProfile(user)
    profile.imageUrl = url
    profile.save()

