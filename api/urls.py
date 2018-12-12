from django.urls import include, path, re_path
from django.conf.urls import url
from rest_framework.authtoken import views

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    re_path(r'^api-token-auth/', views.obtain_auth_token)
]
