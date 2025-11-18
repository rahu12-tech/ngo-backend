from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
import razorpay
from .models import Campaign, Event, News, Newsletter, Donation, Contact, EventRegistration, Comment, Payment, Order, Gallery, HomeContent, LearnMoreContent, LearnMoreSection, LearnMoreImage, DonationCategory, Stats
from .serializers import *
from rest_framework.views import APIView

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        phone = request.data.get('phone', '')
        
        # Check if user exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name
        )
        
        # Create profile
        UserProfile.objects.create(user=user, phone=phone)
        
        # Create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name
            },
            'token': token.key
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = User.objects.get(email=email)
        user = authenticate(username=user.username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name
                },
                'token': token.key
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
            
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=401)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

class CampaignListView(generics.ListCreateAPIView):
    queryset = Campaign.objects.filter(is_active=True)
    serializer_class = CampaignSerializer
    permission_classes = [AllowAny]

class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [AllowAny]

class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

class NewsListView(generics.ListCreateAPIView):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

class NewsletterListView(generics.ListCreateAPIView):
    queryset = Newsletter.objects.filter(is_active=True)
    serializer_class = NewsletterSerializer
    permission_classes = [AllowAny]

class DonationListView(generics.ListCreateAPIView):
    queryset = Donation.objects.all().order_by('-donated_at')
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
def contact_submit(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Contact form submitted successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def newsletter_subscribe(request):
    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Successfully subscribed to newsletter'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def event_register(request):
    serializer = EventRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Successfully registered for event'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response({
            'user': serializer.data,
            'message': 'Profile fetched successfully'
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Update user fields
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()
        
        # Update profile fields
        profile.phone = request.data.get('number', profile.phone)
        profile.gender = request.data.get('gender', profile.gender)
        profile.save()
        
        serializer = UserProfileSerializer(profile)
        return Response({
            'user': serializer.data,
            'message': 'Profile updated successfully'
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_donations(request):
    try:
        donations = Donation.objects.filter(user=request.user).select_related('campaign')
        data = [{
            'id': d.id,
            'campaign_title': d.campaign.title,
            'amount': str(d.amount),
            'donated_at': d.donated_at,
            'transaction_id': d.transaction_id or f"TXN{d.id:06d}"
        } for d in donations]
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        campaign_id = request.data.get('campaign_id')
        amount_raw = request.data.get('amount')
        
        amount = float(str(amount_raw))
        campaign = Campaign.objects.get(id=campaign_id)
        
        # Create Razorpay order
        order_data = {
            'amount': int(amount * 100),
            'currency': 'INR',
            'receipt': f'receipt_{campaign_id}_{request.user.id}'
        }
        
        razorpay_order = client.order.create(data=order_data)
        
        # Save order in database
        Order.objects.create(
            user=request.user,
            campaign=campaign,
            amount=amount,
            razorpay_order_id=razorpay_order['id']
        )
        
        return Response({
            'order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency']
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    try:
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')
        
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        client.utility.verify_payment_signature(params_dict)
        
        # Get order from database
        order = Order.objects.get(razorpay_order_id=razorpay_order_id, user=request.user)
        order.razorpay_payment_id = razorpay_payment_id
        order.status = 'completed'
        order.save()
        
        # Create donation record
        message = request.data.get('message', 'Thank you for your generous donation!')
        donation = Donation.objects.create(
            user=request.user,
            campaign=order.campaign,
            amount=order.amount,
            transaction_id=razorpay_payment_id,
            order_id=razorpay_order_id,
            message=message
        )
        
        # Update campaign raised amount
        campaign = order.campaign
        campaign.raised_amount = float(campaign.raised_amount) + float(order.amount)
        campaign.save()
        
        return Response({
            'message': 'Payment verified successfully',
            'donation_id': donation.id,
            'transaction_id': donation.transaction_id
        })
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def gallery_list(request):
    galleries = Gallery.objects.filter(is_active=True).order_by('-created_at')
    data = []
    for gallery in galleries:
        data.append({
            'id': gallery.id,
            'image': request.build_absolute_uri(gallery.image.url) if gallery.image else None,
            'created_at': gallery.created_at
        })
    return Response(data)

class HomeContentView(APIView):
    def get(self, request):
        content = HomeContent.objects.first()
        if content and content.video:
            return Response({'video': request.build_absolute_uri(content.video.url)})
        return Response({'video': ''})

class LearnMoreContentView(APIView):
    def get(self, request):
        content = LearnMoreContent.objects.prefetch_related('sections', 'images').first()
        if content:
            sections = [{'id': s.id, 'title': s.title, 'content': s.content_text}
                       for s in content.sections.all().order_by('order')]
            images = [img.image_url for img in content.images.all().order_by('order')]
            return Response({'title': content.title, 'sections': sections, 'images': images})
        return Response(None)

class AdminHomeContentView(APIView):
    def put(self, request):
        content, created = HomeContent.objects.get_or_create(id=1)
        if 'video' in request.FILES:
            content.video = request.FILES['video']
            content.save()
        return Response({'message': 'Video uploaded successfully'})

class AdminLearnMoreContentView(APIView):
    def put(self, request):
        content, created = LearnMoreContent.objects.get_or_create(id=1)
        content.title = request.data.get('title', '')
        content.save()
        
        content.sections.all().delete()
        content.images.all().delete()
        
        for i, section in enumerate(request.data.get('sections', [])):
            LearnMoreSection.objects.create(
                content=content, title=section.get('title', ''),
                content_text=section.get('content', ''), order=i)
        
        for i, img_url in enumerate(request.data.get('images', [])):
            if img_url:
                LearnMoreImage.objects.create(content=content, image_url=img_url, order=i)
        
        return Response({'message': 'Updated'})

class DonationCategoriesView(APIView):
    def get(self, request):
        categories = DonationCategory.objects.filter(is_active=True)
        data = []
        for category in categories:
            data.append({
                'id': category.id,
                'title': category.title,
                'description': category.description,
                'image': request.build_absolute_uri(category.image.url) if category.image else '',
                'bg_color': category.bg_color
            })
        return Response(data)

class DonationCategoryDetailView(APIView):
    def get(self, request, pk):
        try:
            category = DonationCategory.objects.get(pk=pk, is_active=True)
            return Response({
                'id': category.id,
                'title': category.title,
                'description': category.description,
                'image': request.build_absolute_uri(category.image.url) if category.image else '',
                'stats': {
                    'people_helped': category.people_helped,
                    'funds_raised': str(category.funds_raised),
                    'projects_completed': category.projects_completed
                }
            })
        except DonationCategory.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)

class StatsView(APIView):
    def get(self, request):
        stats = Stats.objects.first()
        if stats:
            return Response({
                'totalCampaigns': stats.total_campaigns,
                'satisfiedDonors': stats.satisfied_donors,
                'fundRaised': stats.fund_raised,
                'happyVolunteers': stats.happy_volunteers
            })
        return Response({
            'totalCampaigns': 2348,
            'satisfiedDonors': 1748,
            'fundRaised': 4287,
            'happyVolunteers': 1294
        })

class AdminStatsView(APIView):
    def put(self, request):
        stats, created = Stats.objects.get_or_create(id=1)
        stats.total_campaigns = request.data.get('totalCampaigns', stats.total_campaigns)
        stats.satisfied_donors = request.data.get('satisfiedDonors', stats.satisfied_donors)
        stats.fund_raised = request.data.get('fundRaised', stats.fund_raised)
        stats.happy_volunteers = request.data.get('happyVolunteers', stats.happy_volunteers)
        stats.save()
        return Response({'message': 'Stats updated'})

