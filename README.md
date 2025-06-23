# 🛍️ QuantoxBay - Digital Marketplace for Creators

A modern, full-stack **Django-powered digital marketplace** where creators can sell their digital products (eBooks, icons, templates, etc.), with secure payments via Stripe and fast, reliable media delivery using Cloudinary.

---

## 🔗 Live Demo

🟢 [Visit QuantoxBay](https://quantoxbay.onrender.com/)


## 🚀 Features

### 👩‍💻 Seller Dashboard

* Upload digital products with descriptions, pricing, categories, thumbnails, and tags.
* Edit and manage listings.
* View **sales analytics** with total revenue and product performance.

### 💳 Secure Payments with Stripe

* Integrated Stripe Checkout for seamless and secure transactions.
* Auto-handle payment success/failure with redirects.
* Track order history, payment intent, and fulfillment status.

### 📦 Digital Product Management

* Upload files like `.pdf`, `.png`, `.zip`, etc.
* Auto-generate and display file size/type.
* Serve downloads only after successful payment.

### 📊 Sales Page with Charts

* Visualize your revenue growth over time using Chart.js.
* Filter and sort sales data.

### ☁️ Cloud-Based Media Storage

* Integrated **Cloudinary** for scalable file/image hosting.
* CDN-delivered thumbnails and product files.

### 📱 Mobile-Responsive UI

* Beautifully styled using **Tailwind CSS**.
* Optimized for phones, tablets, and desktops.

### 🔐 Authentication

* Custom login/signup views.
* Access control using Django decorators.
* Friendly redirects for unauthorized users.

---

## 🧰 Built With

| Stack         | Tech                                       |
| ------------- | ------------------------------------------ |
| Backend       | Django 5.2.3                               |
| Frontend      | HTML, Tailwind CSS                         |
| Payments      | Stripe                                     |
| Database      | PostgreSQL (via [Neon](https://neon.tech)) |
| Media Storage | Cloudinary                                 |
| Deployment    | Render                                     |

---

## 📂 Project Structure

```
digital_marketplace/
├── mysite/                # Main project
│   ├── settings.py        # Configurations (env, DB, Cloudinary, etc.)
│   ├── urls.py            # URL Routing
│   └── wsgi.py            # For deployment
├── myapp/                 # App: product + order + auth
│   ├── models.py          # Product, OrderDetail
│   ├── views.py           # All business logic
│   ├── templates/         # HTML templates
│   └── static/            # Tailwind CSS & JS
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
└── manage.py
```

---

## ⚙️ Installation & Setup

### 🔧 Local Development

```bash
git clone https://github.com/vedantmpatil/Quantoxbay.git
cd Quantoxbay
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
```

### 🔑 Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_django_secret
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
CLOUDINARY_CLOUD_NAME=dx1214141wgin8hu
CLOUDINARY_API_KEY=99149233417952624717
CLOUDINARY_API_SECRET=M8QX43XpU241El332LUE0z-jZtcZ5Kdt51oC4k
```

### 🛢️ Database (PostgreSQL via Neon)

* Create a Neon DB → Copy the connection string.
* Update `DATABASES` in `settings.py`.
* Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 🌐 Run Locally

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 💡 Core Models

### `Product`

* `title`, `description`, `price`, `discount_price`
* `file`, `thumbnail`, `file_size`, `file_type`
* `tags`, `category`, `seller`

### `OrderDetail`

* `customer_email`, `product`, `amount`
* `stripe_payment_intent`, `has_paid`, `created_on`

---

## 📦 Media Storage with Cloudinary

```python
from cloudinary_storage.storage import MediaCloudinaryStorage
file = models.FileField(upload_to='uploads/products/', storage=MediaCloudinaryStorage())
thumbnail = models.ImageField(upload_to='uploads/thumbnails/', storage=MediaCloudinaryStorage())
```

Files are served via:

```
https://res.cloudinary.com/<cloud_name>/image/upload/...
```

---

## 🧪 Testing

* Add products as an authenticated seller
* Test payment flow (Stripe test card)
* Download product only after payment success
* Check sales analytics

---

## 🚀 Deployment

### Render Setup

* Connect GitHub repo
* Add Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
* Add Start Command: `gunicorn mysite.wsgi`
* Set environment variables in Render Dashboard

### Render Tips

* Use PostgreSQL (like Neon) instead of SQLite
* Use Cloudinary for file persistence across rebuilds

---


## 🤝 Acknowledgments

* [Django](https://www.djangoproject.com/)
* [Stripe](https://stripe.com/)
* [Cloudinary](https://cloudinary.com/)
* [Render](https://render.com/)
* [Neon PostgreSQL](https://neon.tech/)
* [Tailwind CSS](https://tailwindcss.com/)

---

## 🧠 Creator

Made with ❤️ by [Vedant M. Patil](https://github.com/vedantmpatil) — Always building cool, real-world stuff.

---

## 🌟 If you liked this project...

Star it, fork it, or use it as a base for your next startup idea!

```bash
# Clone and start customizing
https://github.com/vedantmpatil/Quantoxbay
```
