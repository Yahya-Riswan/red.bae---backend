# 🛒 RedBae — Django E-Commerce API

A powerful and modular eCommerce backend built using **Django** and **Django REST Framework**.  
It includes authentication, product management, carts, wishlist, and order APIs — ready to integrate with any frontend.

---

## ✨ Features

- 🔐 User Authentication (register, login, user CRUD)
- 🛍️ Product listings (PC, Laptops, Parts) + Admin CRUD
- 🛒 Cart management (add, update, delete, clear)
- ❤️ Wishlist system
- 📦 Order creation, payment verification, admin order management
- 📁 Media file handling

---


## 🔗 API Endpoints

### **AUTH — `/api/auth/`**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register/` | Register user |
| POST | `/login/` | Login user |
| GET/POST | `/users/` | User list & create |
| GET/PUT/DELETE | `/users/<id>/` | User detail operations |

---

### **PRODUCTS — `/api/products/`**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/` | Admin — all products |
| GET | `/admin/<pk>/` | Admin — product detail |
| GET | `/PC/` | PC products |
| GET | `/Laptops/` | Laptop products |
| GET | `/Parts/` | Parts products |
| GET | `/<pk>/` | Single product detail |

---

### **CART — `/api/carts/`**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/` | Admin carts |
| GET/POST | `/<user_id>/` | User cart list / add item |
| PUT/DELETE | `/item/<pk>/` | Update or delete cart item |
| DELETE | `/<user_id>/clear/` | Clear user cart |

---

### **WISHLIST — `/api/`**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST/DELETE | `/wishlist/<user_id>/` | User wishlist |
| GET | `/admin/wishlist/` | Admin wishlist |

---

### **ORDERS — `/api/`**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create-order/` | Create new order |
| POST | `/verify-payment/` | Verify payment |
| GET | `/orders/` | User orders |
| PUT | `/orders/<order_id>/` | Update order status (Admin) |
| GET | `/admin/orders/` | Admin – all orders |

---

## ⚙️ Installation Guide

### **1️⃣ Clone Repository**

```bash
git clone https://github.com/yourusername/redbae.git
cd redbae
```

### **2️⃣ Create Virtual Environment**

```bash
python -m venv env
source env/bin/activate      # macOS/Linux
env\Scripts\activate         # Windows
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4️⃣ Migrate Database**

```bash
python manage.py migrate
```

### **5️⃣ Run Development Server**

```bash
python manage.py runserver
```

---

### **📦 Media File Support**

All media uploads (images, product files, etc.) are served through:

```ini
MEDIA_URL  = /media/
MEDIA_ROOT = /media/
```

---

### **🧪 Testing The API**

You can test all routes using Postman or Insomnia.

Base URL:

```bash
http://localhost:8000/api/
```

---

### **📜 License**

This project is open-source and free to modify and use.

---

### **🤝 Contributing**

Pull requests are welcome!
For major changes, open an issue first to discuss your ideas.

---

### **⭐ Show Your Support**

If this repo helped you, consider giving it a star ⭐ on GitHub!

---

