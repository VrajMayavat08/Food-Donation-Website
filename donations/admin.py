from django.contrib import admin
from .models import (
    Category, Recipient, Donor, Donation, PickupRequest,
    UserHistory, Comment, PhotoUpload, FooterLink
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'contact_phone', 'contact_email', 'zip_code', 'created_at']
    search_fields = ['name', 'user__username', 'contact_email', 'zip_code']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'business_type', 'contact_phone', 'zip_code', 'is_verified', 'created_at']
    list_filter = ['business_type', 'is_verified', 'created_at']
    search_fields = ['business_name', 'user__username', 'contact_phone', 'contact_email', 'address']
    ordering = ['-created_at']
    readonly_fields = ['business_image_preview']
    
    def business_image_preview(self, obj):
        if obj.business_image:
            return f'<img src="{obj.business_image.url}" style="max-height: 100px; max-width: 100px;" />'
        return "No image uploaded"
    business_image_preview.short_description = 'Business Image Preview'
    business_image_preview.allow_tags = True


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['title', 'donor', 'category', 'quantity', 'expiry_date', 'zip_code', 'status', 'created_at']
    list_filter = ['category', 'status', 'expiry_date', 'created_at']
    search_fields = ['title', 'description', 'donor__username', 'zip_code']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'donation', 'desired_time_slot', 'desired_date', 'status', 'created_at']
    list_filter = ['status', 'desired_time_slot', 'desired_date', 'created_at']
    search_fields = ['recipient__name', 'donation__title']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'visits_count', 'last_viewed', 'last_viewed_donation_id', 'created_at']
    list_filter = ['created_at', 'last_viewed']
    search_fields = ['user__username']
    ordering = ['-last_viewed']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'donation', 'text', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'donation__title', 'text']
    ordering = ['-timestamp']


@admin.register(PhotoUpload)
class PhotoUploadAdmin(admin.ModelAdmin):
    list_display = ['donation', 'caption', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['donation__title', 'caption']
    ordering = ['-uploaded_at']


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['label', 'url', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['label', 'url']
    ordering = ['order', 'label']
