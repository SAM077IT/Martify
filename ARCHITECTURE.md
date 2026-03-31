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
**Purpose:** Homepage, base utilities, product catalog, and templatetags

**Key Models:**
- `Category`: Product categories with images
- `Tag`: Product tags for filtering
- `Product`: Main product entity with pricing, images, SKU, description, and `sale_price` property

**Responsibilities:**
- Serves the homepage (`IndexView`)
- Product catalog (`ShopView`, `CategoryView`, `ProductView`)
- Provides base templates and context processors
- Custom template tags and filters (`core_tags`)
- Static pages (contact, about, etc.)

**Important Files:**
- `templatetags/core_tags.py`: Custom template filter `underscore` for URL name conversion
- `views.py`: Class-based views for all core pages
- `urls.py`: URL routing for product, category, and static pages

---

#### `cart`
**Purpose:** Shopping cart management with hybrid session/database persistence

**Key Models:**
- `Cart`: Persistent cart storage linked to authenticated users (OneToOne with User)
- `CartItem`: Individual items in a cart

**Key Classes:**
- `SessionCart` (`cart/cart.py`): Session-based cart for all users (guests + authenticated)
- `utils.py`: Synchronization utilities (`sync_cart_to_db()`, `load_db_cart_into_session()`)
- `signals.py`: Authentication signal handlers for automatic cart sync

**Responsibilities:**
- Add/remove/update cart items via session storage
- Calculate cart totals and discounts
- Support both session-based (guests) and persistent carts (authenticated users)
- Automatic synchronization between session and database:
  - **On login**: Merge guest session cart with existing DB cart, synchronize DB, reload session
  - **During session**: Real-time sync for logged-in users after every cart operation
  - **On logout**: No action needed (DB already current)
  - **Empty cart cleanup**: Delete DB cart when empty
- Coupon application logic (via coupon ID in session)

**Files:**
- `cart.py`: SessionCart implementation
- `utils.py`: Cart synchronization utilities
- `signals.py`: `user_logged_in` and `user_logged_out` signal handlers
- `apps.py`: Registers signal handlers in `ready()` method
- `views.py`: Cart add/remove/clear with automatic sync for authenticated users
- `context_processors.py`: `cart_context` provides global cart access (via `core/context_processors.py`)
- `templatetags/core_tags.py`: `underscore` filter for product URL generation

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
- `core_category`: Product categories with image
- `core_tag`: Product tags for filtering
- `core_product`: Main product entity with:
  - Pricing fields (price, off_percent, computed sale_price property)
  - Images (main, secondary)
  - Foreign keys: category, tag
  - SKU, description, created_at

### Cart Tables
- `cart_cart`: Persistent cart linked to authenticated user (OneToOne)
- `cart_cartitem`: Line items linking Cart → Product with quantity
- Session-based cart stored in `request.session['cart']` (non-persistent)

**Note:** The database cart is synchronized to match the session cart for all authenticated users. Guests only use session storage.

### Order Tables
- `orders_order`: Customer orders with status, total, timestamps
- `orders_orderitem`: Order line items (FK to Order, Product)

### Supporting Tables
- `coupons_coupon`: Discount codes with validity, discount type, usage tracking
- `payments_payment`: Payment transactions (FK to Order)
- `wishlist_wishlist`: User saved products
- `blog_blog`: Blog posts with categories, content, metadata
- `users_<custom>`: Custom user model if implemented

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

### 2. Cart Persistence & Synchronization
**Guest Shopping:**
1. User (not logged in) adds items to cart → stored in session via `SessionCart`
2. Cart persists across pages but not browser restarts

**First Login with Existing Guest Cart:**
1. User adds items as guest → session cart contains items
2. User logs in → `user_logged_in` signal fires
3. Existing DB cart (if any) is loaded into session → **merged** with guest items
4. Combined session cart is **synchronized** to DB
5. Session cart is cleared and **reloaded from DB** (ensures consistency)
6. User now has persistent cart stored in database

**Authenticated Shopping:**
1. User is logged in and adds/removes items
2. Every cart operation immediately syncs DB cart to match session (in the view)
3. DB cart is always current (authoritative source)

**Logout:**
1. User logs out → `user_logged_out` signal fires
2. DB cart already current from real-time sync → no action needed
3. Session cart is cleared by Django's logout

**Browser Close (No Logout):**
- Cart remains in DB (synchronized from last operation)
- User can see their cart next time they log in

**Empty Cart Cleanup:**
- When cart becomes empty (all items removed), DB cart is automatically deleted
- Keeps database clean of unused empty carts

### 3. Browse & Add to Cart (Normal Flow)
1. User browses products from `core` app
2. Add to cart → `cart/views.py:cart_add` uses `SessionCart`
3. For logged-in users: `sync_cart_to_db()` updates DB in real-time
4. Cart count badge updates dynamically via `{{ cart|length }}`

### 4. Checkout Process
1. User proceeds to checkout
2. `orders` app creates Shipping/Billing addresses
3. Coupon validation via `coupons` app
4. Order creation from cart items
5. Cart is cleared (both session and DB)
6. Payment processing via `payments` app (Stripe integration planned)
7. Order confirmation and email

### 5. Order Management
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
- **Signal-based event handling**: Cart synchronization uses `user_logged_in`/`user_logged_out` signals
- **Context processors**: Global cart access via `core/context_processors.py`

### Template Structure
```
templates/
├── base.html (main layout with dynamic cart dropdown)
├── core/
│   ├── index.html (homepage)
│   ├── category.html (shop page with product grid)
│   ├── product.html (product detail with related products)
│   ├── page_about.html (about us page)
│   ├── contact.html (contact form)
│   ├── err404.html (404 error page)
│   ├── category-list.html (list view variant)
│   └── ... (other templates)
├── cart/
│   └── cart.html (dynamic cart detail page with live totals)
├── orders/
│   ├── checkout.html
│   └── order_complete.html
└── ... (per-app templates)
```

**Key Template Features:**
- **Global cart access**: All templates have access to `{{ cart }}` via context processor
- **Dynamic cart count**: Header displays `{{ cart|length }}`
- **Dynamic cart dropdown**: Base template iterates over cart items with product links

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
- `CART_SESSION_ID = 'cart'`: Session key for storing cart data

### URLs
- `martify/urls.py`: Main URL configuration
- Each app has its own `urls.py` included via `include()`

---

## Current State & Future Plans

### Implemented
- User authentication (basic)
- Product catalog with categories and tags
- **Shopping cart with hybrid persistence**:
  - Session-based cart works for guests and authenticated users
  - Database-backed cart automatically created for logged-in users
  - **Automatic synchronization** between session and database on login/logout
  - Real-time DB sync during session for logged-in users
  - Guest cart merges with existing DB cart on first login
  - Empty carts automatically deleted
  - Global cart context processor for templates
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
