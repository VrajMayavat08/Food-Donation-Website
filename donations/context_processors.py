from .models import FooterLink

def footer_links(request):
    """Make footer links available globally"""
    return {
        'footer_links': FooterLink.objects.filter(is_active=True).order_by('order')
    } 