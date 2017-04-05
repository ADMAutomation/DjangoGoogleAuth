from django.conf.urls import url
from .views import GoToGoogleLoginPage, AfterGoogleLoginPage
from .urlsAPI import urlpatterns as google_api_urlpatterns

urlpatterns = [
    url(r'^stepOne/$', GoToGoogleLoginPage.as_view(), name="google-auth-step-one"),
    url(r'^stepTwo/$', AfterGoogleLoginPage.as_view(), name="google-auth-step-two"),
]
