from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json

"""
This is will create view for a player registered, checks for username and password in database and returns data with auth token and error messages.
"""
@csrf_exempt
def register(request):
    data = json.loads(request.body)
    username = data['username']
    password1 = data['password1']
    password2 = data['password2']
    user=User(username=username)
    if len(username) <= 3:
        response = JsonResponse({"error":"Username must be at least 3 characters."}, safe=True, status=500)
    elif len(password1) <= 5:
        response = JsonResponse({"error":"Password must be at least 5 characters."}, safe=True, status=500)
    elif password1 != password2:
        response = JsonResponse({"error":"The two password fields didn't match."}, safe=True, status=500)
    else:
      try:
          user.validate_unique()
      except ValidationError:
          response = JsonResponse({"error":"A user with that username already exists."}, safe=True, status=500)
      else:
          user.set_password(password1)
          user.save()
          response = JsonResponse({"key":str(user.auth_token)}, safe=True, status=201)
    return response

"""
This will take a user request for access and checks for existing username and password in database and will return with auth token or if not existed, then return error message.
"""

@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        response = JsonResponse({"error":"User does not exist."}, safe=True, status=500)
    else:
        if user.check_password(password):
            response = JsonResponse({"key":str(user.auth_token)}, safe=True, status=200)
        else:
            response = JsonResponse({"error":"Unable to log in with provided credentials."}, safe=True, status=500)
    return response

