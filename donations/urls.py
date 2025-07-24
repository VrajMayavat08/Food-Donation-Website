from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),
    
    # Donation views
    path('donations/', views.DonationListView.as_view(), name='donation_list'),
    path('donations/create/', views.DonationCreateView.as_view(), name='donation_create'),
    path('donations/<int:pk>/', views.DonationDetailView.as_view(), name='donation_detail'),
    path('donations/<int:pk>/status/', views.donation_status_update, name='donation_status_update'),
    path('donations/<int:pk>/delete/', views.donation_delete, name='donation_delete'),
    
    # Pickup request views
    path('pickup-requests/', views.PickupRequestListView.as_view(), name='pickup_list'),
    path('donations/<int:donation_id>/request-pickup/', views.PickupRequestCreateView.as_view(), name='pickup_create'),
    
    # Function-based views
    path('history/', views.history_view, name='history'),
    path('donations/<int:donation_id>/comment/', views.comment_create, name='comment_create'),
    path('donations/<int:donation_id>/upload/', views.upload_view, name='upload'),
    path('photos/<int:photo_id>/delete/', views.photo_delete, name='photo_delete'),
    path('footer-manage/', views.footer_manage, name='footer_manage'),
    
    # Authentication views
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Recipient profile views
               path('recipient/create/', views.recipient_create, name='recipient_create'),
           path('recipient/update/', views.recipient_update, name='recipient_update'),
           path('donor/create/', views.donor_create, name='donor_create'),
           path('donor/update/', views.donor_update, name='donor_update'),
] 