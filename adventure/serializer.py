from rest_framework import serializers


class RoomSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, default="DEFAULT TITLE")
    description = serializers.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    items = serializers.CharField(max_length=500, default="")
    x = serializers.IntegerField(default=0)
    y = serializers.IntegerField(default=0)
    n = serializers.IntegerField(default=0)
    s = serializers.IntegerField(default=0)
    e = serializers.IntegerField(default=0)
    w = serializers.IntegerField(default=0)