from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('water', 'Water'),
        ('education', 'Education'),
        ('health', 'Health'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    raised_amount = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='campaigns/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()  # Main field for dynamic dates
    time = models.CharField(max_length=50, default='TBD')
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/')
    category = models.CharField(max_length=100, default='General')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/')
    author_name = models.CharField(max_length=100, default='Admin')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, default='News')

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.status}"

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    donated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_email = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} - {self.event.title}"

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    image = models.ImageField(upload_to='comments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    admin_reply = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.message[:50]}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.status}"

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Gallery Image {self.id}"

class HomeContent(models.Model):
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LearnMoreContent(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LearnMoreSection(models.Model):
    content = models.ForeignKey(LearnMoreContent, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    content_text = models.TextField()
    order = models.IntegerField(default=0)

class LearnMoreImage(models.Model):
    content = models.ForeignKey(LearnMoreContent, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    order = models.IntegerField(default=0)

class DonationCategory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    bg_color = models.CharField(max_length=50, default='bg-[#cae4f7]')
    people_helped = models.IntegerField(default=0)
    funds_raised = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    projects_completed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Stats(models.Model):
    total_campaigns = models.IntegerField(default=0)
    satisfied_donors = models.IntegerField(default=0)
    fund_raised = models.IntegerField(default=0)
    happy_volunteers = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Stats"