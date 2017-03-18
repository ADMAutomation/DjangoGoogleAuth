from django.views.generic import RedirectView, View
from .utils import getGoogleAPIAuthURI, getGoogleCredentials, getRedirectUrlFromRequest, \
    getUserFromIdInfo, getUserJWTToken
from django.shortcuts import render

from django.http import HttpResponseForbidden

from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .permissions import IsAnonymous
from .serializers import GoogleTokenSerializer
from .utils import getUserJWTToken, getIdInfoFromRawIdToken, getUserFromIdInfo
from .models import GoogleCredentials
from .utils import updateUserImageUrl


class GoToGoogleLoginPage(RedirectView):
    permanent = False
    url = ''
    def get_redirect_url(self, *args, **kwargs):
        try:
            self.request.session['redirect_to'] = self.request.GET['redirect_to']
        except:
            pass
        return getGoogleAPIAuthURI(
            getRedirectUrlFromRequest(self.request)
        )

class AfterGoogleLoginPage(View):
    def get(self, request, *args, **kwargs):
        request = self.request
        credentials = getGoogleCredentials(
            request.GET['code'],
            getRedirectUrlFromRequest(request)
        )
        current_user = getUserFromIdInfo(credentials.id_token)
        if current_user is None:
            return HttpResponseForbidden()
        return render(request, 'googleAuth/stepTwoPopup.html', context={'new_token': getUserJWTToken(current_user)})


class GoogleTokenToDjangoTokenViewSet(viewsets.GenericViewSet):
    queryset = GoogleCredentials.objects.filter(id=-1)
    serializer_class = GoogleTokenSerializer
    permission_classes = (IsAnonymous,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        idinfo = getIdInfoFromRawIdToken(serializer.data['token'])
        if idinfo is None:
            raise ValidationError({'token': 'not a valid token'})
        u = getUserFromIdInfo(idinfo)
        token = None
        if u is None:
            raise ValidationError({'token': 'not a valid token'})
        else:
            token = getUserJWTToken(u)
        updateUserImageUrl(u, idinfo['picture'])
        serializer = self.get_serializer(data={'token': token})
        serializer.is_valid(raise_exception=True)


        return Response(serializer.data, status=status.HTTP_201_CREATED)


