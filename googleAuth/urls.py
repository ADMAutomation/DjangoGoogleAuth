from django.conf.urls import url
from .views import GoToGoogleLoginPage, AfterGoogleLoginPage
urlpatterns = [
    url(r'^stepOne/$', GoToGoogleLoginPage.as_view(), name="google-auth-step-one"),
    url(r'^stepTwo/$', AfterGoogleLoginPage.as_view(), name="google-auth-step-two"),
]
