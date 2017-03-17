from django.views.generic import RedirectView, View
from .utils import getGoogleAPIAuthURI, getGoogleCredentials, getRedirectUrlFromRequest, \
    getUserFromIdInfo, getUserJWTToken
from django.shortcuts import render

from django.http import HttpResponseForbidden

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

