# Excess Food Rescue Network

A Django web application that connects surplus food donors with recipients in the community to reduce food waste and build stronger local communities.

## 🌱 Project Overview

**Excess Food Rescue Network** is a green-tech platform designed to:
- Reduce food waste and methane emissions
- Connect restaurants, grocers, and home cooks with shelters and neighbors in need
- Build local community resilience
- Provide a sustainable solution for surplus food distribution

## 🚀 Features

### Core Functionality
- **Donation Management**: Post, browse, and manage food donations
- **Pickup Requests**: Request and track food pickups
- **User Profiles**: Separate donor and recipient profiles
- **Photo Uploads**: Add photos to donations with validation
- **Comments System**: Community interaction on donations
- **Search & Filtering**: Advanced search with category and location filters

### Technical Features
- **Authentication**: Complete user registration, login, logout, and password reset
- **Class-Based Views**: Modern Django views for better code organization
- **Bootstrap 5**: Responsive, mobile-friendly UI
- **File Uploads**: Image upload with validation and storage
- **Sessions & Cookies**: User activity tracking and history
- **Admin Interface**: Full Django admin integration
- **JSON Fixtures**: Initial data loading for categories and footer links

### Models Implemented
- `Donation`: Food items with details, expiry dates, and location
- `Category`: Food categories (Produce, Dairy, Bakery, etc.)
- `PickupRequest`: Requests linking users and donations
- `Recipient`: User profiles for food recipients
- `UserHistory`: Session tracking and user activity
- `Comment`: Community comments on donations
- `PhotoUpload`: Image uploads for donations
- `FooterLink`: Manageable footer links

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Python**: 3.10+
- **Image Processing**: Pillow
- **Authentication**: Django built-in auth system

## 📋 Requirements

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd food-rescue-network
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install django==4.2.7 pillow
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Load Initial Data
```bash
python manage.py loaddata categories.json footer_links.json
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

### 9. Access the Application
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Default Admin**: username: `admin`, password: `admin123`

## 📁 Project Structure

```
food_rescue_network/
├── donations/                 # Main app
│   ├── migrations/           # Database migrations
│   ├── fixtures/             # Initial data
│   │   ├── categories.json
│   │   └── footer_links.json
│   ├── templates/            # App-specific templates
│   ├── admin.py             # Admin configuration
│   ├── forms.py             # All forms
│   ├── models.py            # Database models
│   ├── views.py             # Views and logic
│   └── urls.py              # URL routing
├── food_rescue_network/      # Project settings
│   ├── settings.py          # Django settings
│   └── urls.py              # Main URL configuration
├── templates/               # Global templates
│   ├── base.html           # Base template
│   ├── donations/          # App templates
│   └── registration/       # Auth templates
├── static/                 # Static files
├── media/                  # Uploaded files
├── manage.py              # Django management
└── README.md              # This file
```

## 🎯 Key Features Implementation

### 1. Models & Database
- **8 Models**: Complete data structure for food rescue operations
- **Relationships**: Proper foreign keys and many-to-many relationships
- **Validation**: Form validation and model constraints

### 2. Forms (8 Total)
- `DonationForm`: Create and edit donations
- `CategoryForm`: Manage food categories
- `PickupRequestForm`: Request food pickups
- `RecipientForm`: User profile management
- `HistoryFilterForm`: Filter user activity
- `CommentForm`: Add comments to donations
- `UploadForm`: Photo upload with validation
- `FooterLinkForm`: Manage footer links

### 3. Views (8+ Total)
**Class-Based Views:**
- `DonationListView`: Browse donations with search/filter
- `DonationCreateView`: Create new donations
- `DonationDetailView`: View donation details
- `PickupRequestListView`: User's pickup requests
- `PickupRequestCreateView`: Create pickup requests

**Function-Based Views:**
- `history_view`: User activity tracking
- `comment_create`: Add comments
- `upload_view`: Photo uploads
- `footer_manage`: Admin footer management

### 4. Templates (8+ Total)
- `home.html`: Landing page with statistics
- `donation_list.html`: Browse donations with search
- `donation_form.html`: Create/edit donations
- `donation_detail.html`: View donation with comments
- `pickup_list.html`: User's pickup requests
- `pickup_form.html`: Request pickups
- `history.html`: User activity history
- `upload.html`: Photo upload interface
- `footer.html`: Footer link management
- Authentication templates (signup, login)

### 5. Authentication System
- User registration with custom form
- Login/logout functionality
- Password reset via email
- User profile management
- Session tracking

### 6. Search & Filtering
- Free-text search across donations
- Category-based filtering
- ZIP code filtering
- Pagination for results

### 7. File Uploads
- Image upload with validation
- File type restrictions (JPG, PNG, GIF)
- File size limits (5MB max)
- Media file serving

### 8. Sessions & Cookies
- User visit tracking
- Last viewed donation tracking
- Session management
- Activity history

### 9. Responsive Design
- Bootstrap 5 framework
- Mobile-friendly interface
- Modern UI components
- Consistent styling

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Database Configuration
**Development (SQLite):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'food_rescue_db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📊 Admin Interface

Access the Django admin at `/admin/` to:
- Manage all models
- View user activity
- Monitor donations and requests
- Manage categories and footer links
- Handle user accounts

## 🌐 Deployment

### Production Checklist
1. Set `DEBUG = False`
2. Configure production database
3. Set up static file serving
4. Configure media file storage
5. Set up email backend
6. Configure security settings
7. Set up HTTPS

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **AWS**: Scalable cloud hosting
- **DigitalOcean**: VPS hosting
- **PythonAnywhere**: Python-focused hosting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- Food rescue organizations for inspiration
- Open source contributors

## 📞 Support

For support or questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Built with ❤️ for a sustainable future** 