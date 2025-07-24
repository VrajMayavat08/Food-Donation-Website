from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Category(models.Model):
    """Food categories for organizing donations"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Recipient(models.Model):
    """Recipients who can request food donations"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    dietary_preferences = models.TextField(blank=True, help_text="Any dietary restrictions or preferences")
    address = models.TextField(blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Donor(models.Model):
    """Donors who post food donations with custom business/store information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200, help_text="Store name, restaurant name, or business name")
    business_image = models.ImageField(
        upload_to='donor_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        help_text="Upload a photo of your business/store/restaurant (optional)"
    )
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    business_hours = models.TextField(blank=True, help_text="e.g., Mon-Fri 9AM-6PM, Sat 10AM-4PM")
    business_type = models.CharField(max_length=100, blank=True, help_text="e.g., Restaurant, Grocery Store, Bakery, Home Cook")
    description = models.TextField(blank=True, help_text="Brief description of your business or organization")
    is_verified = models.BooleanField(default=False, help_text="Verified business/organization")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.business_name} ({self.user.username})"


class Donation(models.Model):
    """Food donations posted by donors"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('donated', 'Donated'),
        ('expired', 'Expired'),
    ]
    
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.CharField(max_length=100, help_text="e.g., 5 lbs, 2 dozen, 1 container")
    expiry_date = models.DateField()
    zip_code = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_available = models.BooleanField(default=True)  # Keep for backward compatibility
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if hasattr(self.donor, 'donor') and self.donor.donor.business_name:
            return f"{self.title} by {self.donor.donor.business_name}"
        return f"{self.title} by {self.donor.username}"
    
    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()
    
    def save(self, *args, **kwargs):
        # Auto-update status to expired if past expiry date
        if self.expiry_date < timezone.now().date():
            self.status = 'expired'
        super().save(*args, **kwargs)


class PickupRequest(models.Model):
    """Requests to pick up donations"""
    TIME_SLOTS = [
        ('morning', 'Morning (8 AM - 12 PM)'),
        ('afternoon', 'Afternoon (12 PM - 4 PM)'),
        ('evening', 'Evening (4 PM - 8 PM)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='pickup_requests')
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='pickup_requests')
    desired_time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    desired_date = models.DateField()
    message = models.TextField(blank=True, help_text="Any special instructions or notes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['recipient', 'donation']
    
    def __str__(self):
        return f"Pickup request for {self.donation.title} by {self.recipient.name}"


class UserHistory(models.Model):
    """Track user activity and visits"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    visits_count = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)
    last_viewed_donation_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "User histories"
        ordering = ['-last_viewed']
    
    def __str__(self):
        return f"History for {self.user.username}"


class Comment(models.Model):
    """Comments on donations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.donation.title}"


class PhotoUpload(models.Model):
    """Photos uploaded for donations"""
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(
        upload_to='donation_photos/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Photo for {self.donation.title}"


class FooterLink(models.Model):
    """Footer links for the website"""
    label = models.CharField(max_length=100)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'label']
    
    def __str__(self):
        return self.label
