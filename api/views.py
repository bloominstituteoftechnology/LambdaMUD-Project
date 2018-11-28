from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json

@csrf_exempt
def register(request):
    # example: request.body
    # {
    # "username": "dragon",
    # "password1": "I am a password",
    # "password2": "I am a password"
    # }
    # Two passwords are needed to ensure user entered the password
    # they have in mind
    data = json.loads(request.body)
    username = data['username']
    password1 = data['password1']
    password2 = data['password2']
    user=User(username=username)
    if len(username) < 3:
        response = JsonResponse({"error":"Username must be at least 3 characters."}, safe=True, status=500)
    elif len(password1) < 5:
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

@csrf_exempt
def login(request):
    # example: request.body
    # {
    #   "username": "dragon",
    #   "password": "I am a password"
    # }
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

