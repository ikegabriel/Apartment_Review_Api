from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.views import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

User = get_user_model()


@csrf_exempt
@api_view(['POST'])
def signup(request):
    try:
        if request.method == 'POST':
            data = JSONParser().parse(request)
            try:
                user = User.objects.create_user(
                    email=data['email'],
                    username=data['username'],
                    password=data['password']
                )
            except:
                return JsonResponse({'error':'Data appears to be invalid or incomplete, check again'}, status=400)
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
    except IntegrityError:
        return JsonResponse({'error':'Username or email taken, choose another'}, status=400)

@permission_classes([permissions.IsAuthenticated])
@api_view(['POST','GET'])
def update(request):
    if request.method == 'GET':
        user = get_object_or_404(User, id=request.user.id)
        data = {
            'id':user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'email':user.email,
        }
        return JsonResponse(data, status=200)
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        data = JSONParser().parse(request)
        try:
            if data['first_name']:
                user.first_name=data['first_name']
            if data['last_name']:
                user.last_name=data['last_name']
            if data['username']:
                user.username=data['username']
            if data['password']:
                user.set_password=data['password']
            user.save()
        except:
            return JsonResponse({'error':'Data appears to be invalid or incomplete, check again'}, status=400)

        updated_data = {
            'id':user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'email':user.email
        }
        return JsonResponse(updated_data, status=200)



@csrf_exempt
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = authenticate(
                request,
                email=data['email'],
                password=data['password']
                )
        except:
            return JsonResponse({'error':'Data appears to be invalid or incomplete, check again'}, status=400)
        if user is None:
            return JsonResponse({'error':'unable to login, check email and password'}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=200)
    return JsonResponse({'error':'something went wrong'}, status=400)
    

@api_view(['POST'])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return JsonResponse({'detail':'user logged out successfully'}, status=200)
    except:
        return JsonResponse({'error':'user not found'}, status=400)
    