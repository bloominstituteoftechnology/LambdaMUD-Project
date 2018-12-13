from django.urls import include, path
from django.conf.urls import url

# tells us to include authorization urls for given paths

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]
