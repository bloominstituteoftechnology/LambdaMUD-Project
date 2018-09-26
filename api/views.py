from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json


@csrf_exempt
def register(request):
    data = json.loads(request.body)
    username = data['username']
    password1 = data['password1']
    password2 = data['password2']
    user = User(username=username)
    if len(username) <= 3:
        response = JsonResponse({"error": "Username must be at least 3 characters."}, safe=True, status=500)
    elif len(password1) <= 5:
        response = JsonResponse({"error": "Password must be at least 5 characters."}, safe=True, status=500)
    elif password1 != password2:
        response = JsonResponse({"error": "The two password fields didn't match."}, safe=True, status=500)
    else:
        try:
            user.validate_unique()
        except ValidationError:
            response = JsonResponse({"error": "A user with that username already exists."}, safe=True, status=500)
        else:
            user.set_password(password1)
            user.save()
            response = JsonResponse({"key":str(user.auth_token)}, safe=True, status=201)
    return response


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        response = JsonResponse({"error": "User does not exist."}, safe=True, status=500)
    else:
        if user.check_password(password):
            response = JsonResponse({"key": str(user.auth_token)}, safe=True, status=200)
        else:
            response = JsonResponse({"error": "Unable to log in with provided credentials."}, safe=True, status=500)
    return response

# Login
# curl -X POST -H "Content-Type: application/json" -d '{"username": "sibhat", "password":"sibhat"}' localhost:8800/api/login/

# registration
# curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser3", "password1":"testpassword3", "password2":"testpassword3"}' https://sibhat-lambdamud.herokuapp.com/api/registration/

# Login
# curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser3", "password":"testpassword3"}' https://sibhat-lambdamud.herokuapp.com/api/login/

# Initialize
# curl -X GET -H 'Authorization: Token 91f11c58f22101dbee9fe74154ea43c2564013d1' https://sibhat-lambdamud.herokuapp.com/api/adv/init/
# 3a94d205b2ec799d243817bceccb82ea5fa27100
# curl -X POST -H 'Authorization: Token 3a94d205b2ec799d243817bceccb82ea5fa27100' -H "Content-Type: application/json" -d '{"message":"Hello, world!"}' localhost:8800/api/adv/say/