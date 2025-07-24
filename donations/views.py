from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Donation, Category, PickupRequest, Recipient, Donor,
    UserHistory, Comment, PhotoUpload, FooterLink
)
from .forms import (
    DonationForm, DonationWithImagesForm, CategoryForm, PickupRequestForm, RecipientForm, DonorForm,
    HistoryFilterForm, CommentForm, UploadForm, FooterLinkForm,
    CustomUserCreationForm, AccountTypeSignupForm, DonationSearchForm, DonationStatusForm, DonationDeleteForm
)


# Class-Based Views
class DonationListView(ListView):
    """Display list of all donations with search and filtering"""
    model = Donation
    template_name = 'donations/donation_list.html'
    context_object_name = 'donations'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Donation.objects.filter(is_available=True).select_related('donor', 'category')
        
        # Get search parameters
        query = self.request.GET.get('query', '')
        category_id = self.request.GET.get('category', '')
        zip_code = self.request.GET.get('zip_code', '')
        
        # Apply filters
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(donor__username__icontains=query)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if zip_code:
            queryset = queryset.filter(zip_code__icontains=zip_code)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DonationSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()
        return context


class DonationCreateView(LoginRequiredMixin, CreateView):
    """Create a new donation"""
    model = Donation
    form_class = DonationWithImagesForm
    template_name = 'donations/donation_form.html'
    success_url = reverse_lazy('donations:donation_list')
    
    def form_valid(self, form):
        form.instance.donor = self.request.user
        response = super().form_valid(form)
        
        # Handle image upload
        image = self.request.FILES.get('images')
        if image:
            PhotoUpload.objects.create(
                donation=form.instance,
                image=image,
                caption=f"Photo for {form.instance.title}"
            )
            messages.success(self.request, 'Donation created successfully with image!')
        else:
            messages.success(self.request, 'Donation created successfully!')
        
        return response


class DonationDetailView(DetailView):
    """Display donation details"""
    model = Donation
    template_name = 'donations/donation_detail.html'
    context_object_name = 'donation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['photos'] = self.object.photos.all()
        context['comment_form'] = CommentForm()
        
        # Track user history
        if self.request.user.is_authenticated:
            history, created = UserHistory.objects.get_or_create(user=self.request.user)
            history.visits_count += 1
            history.last_viewed_donation_id = self.object.id
            history.save()
        
        return context
    
    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        # Set cookie for last viewed donation
        response.set_cookie('last_viewed_donation_id', self.object.id, max_age=30*24*60*60)  # 30 days
        return response


class PickupRequestListView(LoginRequiredMixin, ListView):
    """Display list of pickup requests for the current user"""
    model = PickupRequest
    template_name = 'donations/pickup_list.html'
    context_object_name = 'pickup_requests'
    paginate_by = 10
    
    def get_queryset(self):
        if hasattr(self.request.user, 'recipient'):
            return PickupRequest.objects.filter(recipient=self.request.user.recipient)
        return PickupRequest.objects.none()


class PickupRequestCreateView(LoginRequiredMixin, CreateView):
    """Create a new pickup request"""
    model = PickupRequest
    form_class = PickupRequestForm
    template_name = 'donations/pickup_form.html'
    success_url = reverse_lazy('donations:pickup_list')
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user has a recipient profile
        if not hasattr(request.user, 'recipient'):
            messages.error(request, 'You need to create a recipient profile first.')
            return redirect('donations:recipient_create')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donation'] = get_object_or_404(Donation, pk=self.kwargs['donation_id'])
        return context
    
    def form_valid(self, form):
        form.instance.recipient = self.request.user.recipient
        form.instance.donation = get_object_or_404(Donation, pk=self.kwargs['donation_id'])
        
        # Check if user already has a request for this donation
        if PickupRequest.objects.filter(recipient=self.request.user.recipient, donation=form.instance.donation).exists():
            messages.error(self.request, 'You have already requested this donation.')
            return redirect('donations:donation_detail', pk=form.instance.donation.pk)
        
        messages.success(self.request, 'Pickup request created successfully!')
        return super().form_valid(form)


# Function-Based Views
def format_duration(seconds):
    """Convert seconds into human-readable format"""
    if seconds is None or seconds == "Not available":
        return "Not available"
    
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "Invalid value"
    
    if seconds < 0:
        return "Invalid value"
    
    # Calculate days, hours, minutes
    days = seconds // 86400  # 86400 seconds in a day
    hours = (seconds % 86400) // 3600  # 3600 seconds in an hour
    minutes = (seconds % 3600) // 60  # 60 seconds in a minute
    remaining_seconds = seconds % 60
    
    # Build the formatted string
    parts = []
    
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    
    # Only show seconds if less than a minute
    if seconds < 60:
        parts.append(f"{remaining_seconds} second{'s' if remaining_seconds != 1 else ''}")
    
    if not parts:
        return "0 seconds"
    
    return ", ".join(parts)

def format_duration_short(seconds):
    """Convert seconds into short format"""
    if seconds is None or seconds == "Not available":
        return "N/A"
    
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "N/A"
    
    if seconds < 0:
        return "N/A"
    
    # Calculate days, hours, minutes
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    
    # Build the short formatted string
    parts = []
    
    if days > 0:
        parts.append(f"{days}d")
    
    if hours > 0:
        parts.append(f"{hours}h")
    
    if minutes > 0:
        parts.append(f"{minutes}m")
    
    # Show seconds if less than a minute
    if seconds < 60:
        parts.append(f"{remaining_seconds}s")
    
    if not parts:
        return "0s"
    
    return " ".join(parts)

@login_required
def history_view(request):
    """Display user history with filtering"""
    user_history, created = UserHistory.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        filter_form = HistoryFilterForm(request.POST)
        if filter_form.is_valid():
            # Apply filters (simplified for demo)
            date_from = filter_form.cleaned_data.get('date_from')
            date_to = filter_form.cleaned_data.get('date_to')
            min_visits = filter_form.cleaned_data.get('min_visits')
            
            # In a real application, you would filter the history data
            # For now, we'll just show the current history
            pass
    else:
        filter_form = HistoryFilterForm()
    
    # Get session expiry age (time remaining until expiration)
    session_age = request.session.get_expiry_age()
    session_age_formatted = format_duration(session_age)
    session_age_short = format_duration_short(session_age)
    
    context = {
        'user_history': user_history,
        'filter_form': filter_form,
        'last_viewed_donation_id': request.COOKIES.get('last_viewed_donation_id'),
        'session_age_formatted': session_age_formatted,
        'session_age_short': session_age_short,
        'session_age': session_age,
    }
    
    return render(request, 'donations/history.html', context)


@login_required
def comment_create(request, donation_id):
    """Create a comment on a donation"""
    donation = get_object_or_404(Donation, pk=donation_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.donation = donation
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('donations:donation_detail', pk=donation_id)


@login_required
def upload_view(request, donation_id):
    """Upload photos for a donation"""
    donation = get_object_or_404(Donation, pk=donation_id)
    
    # Check if user is the donor
    if donation.donor != request.user:
        messages.error(request, 'You can only upload photos for your own donations.')
        return redirect('donations:donation_detail', pk=donation_id)
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.donation = donation
            photo.save()
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('donations:donation_detail', pk=donation_id)
    else:
        form = UploadForm()
    
    context = {
        'form': form,
        'donation': donation,
    }
    return render(request, 'donations/upload.html', context)


@login_required
def footer_manage(request):
    """Manage footer links (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('donations:donation_list')
    
    if request.method == 'POST':
        form = FooterLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Footer link added successfully!')
            return redirect('donations:footer_manage')
    else:
        form = FooterLinkForm()
    
    footer_links = FooterLink.objects.all()
    context = {
        'form': form,
        'footer_links': footer_links,
    }
    return render(request, 'donations/footer.html', context)


# Authentication Views
def signup_view(request):
    """Enhanced user registration view with account type selection"""
    if request.method == 'POST':
        form = AccountTypeSignupForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()
            
            # Create profile based on account type
            account_type = form.cleaned_data['account_type']
            
            if account_type == 'donor':
                # Create donor profile
                donor = Donor.objects.create(
                    user=user,
                    business_name=form.cleaned_data['business_name'],
                    business_type=form.cleaned_data['business_type'],
                    contact_phone=form.cleaned_data['contact_phone'],
                    contact_email=form.cleaned_data['contact_email'],
                    address=form.cleaned_data['address'],
                    zip_code=form.cleaned_data['zip_code'],
                    business_hours=form.cleaned_data['business_hours'],
                    description=form.cleaned_data['description']
                )
                messages.success(request, f'Donor account created successfully! Welcome to Food Rescue, {donor.business_name}!')
            
            elif account_type == 'recipient':
                # Create recipient profile
                recipient = Recipient.objects.create(
                    user=user,
                    name=f"{user.first_name} {user.last_name}",
                    contact_phone=form.cleaned_data['recipient_phone'],
                    contact_email=form.cleaned_data['recipient_email'],
                    address=form.cleaned_data['recipient_address'],
                    zip_code=form.cleaned_data['recipient_zip_code'],
                    dietary_preferences=form.cleaned_data['dietary_preferences']
                )
                messages.success(request, f'Recipient account created successfully! Welcome to Food Rescue, {recipient.name}!')
            
            login(request, user)
            return redirect('donations:donation_list')
    else:
        # Pre-select account type based on URL parameter
        account_type = request.GET.get('type', '')
        initial_data = {}
        if account_type in ['donor', 'recipient']:
            initial_data['account_type'] = account_type
        form = AccountTypeSignupForm(initial=initial_data)
    
    return render(request, 'registration/signup.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = 'donations:donation_list'


# Additional Views
@login_required
def recipient_create(request):
    """Create recipient profile"""
    if hasattr(request.user, 'recipient'):
        messages.info(request, 'You already have a recipient profile.')
        return redirect('donations:donation_list')
    
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.user = request.user
            recipient.save()
            messages.success(request, 'Recipient profile created successfully!')
            return redirect('donations:donation_list')
    else:
        form = RecipientForm()
    
    return render(request, 'donations/recipient_form.html', {'form': form})


@login_required
def recipient_update(request):
    """Update recipient profile"""
    try:
        recipient = request.user.recipient
    except Recipient.DoesNotExist:
        messages.error(request, 'You need to create a recipient profile first.')
        return redirect('donations:recipient_create')
    
    if request.method == 'POST':
        form = RecipientForm(request.POST, instance=recipient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipient profile updated successfully!')
            return redirect('donations:donation_list')
    else:
        form = RecipientForm(instance=recipient)
    
    return render(request, 'donations/recipient_form.html', {'form': form})


@login_required
def donor_create(request):
    """Create donor profile"""
    if hasattr(request.user, 'donor'):
        messages.info(request, 'You already have a donor profile.')
        return redirect('donations:donation_list')
    
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            messages.success(request, 'Donor profile created successfully!')
            return redirect('donations:donation_list')
    else:
        form = DonorForm()
    
    context = {
        'form': form,
        'is_update': False,
    }
    return render(request, 'donations/donor_form.html', context)


@login_required
def donor_update(request):
    """Update donor profile"""
    try:
        donor = request.user.donor
    except Donor.DoesNotExist:
        messages.error(request, 'You need to create a donor profile first.')
        return redirect('donations:donor_create')
    
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donor profile updated successfully!')
            return redirect('donations:donation_list')
    else:
        form = DonorForm(instance=donor)
    
    context = {
        'form': form,
        'is_update': True,
    }
    return render(request, 'donations/donor_form.html', context)


@login_required
def donation_status_update(request, pk):
    """Update donation status"""
    donation = get_object_or_404(Donation, pk=pk)
    
    # Check if user is the donor
    if donation.donor != request.user:
        messages.error(request, 'You can only update your own donations.')
        return redirect('donations:donation_detail', pk=pk)
    
    if request.method == 'POST':
        form = DonationStatusForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, f'Donation status updated to {donation.get_status_display()}.')
            return redirect('donations:donation_detail', pk=pk)
    else:
        form = DonationStatusForm(instance=donation)
    
    context = {
        'form': form,
        'donation': donation,
    }
    return render(request, 'donations/donation_status_form.html', context)


@login_required
def donation_delete(request, pk):
    """Delete a donation"""
    donation = get_object_or_404(Donation, pk=pk)
    
    # Check if user is the donor
    if donation.donor != request.user:
        messages.error(request, 'You can only delete your own donations.')
        return redirect('donations:donation_detail', pk=pk)
    
    if request.method == 'POST':
        form = DonationDeleteForm(request.POST)
        if form.is_valid():
            donation.delete()
            messages.success(request, 'Donation deleted successfully.')
            return redirect('donations:donation_list')
    else:
        form = DonationDeleteForm()
    
    context = {
        'form': form,
        'donation': donation,
    }
    return render(request, 'donations/donation_delete_confirm.html', context)


@login_required
def photo_delete(request, photo_id):
    """Delete a photo from a donation"""
    photo = get_object_or_404(PhotoUpload, pk=photo_id)
    
    # Check if user is the donor of the donation
    if photo.donation.donor != request.user:
        messages.error(request, 'You can only delete photos from your own donations.')
        return redirect('donations:donation_detail', pk=photo.donation.pk)
    
    donation_id = photo.donation.pk
    photo.delete()
    messages.success(request, 'Photo deleted successfully.')
    
    return redirect('donations:donation_detail', pk=donation_id)


def home_view(request):
    """Home page view"""
    # Show recent donations with different statuses, prioritizing available ones
    recent_donations = Donation.objects.filter(
        status__in=['available', 'reserved']
    ).order_by('-created_at')[:6]
    
    categories = Category.objects.all()
    stats = {
        'total_donations': Donation.objects.count(),
        'available_donations': Donation.objects.filter(status='available').count(),
        'reserved_donations': Donation.objects.filter(status='reserved').count(),
        'donated_donations': Donation.objects.filter(status='donated').count(),
        'total_users': User.objects.count(),
    }
    
    context = {
        'recent_donations': recent_donations,
        'categories': categories,
        'stats': stats,
    }
    return render(request, 'donations/home.html', context)
