# Shortify (Django, PostgreSQL, Redis, Celery, Docker)

🚀 A **scalable URL shortening service** built with Django, PostgreSQL, Redis, and Celery. Supports **async tasks, caching, and background analytics processing** using Dockerized microservices.

## 🌟 Features

✅ Shorten long URLs and generate unique short links  
✅ Redirect users from short URLs to original links  
✅ Store URLs in **PostgreSQL** with efficient indexing  
✅ **Redis caching** for high-speed URL lookups  
✅ **Celery for background tasks** (e.g., tracking click analytics)  
✅ **Dockerized setup** for easy deployment

---

## 📌 Tech Stack

- **Backend:** Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Caching:** Redis
- **Background Tasks:** Celery + Redis
- **Containerization:** Docker + Docker Compose
- **Web Server:** Gunicorn

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Pradhansumit/URL_Shortner.git
cd URL_Shortner
```

### 2️⃣ Create & Configure Environment Variables

Create a `.env` file in the root directory:

```ini
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=*
DATABASE_URL=postgres://myuser:password@pgdb:5432/url_shortner
REDIS_URL=redis://redis:6379/0
```

### 3️⃣ Run with Docker

```bash
docker-compose up --build
```

This will spin up:

- **Django API** on `http://localhost:8000/`
- **PostgreSQL DB**
- **Redis Cache**
- **Celery Worker**

---

## 📡 API Endpoints

### 1️⃣ Shorten a URL

**Request:**

```http
POST /api/shortner/
Content-Type: application/json
{
    "original_url": "https://example.com/very-long-url"
}
```

**Response:**

```json
{
  "short_url": "http://localhost:8000/api/hxYz1a"
}
```

### 2️⃣ Redirect from Short URL

```http
GET /s/hxYz1a/
```

Redirects to the original URL.

---

## 📦 Project Structure

```
URL_Shortner/
│── api/                 # Django app handling API
│── config/              # Django project settings
│   ├── settings.py      # Main configuration
│   ├── urls.py          # Project URLs
│   ├── wsgi.py          # WSGI entry point
│── docker/              # Docker configurations
│── docker-compose.yml   # Docker Compose services
│── Dockerfile           # Docker container setup
│── requirements.txt     # Project dependencies
│── .env                 # Environment variables (not committed)
│── .gitignore           # Ignore unnecessary files
│── README.md            # Project documentation
```

---

## 🛠 Running Celery Worker

Celery handles background jobs (e.g., tracking click analytics).  
Start the worker manually if needed:

```bash
docker-compose run celery
```

---

## 📜 License

This project is licensed under the **MIT License**.

🚀 **Contributions are welcome!** Feel free to fork and submit a PR.
