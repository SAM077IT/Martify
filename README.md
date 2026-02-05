# 🛒 Martify

Martify is a full-featured **eCommerce web application** built with **Python & Django**, designed to sell **multi-category products** for the **US market**.  
The project focuses on clean architecture, scalability, and real-world eCommerce workflows such as cart management, checkout, payments, and order tracking.

---

## 🚀 Features

### 🧑‍💻 User Features
- User registration, login, and authentication
- Browse products by category
- Product search and filtering
- Session-based and persistent cart
- Add, update, and remove items from cart
- Secure checkout flow
- Order history and order details
- Address management
- Order confirmation emails

### 🛍️ Store & Admin Features
- Product and category management
- Inventory management
- Order management via Django Admin
- Coupon & discount support
- Shipping and tax calculation (basic)
- Payment integration (Stripe)
- Analytics & tracking ready

---

## 🏗️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** Django Templates, HTML, CSS (Tailwind/Bootstrap planned)
- **Database:** SQLite (development), PostgreSQL (production-ready)
- **Authentication:** Django Auth
- **Payments:** Stripe
- **Caching:** Redis (planned)
- **Task Queue:** Celery (planned)
- **Deployment:** Docker, Gunicorn (planned)

---

## 📁 Project Structure

martify/
│
├── manage.py
├── requirements.txt
├── README.md
├── .env
│
├── martify/ # Core project settings
│ ├── settings/
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
│
├── core/ # Homepage & base utilities
├── accounts/ # Authentication & profiles
├── products/ # Product catalog
├── cart/ # Cart logic (session + DB)
├── orders/ # Orders & checkout
├── payments/ # Payment integrations
├── coupons/ # Discounts & promotions
├── analytics/ # Analytics (optional)
│
├── templates/ # Global templates
├── static/ # Static files
└── media/ # Uploaded media


---

## ⚙️ Setup Instructions

1️⃣ Clone the repository
git clone https://github.com/SAM077IT/Martify.git
cd Martify

2️⃣ Create a virtual environment

Windows (PowerShell / Git Bash):

python -m venv venv


macOS / Linux:

python3 -m venv venv

3️⃣ Activate the virtual environment

Windows (PowerShell):

venv\Scripts\Activate


Windows (Git Bash):

source venv/Scripts/activate


macOS / Linux:

source venv/bin/activate


✅ You should see (venv) in your terminal.

4️⃣ Upgrade pip
python -m pip install --upgrade pip

5️⃣ Install dependencies
pip install django python-dotenv pillow stripe


(Optional – save dependencies)

pip freeze > requirements.txt

6️⃣ Create environment variables file

Create a .env file in the project root:

SECRET_KEY=your-secret-key
DEBUG=True

# Stripe Keys
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key


⚠️ Do not commit the .env file to GitHub.

7️⃣ Start the Django project
django-admin startproject martify .

8️⃣ Create Django apps
python manage.py startapp core
python manage.py startapp accounts
python manage.py startapp products
python manage.py startapp cart
python manage.py startapp orders
python manage.py startapp payments
python manage.py startapp coupons
python manage.py startapp analytics

9️⃣ Register apps in settings

Open:

martify/settings.py


Add the apps:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'core',
    'accounts',
    'products',
    'cart',
    'orders',
    'payments',
    'coupons',
    'analytics',
]

🔟 Run database migrations
python manage.py makemigrations
python manage.py migrate


