# Django imports
from math import perm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
from django.db import IntegrityError

# rest framework imports
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.views import csrf_exempt
from rest_framework import permissions

# models and other imports
from review.models import Review, TestReview
from .serializers import ReviewSerializer, TestSerializer, ReviewListSerializer
User = get_user_model()

class CreateTest(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            data = {
                'author':request.user.id,
                'image':request.data.get('image'),
                'title':request.data.get('title'),
                'description':request.data.get('description')
            }
        except AttributeError:
            return Response({'error':'The data seems to be missing some required fields'}, status=400)
        
        serializer = TestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({'error':'The data receieved is not valid'}, status=400)
# List all reviews
class ReviewListView(APIView):

    def get(self, request):
        reviews = Review.objects.all().order_by('-id') # or date if you wish
        serializer = ReviewListSerializer(reviews, many=True)

        return Response(serializer.data, status=200)

# Display a single review
class ReviewDetailView(APIView):

    # Fetch review instance using id
    def get_object(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return None

    # Handle the get request 
    def get(self, request, id):
        review_instance = self.get_object(id)

        if not review_instance:
            return Response({'error':'The object with review id does not exist'}, status=400)

        serializer = ReviewSerializer(review_instance)
        return Response(serializer.data, status=200)

# Create a new review
class ReviewCreateView(APIView):
    
    permission_classes =[permissions.IsAuthenticated]

    # Handle the post request
    def post(self, request):

        try:
            data = {
                'author':request.user.id,
                'apartment_address':request.data.get('apartment_address'),
                'apartment_image':request.data.get('apartment_image'),
                'apartment_video':request.data.get('apartment_video'),
                'apartment_review':request.data.get('apartment_review'),
                'image1':request.data.get('image1'),
                'amenities_review':request.data.get('amenities_review'),
                'image2':request.data.get('image2'),
                'landlord_review':request.data.get('landlord_review'),
                'image3':request.data.get('image3'),
                'country':request.data.get('country').lower(),
                'state':request.data.get('state').lower(),
                'city':request.data.get('city').lower()

            }
        except AttributeError:
            return Response({'error':'The data seems to be missing some required fields'}, status=400)
        
        # This helps to prevent validation errors, by removing empty fields from data
        if data['apartment_image'] == '' or None:
            del data['apartment_image']
        if data['apartment_video'] == '' or None:
            del data['apartment_video']
        if data['image1'] == '' or None:
            del data['image1']
        if data['image2'] == '' or None:
            del data['image2']
        if data['image3'] == '' or None:
            del data['image3']

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class ReviewUpdateView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id, user):
        try:
            return Review.objects.get(id=id, author=user)
        except Review.DoesNotExist:
            return None

    def get(self, request, id):
        review_instance = self.get_object(id, request.user.id)
        if not review_instance:
            return Response({'error':'The object with review id does not exist'}, status=200)

        serializer = ReviewSerializer(review_instance, many=True)
        return Response(serializer.data, status=200)

    def put(self, request, id):
        review_instance = self.get_object(id, request.user.id)
        if not review_instance:
            return Response({'error':'The object with review id does not exist'}, status=200)
        
        try:
            data = {
                'author':request.user.id,
                'apartment_address':request.data.get('apartment_address'),
                'apartment_image':request.data.get('apartment_image'),
                'apartment_video':request.data.get('apartment_video'),
                'apartment_review':request.data.get('apartment_review'),
                'image1':request.data.get('image1'),
                'amenities_review':request.data.get('amenities_review'),
                'image2':request.data.get('image2'),
                'landlord_review':request.data.get('landlord_review'),
                'image3':request.data.get('image3'),
                'country':request.data.get('country').lower(),
                'state':request.data.get('state').lower(),
                'city':request.data.get('city').lower()

            }
        except AttributeError:
            return Response({'error':'The data seems to be missing some required fields'}, status=400)
        

        ''' This helps to prevent validation errors, by removing empty fields from data.
            It is based on fields that were set blank=True in he models'''
        
        if data['apartment_image'] == '' or None:
            del data['apartment_image']
        if data['apartment_video'] == '' or None:
            del data['apartment_video']
        if data['image1'] == '' or None:
            del data['image1']
        if data['image2'] == '' or None:
            del data['image2']
        if data['image3'] == '' or None:
            del data['image3']

        serializer = ReviewSerializer(review_instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


@permission_classes([permissions.IsAuthenticated])
@api_view(['DELETE'])
def delete(request, id):
    try:
        review = Review.objects.get(id=id, author=request.user.id)
    except:
        review = None
    
    if not review:
        return JsonResponse({'error':'Object with review id does not exist'}, status=400)
    review.delete()
    return JsonResponse({'detail':'Review deleted succesfully'}, status=200)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def helpful(request, id):
    if request.method == 'POST':
        helpful = False
        review = get_object_or_404(Review, id=id)
        if review.helpful.filter(id=request.user.id).exists():
            review.helpful.remove(request.user)
            result = review.helpful_count()
            review.save()
        else:
            review.helpful.add(request.user)
            result = review.helpful_count()
            review.save()
            helpful = True
    return Response({'helpful_count':result, 'helpful':helpful}, status=200)


class ReviewHelpfulView(APIView):
    
    def get(self, request):
        reviews = Review.objects.all().order_by('-helpful')
        serializer = ReviewListSerializer(reviews, many=True)

        return Response(serializer.data, status=200)


@api_view(['GET'])
def country_search(request, key):
    sub_key = key.lower()
    try:
        reviews = Review.objects.filter(country=sub_key)
    except:
        return Response({'detail':'Keyword produced no results'}, status=404)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def state_search(request, key):
    sub_key = key.lower()
    try:
        reviews = Review.objects.filter(state=sub_key)
    except:
        return Response({'detail':'Keyword produced no results'}, status=404)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def city_search(request, key):
    sub_key = key.lower()
    try:
        reviews = Review.objects.filter(city=sub_key)
    except:
        return Response({'detail':'Keyword produced no results'}, status=404)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data, status=200)