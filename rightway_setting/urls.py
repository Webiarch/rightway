from django.conf.urls import url
from django.contrib import admin
from rightway import views

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^bigcommerce/callback', views.AuthCallback.as_view(), name='authcallback'),
    url(r'^bigcommerce/load', views.Load.as_view(), name='load'),
    url(r'^', views.Display.as_view(), name='display'),
    url(r'^store/$', views.DisplayStoreUser.as_view(), name='store'),
]