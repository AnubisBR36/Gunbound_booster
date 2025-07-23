# GunBound Marketplace

## Overview

A Flask-based web marketplace for buying and selling GunBound game accounts. The application features user authentication, account listings, purchase tracking, and a responsive dark-themed interface. Built for Brazilian Portuguese users with a focus on security and user experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Authentication**: Session-based authentication with Werkzeug password hashing
- **Database**: SQLite (development) with PostgreSQL compatibility via environment variables

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5.3.0 with dark theme
- **JavaScript**: Vanilla JavaScript with Bootstrap components
- **Icons**: Font Awesome 6.0.0
- **Responsive Design**: Mobile-first approach using Bootstrap grid system

### Security Implementation
- Password hashing using Werkzeug's secure methods
- Session-based user authentication
- CSRF protection through Flask's session management
- Environment-based configuration for sensitive data

## Key Components

### Models (models.py)
- **User**: Handles user accounts with secure password storage
- **Account**: Manages GunBound account listings with status tracking
- **AccountPurchase**: Junction table for purchase history and relationships

### Routes (routes.py)
- **Authentication**: Login/logout/registration with validation
- **Marketplace**: Account browsing and listing functionality
- **Dashboard**: User profile and purchase history management
- **Content Pages**: Static content like videos and information

### Templates
- **Base Template**: Consistent navigation and layout structure
- **Responsive Design**: Mobile-optimized with Bootstrap components
- **Brazilian Portuguese**: All content localized for Brazilian users
- **Dark Theme**: Gaming-focused aesthetic with yellow accent colors

## Data Flow

1. **User Registration/Login**: 
   - Password hashing and secure storage
   - Session creation and management
   - Redirect to dashboard upon successful authentication

2. **Account Browsing**:
   - Query available accounts from database
   - Display with pagination and filtering capabilities
   - Real-time status updates (available/sold)

3. **Purchase Process**:
   - User authentication verification
   - Account availability checking
   - Purchase record creation with timestamp and price

4. **Dashboard Management**:
   - User profile information display
   - Purchase history with account details
   - Account management for sellers

## External Dependencies

### Frontend Dependencies (CDN)
- Bootstrap 5.3.0 CSS/JS
- Font Awesome 6.0.0 icons
- Standard web fonts (Segoe UI family)

### Python Dependencies
- Flask web framework
- Flask-SQLAlchemy for database operations
- Werkzeug for security utilities
- SQLAlchemy ORM with declarative base

### Development Tools
- Logging configured for debugging
- ProxyFix middleware for deployment compatibility
- Environment variable configuration support

## Deployment Strategy

### Database Configuration
- **Production Database**: PostgreSQL with full environment integration
- **Connection**: Using DATABASE_URL, PGHOST, PGUSER, PGPASSWORD, PGDATABASE, PGPORT
- **Connection Pooling**: Configured with pool_recycle and pre_ping options for reliability
- **Tables**: User accounts, GunBound account listings, and purchase history tracking

### Application Configuration
- **Secret Key**: Environment-based session management
- **Debug Mode**: Configurable through main.py
- **Host/Port**: Configured for both local development (0.0.0.0:5000) and production deployment

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Flask session security key
- Fallback values provided for development environment

### Production Considerations
- ProxyFix middleware configured for reverse proxy deployment
- SQLAlchemy connection pooling for database reliability
- Structured logging for monitoring and debugging
- Session-based authentication suitable for load balancing

The application follows a traditional MVC pattern with clear separation of concerns, making it maintainable and scalable for a marketplace environment.