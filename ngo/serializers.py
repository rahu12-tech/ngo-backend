from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Campaign, Event, News, UserProfile, Newsletter, Donation, Contact, EventRegistration, Comment, Payment, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=15)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'phone']
    
    def create(self, validated_data):
        phone = validated_data.pop('phone')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, phone=phone)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'username', 'phone', 'gender', 'profile_pic']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        # Update User fields
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()
        
        # Update UserProfile fields
        instance.phone = validated_data.get('phone', instance.phone)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        
        return instance

class CampaignSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Campaign
        fields = '__all__'
    
    def get_progress_percentage(self, obj):
        if float(obj.goal_amount) > 0:
            return round((float(obj.raised_amount) / float(obj.goal_amount)) * 100, 2)
        return 0

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = News
        fields = '__all__'

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

class DonationSerializer(serializers.ModelSerializer):
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    
    class Meta:
        model = Donation
        fields = ['id', 'campaign_title', 'amount', 'donated_at', 'transaction_id']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class EventRegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = EventRegistration
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['is_approved', 'admin_reply', 'replied_at']