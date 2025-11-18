# NGO Backend API

Django REST Framework backend for NGO management system.

## Setup Complete! 🎉

### Available API Endpoints:

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login

#### Campaigns
- `GET /api/campaigns/` - List all active campaigns
- `POST /api/campaigns/` - Create new campaign
- `GET /api/campaigns/{id}/` - Get campaign details
- `PUT /api/campaigns/{id}/` - Update campaign
- `DELETE /api/campaigns/{id}/` - Delete campaign

#### Events
- `GET /api/events/` - List all events
- `POST /api/events/` - Create new event

#### News
- `GET /api/news/` - List all news
- `POST /api/news/` - Create new news

#### Newsletter
- `GET /api/newsletter/` - List all subscribers
- `POST /api/newsletter/` - Subscribe to newsletter

#### Donations
- `GET /api/donations/` - List all donations
- `POST /api/donations/` - Make a donation

### Next Steps:

1. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

2. **Start Development Server:**
   ```bash
   python manage.py runserver
   ```

3. **Access Admin Panel:**
   - URL: http://127.0.0.1:8000/admin/
   - Add sample data through admin interface

4. **Test API:**
   ```bash
   python test_api.py
   ```

### Features Included:
- ✅ User authentication with tokens
- ✅ Campaign management with progress tracking
- ✅ Event management
- ✅ News management
- ✅ Image upload support
- ✅ CORS enabled for frontend
- ✅ Admin interface configured
- ✅ API documentation ready

### Frontend Integration:
- Base URL: `http://127.0.0.1:8000/api/`
- CORS enabled for `localhost:3000`
- Token-based authentication