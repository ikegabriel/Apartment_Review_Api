from dataclasses import field
from review.models import Review, TestReview
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    # date = serializers.ReadOnlyField()
    # apartment_video = serializers.FileField()
    # apartment_image = serializers.FileField(required=False, allow_null=True)
    helpful_count = serializers.ReadOnlyField()
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Review
        # fields = '__all__'
        fields = [
            'id',
            'author',
            'author_name',
            'apartment_address',
            'apartment_image',
            'apartment_video',
            'apartment_review',
            'image1',
            'amenities_review',
            'image2',
            'landlord_review',
            'image3',
            'country',
            'state',
            'city',
            'date',
            'helpful_count'
        ]
    
    def get_helpful_count(self, obj):
        return self.helpful_count()
    
class ReviewListSerializer(serializers.ModelSerializer):
    helpful_count = serializers.ReadOnlyField()
    author_name = serializers.CharField(source='author.username')
    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'author_name',
            'apartment_address',
            'apartment_image',
            'country',
            'state',
            'city',
            'date',
            'helpful_count'
        ]
    
    def get_helpful_count(self, obj):
        return self.helpful_count()


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestReview
        fields = '__all__'