from django.contrib import admin
from .models import Campaign, Event, News, UserProfile, Newsletter, Donation, Contact, EventRegistration, Comment, Payment, Order, Gallery, HomeContent, LearnMoreContent, LearnMoreSection, LearnMoreImage, DonationCategory, Stats

# Additional admin customization
admin.site.site_url = '/'
admin.site.empty_value_display = '(None)'

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'goal_amount', 'raised_amount', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['raised_amount']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'date', 'time', 'created_at']
    list_filter = ['category', 'date', 'created_at']
    search_fields = ['title', 'location', 'category']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content', 'author_name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'phone']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'campaign', 'amount', 'donated_at']
    list_filter = ['donated_at', 'campaign']
    search_fields = ['user__username', 'campaign__title']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'event', 'registered_at']
    list_filter = ['event', 'registered_at']
    search_fields = ['user_email', 'event__title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_approved', 'created_at', 'replied_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'message']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'donation', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__username', 'donation__transaction_id']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'campaign', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'razorpay_order_id']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']

@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = ['video', 'created_at', 'updated_at']
    
class LearnMoreSectionInline(admin.TabularInline):
    model = LearnMoreSection
    extra = 1
    ordering = ['order']

class LearnMoreImageInline(admin.TabularInline):
    model = LearnMoreImage
    extra = 1
    ordering = ['order']

@admin.register(LearnMoreContent)
class LearnMoreContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    inlines = [LearnMoreSectionInline, LearnMoreImageInline]

@admin.register(DonationCategory)
class DonationCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']

@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    list_display = ['total_campaigns', 'satisfied_donors', 'fund_raised', 'happy_volunteers', 'updated_at']

# Custom admin site class (optional)
class NGOAdminSite(admin.AdminSite):
    site_header = 'NGO Management System'
    site_title = 'NGO Admin Portal'
    index_title = 'NGO Dashboard'
    
    def each_context(self, request):
        context = super().each_context(request)
        context['site_url'] = '/'
        return context