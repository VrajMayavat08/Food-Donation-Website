from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Donation, Category, PickupRequest, Recipient, Donor,
    Comment, PhotoUpload, FooterLink
)
from django.utils import timezone


class DonationForm(forms.ModelForm):
    """Form for creating and editing donations"""
    class Meta:
        model = Donation
        fields = ['title', 'category', 'description', 'quantity', 'expiry_date', 'zip_code']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter food item title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the food item...'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5 lbs, 2 dozen, 1 container'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ZIP code'}),
        }
    
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < timezone.now().date():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date


class DonationWithImagesForm(forms.ModelForm):
    """Form for creating donations with image uploads"""
    images = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text="Upload an image (JPG, PNG, GIF). Max 5MB. You can add more photos later."
    )
    
    class Meta:
        model = Donation
        fields = ['title', 'category', 'description', 'quantity', 'expiry_date', 'zip_code']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter food item title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the food item...'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5 lbs, 2 dozen, 1 container'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ZIP code'}),
        }
    
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < timezone.now().date():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date
    
    def clean_images(self):
        image = self.files.get('images')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError(f"Image {image.name} is too large. Maximum size is 5MB.")
            
            # Check file extension
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
            file_extension = image.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(f"Image {image.name} has an unsupported format. Please use JPG, PNG, or GIF.")
        
        return image


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories"""
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter category description...'}),
        }


class PickupRequestForm(forms.ModelForm):
    """Form for creating pickup requests"""
    class Meta:
        model = PickupRequest
        fields = ['desired_time_slot', 'desired_date', 'message']
        widgets = {
            'desired_time_slot': forms.Select(attrs={'class': 'form-select'}),
            'desired_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special instructions or notes...'}),
        }
    
    def clean_desired_date(self):
        desired_date = self.cleaned_data.get('desired_date')
        if desired_date and desired_date < timezone.now().date():
            raise forms.ValidationError("Pickup date cannot be in the past.")
        return desired_date


class RecipientForm(forms.ModelForm):
    """Form for creating and editing recipient profiles"""
    class Meta:
        model = Recipient
        fields = ['name', 'contact_phone', 'contact_email', 'dietary_preferences', 'address', 'zip_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'dietary_preferences': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any dietary restrictions or preferences...'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter your address'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ZIP code'}),
        }


class DonorForm(forms.ModelForm):
    """Form for creating/updating donor profiles"""
    class Meta:
        model = Donor
        fields = ['business_name', 'business_image', 'contact_phone', 'contact_email', 'address', 'zip_code', 'business_hours', 'business_type', 'description']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business/store name'}),
            'business_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter business phone number'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter business email address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter business address'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ZIP code'}),
            'business_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mon-Fri 9AM-6PM, Sat 10AM-4PM'}),
            'business_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Restaurant, Grocery Store, Bakery, Home Cook'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of your business or organization...'}),
        }
    
    def clean_business_image(self):
        image = self.cleaned_data.get('business_image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file size must be under 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                raise forms.ValidationError("Please upload a valid image file (JPEG, PNG, or GIF).")
        
        return image


class HistoryFilterForm(forms.Form):
    """Form for filtering user history"""
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    min_visits = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum visits'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError("Start date cannot be after end date.")
        
        return cleaned_data


class CommentForm(forms.ModelForm):
    """Form for creating comments on donations"""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Write your comment here...',
                'maxlength': 500
            }),
        }
        labels = {
            'text': 'Comment'
        }


class UploadForm(forms.ModelForm):
    """Form for uploading photos"""
    class Meta:
        model = PhotoUpload
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter photo caption...'}),
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file size must be under 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                raise forms.ValidationError("Please upload a valid image file (JPEG, PNG, or GIF).")
        
        return image


class FooterLinkForm(forms.ModelForm):
    """Form for managing footer links"""
    class Meta:
        model = FooterLink
        fields = ['label', 'url', 'order', 'is_active']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DonationStatusForm(forms.ModelForm):
    """Form for updating donation status"""
    class Meta:
        model = Donation
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class DonationDeleteForm(forms.Form):
    """Form for confirming donation deletion"""
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="I understand that this action cannot be undone."
    )


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AccountTypeSignupForm(CustomUserCreationForm):
    """Enhanced signup form with account type selection and profile creation"""
    ACCOUNT_TYPE_CHOICES = [
        ('donor', 'Donor - I want to donate food'),
        ('recipient', 'Recipient - I want to receive food donations'),
    ]
    
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Account Type',
        help_text='Choose how you want to use Food Rescue'
    )
    
    # Donor-specific fields
    business_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Store name, restaurant name, or business name'}),
        help_text='Required for donors - helps recipients identify your business'
    )
    business_type = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Restaurant, Grocery Store, Bakery, Home Cook'}),
        help_text='Required for donors - helps categorize your donations'
    )
    contact_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        help_text='Required for donors - for pickup coordination'
    )
    contact_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        help_text='Required for donors - for donation notifications'
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Business address'}),
        help_text='Required for donors - for pickup arrangements'
    )
    zip_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP code'}),
        help_text='Required for donors - helps recipients find your location'
    )
    business_hours = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mon-Fri 9AM-6PM, Sat 10AM-4PM'}),
        help_text='Optional for donors - helps recipients plan pickups'
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of your business or organization'}),
        help_text='Optional for donors - helps recipients understand your business'
    )
    
    # Recipient-specific fields
    # Note: We'll use the user's first_name + last_name instead of a separate recipient_name field
    recipient_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        help_text='For pickup coordination'
    )
    recipient_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        help_text='For donation notifications'
    )
    recipient_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your address'}),
        help_text='For pickup arrangements'
    )
    recipient_zip_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP code'}),
        help_text='To find nearby donations'
    )
    dietary_preferences = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any dietary restrictions, allergies, or preferences'}),
        help_text='Optional for recipients'
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')
        
        if account_type == 'donor':
            # Validate donor-specific required fields
            donor_fields = ['business_name', 'business_type', 'contact_phone', 'contact_email', 'address', 'zip_code']
            for field in donor_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required for donor accounts.')
        
        elif account_type == 'recipient':
            # Validate recipient-specific required fields
            # No additional validation needed since first_name and last_name are already required
            pass
        
        return cleaned_data


class DonationSearchForm(forms.Form):
    """Form for searching donations"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search donations...',
            'aria-label': 'Search donations'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    zip_code = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ZIP code'
        })
    ) 