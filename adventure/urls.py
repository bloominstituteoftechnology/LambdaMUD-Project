from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('grab', api.grab),
    url('drop', api.drop),
    url('inventory', api.inventory),
    url('equip', api.equip),
    url('takeOffItem', api.takeOffItem),
    url('getStats', api.getStats),
]