# Martify Architecture

## Overview

Martify is a full-featured eCommerce web application built with Django 5.2.8, targeting the US market. The application follows a modular app-based architecture with clear separation of concerns.

**Key Characteristics:**
- Monolithic Django application with multiple specialized apps
- Server-side rendering with Django templates
- MySQL database for data persistence
- Session-based and database-backed shopping cart
- Planned Stripe payment integration
- Multi-category product catalog with tagging

---

## Application Structure

### Core Apps

#### `core`
**Purpose:** Homepage, base utilities, and product catalog foundation

**Key Models:**
- `Category`: Product categories with images
- `Tag`: Product tags for filtering
- `Product`: Main product entity with pricing, images, SKU, description

**Responsibilities:**
- Serves the homepage
- Provides base templates and context processors
- Product and category data models

---

#### `cart`
**Purpose:** Shopping cart management

**Key Models:**
- `Cart`: Session-based cart storage
- `CartItem`: Individual items in a cart

**Responsibilities:**
- Add/remove/update cart items
- Calculate cart totals
- Support both session-based and persistent carts
- Coupon application logic

---

#### `orders`
**Purpose:** Order processing and checkout

**Key Models:**
- `Order`: Customer orders with status tracking
- `OrderItem`: Individual items within an order
- `ShippingAddress`: Delivery addresses
- `BillingAddress`: Billing addresses

**Responsibilities:**
- Checkout flow management
- Order creation from cart
- Order status tracking
- Address management

---

#### `users`
**Purpose:** User authentication and profiles

**Key Models:**
- Custom user model (if implemented) or extends Django's User

**Responsibilities:**
- User registration/login/logout
- Profile management
- Authentication middleware

---

#### `products`
**Purpose:** Product catalog management (admin-focused)

**Responsibilities:**
- Product CRUD operations (for staff)
- Inventory management
- Category/tag management interface

---

#### `payments`
**Purpose:** Payment gateway integration

**Key Models:**
- `Payment`: Payment transaction records

**Responsibilities:**
- Stripe integration (planned)
- Payment processing
- Payment status tracking
- Webhook handling

---

#### `coupons`
**Purpose:** Discount and promotion management

**Key Models:**
- `Coupon`: Discount codes with validity and discount types

**Responsibilities:**
- Coupon validation
- Discount calculation
- Coupon usage tracking

---

#### `wishlist`
**Purpose:** User wishlist functionality

**Key Models:**
- `Wishlist`: User's saved products

**Responsibilities:**
- Save products for later
- Move items to cart

---

#### `analytics`
**Purpose:** Tracking and reporting (optional)

**Responsibilities:**
- Sales analytics
- User behavior tracking
- Reporting dashboard

---

#### `blog`
**Purpose:** Content management

**Key Models:**
- `Blog`: Blog posts with categories and content

**Responsibilities:**
- Blog CRUD operations
- Content publishing
- SEO metadata

---

#### `ajax`
**Purpose:** Asynchronous request handlers

**Responsibilities:**
- Dynamic UI updates
- Real-time features
- API-like endpoints for frontend interactions

---

## Database Schema Overview

### Core Tables
- `core_category`
- `core_tag`
- `core_product` (FK to Category, Tag)

### Cart Tables
- `cart_cart` (linked to user/session)
- `cart_cartitem` (FK to Cart, Product)

### Order Tables
- `orders_order` (FK to user, shipping/billing addresses)
- `orders_orderitem` (FK to Order, Product)

### Supporting Tables
- `coupons_coupon`
- `payments_payment` (FK to Order)
- `wishlist_wishlist` (FK to user, Product)
- `blog_blog`

---

## Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Backend | Django | 5.2.8 |
| Database | MySQL | (development & production) |
| Frontend | Django Templates + HTML/CSS | - |
| Static Assets | Django Static Files | - |
| Media | Django Media Files | - |
| Future | Redis (caching) | planned |
| Future | Celery (task queue) | planned |

---

## Key Workflows

### 1. User Registration & Authentication
1. User signs up → `users` app creates account
2. Session established via Django auth middleware
3. Redirect to homepage or intended destination

### 2. Browse & Add to Cart
1. User browses products from `core` app
2. Add to cart → `cart` app creates/updates CartItem
3. Cart stored in session and/or database

### 3. Checkout Process
1. User proceeds to checkout
2. `orders` app creates Shipping/Billing addresses
3. Coupon validation via `coupons` app
4. Order creation from cart items
5. Payment processing via `payments` app
6. Order confirmation and email

### 4. Order Management
1. Staff views orders via Django admin
2. Order status updates
3. Customer can view order history

---

## Development Patterns

### Django Conventions
- App-specific models, views, templates, URLs, admin
- Class-based views for most functionality
- Django forms for validation
- GET/POST pattern for form submissions

### Template Structure
```
templates/
├── base.html (main layout)
├── core/
│   ├── index.html
│   ├── product_detail.html
│   └── category_view.html
├── cart/
│   └── cart_detail.html
├── orders/
│   ├── checkout.html
│   └── order_complete.html
└── ... (per-app templates)
```

### Static Files
```
static/
├── css/
├── js/
├── images/
└── ...
```

### Media Files
- User-uploaded images stored in `media/`
- Product images, category images, user uploads
- Served via Django in development; CDN/whitenoise in production (to be configured)

---

## Configuration

### Settings
- `martify/settings.py`: Main settings module
- Database: MySQL configured (localhost, root user)
- Static and media URLs configured
- INSTALLED_APPS includes all Django defaults + local apps

### URLs
- `martify/urls.py`: Main URL configuration
- Each app has its own `urls.py` included via `include()`

---

## Current State & Future Plans

### Implemented
- User authentication (basic)
- Product catalog with categories and tags
- Shopping cart (session + DB)
- Basic checkout flow
- Order management
- Blog functionality
- Wishlist
- Coupon system (structure in place)

### Planned
- Stripe payment integration
- Redis caching
- Celery for async tasks (emails, order processing)
- Docker deployment
- Gunicorn for production
- Advanced analytics
- Search and filtering improvements
- Email confirmations
- Shipping/tax calculation

---

## Deployment Considerations

### Environment
- Python 3.x
- MySQL database (production)
- Web server: Gunicorn (planned) + Nginx/Apache
- Static files: Whitenoise or S3/CDN
- Environment variables for secrets

### Security
- Secret key management via `.env`
- Debug disabled in production
- Allowed hosts configured
- HTTPS enforcement
- CSRF protection enabled
- SQL injection protection via Django ORM

---

## Development Workflow

1. Create/modify models → `makemigrations` → `migrate`
2. Update views and URLs
3. Create/modify templates
4. Test locally
5. Commit with clear messages
6. Push to remote

---

## Contributing

See `CONTRIBUTING.md` for contribution guidelines (to be added).

---

## License

Proprietary - All rights reserved by project owner.
