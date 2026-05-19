# not-twitter

A full-stack social media application built with Django REST Framework and React, featuring user authentication, profiles, posts, comments, likes, and follow functionality.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)

## Features

- **User Authentication**: JWT-based authentication with token refresh
- **User Profiles**: Create and manage user profiles with avatar, bio, and display names
- **Posts**: Create, and delete posts with media attachments
- **Comments**: Comment on posts with nested comment support
- **Likes**: Like posts and comments
- **Follow System**: Follow and unfollow other users
- **Feed**: Personalized feed based on followed users
- **CORS Support**: Cross-origin resource sharing enabled

## Tech Stack

### Backend

- **Framework**: Django 6.0+ with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **File Storage**: Cloudinary
- **Testing**: pytest, pytest-django, factory-boy
- **Python**: 3.12+

### Frontend

- **Framework**: React 19+
- **Build Tool**: Vite
- **Language**: TypeScript
- **State Management**: Redux Toolkit
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Routing**: React Router v7
- **Icons**: Lucide React

## Project Structure

```
not-twitter/
├── backend/              # Django REST API
│   ├── accounts/        # User authentication and profiles
│   ├── posts/           # Posts, comments, likes
│   ├── webhooks/        # External integrations
│   ├── app/             # Django project settings
│   ├── manage.py
│   ├── pyproject.toml   # Poetry dependencies
│   └── pytest.ini
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   ├── store/       # Redux store
│   │   └── utils/       # Utility functions
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Prerequisites

- **Python 3.12+** - Required for the backend
- **Node.js 18+** - Required for the frontend
- **PostgreSQL** - Database server
- **Git** - For version control

## Installation

### Backend Setup

1. **Navigate to the backend directory**:

   ```bash
   cd backend
   ```

2. **Create a Python virtual environment**:

   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Install dependencies using Poetry**:

   ```bash
   pip install poetry
   poetry install
   ```

5. **Create a `.env` file** in the backend directory:

   ```bash
   cp .env.example .env  # If template exists, or create manually
   ```

6. **Configure environment variables** in `.env`:

   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgresql://user:password@localhost:5432/not_twitter
   CLOUDINARY_CLOUD_NAME=your-cloudinary-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

7. **Run database migrations**:

   ```bash
   python manage.py migrate
   ```

8. **Create a superuser** (optional, for admin panel):
   ```bash
   python manage.py createsuperuser
   ```

### Frontend Setup

1. **Navigate to the frontend directory** (from project root):

   ```bash
   cd frontend
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Create a `.env` file** for frontend configuration:
   ```bash
   VITE_API_URL=http://localhost:8000/api
   ```

## Configuration

### Backend Configuration

Key settings in `backend/app/settings.py`:

- `ALLOWED_HOSTS`: Add your domain/IP
- `DATABASES`: Configure PostgreSQL connection
- `CORS_ALLOWED_ORIGINS`: Add frontend URL
- `CLOUDINARY_STORAGE`: Configure for media uploads

### Frontend Configuration

- API base URL in environment variables or service configuration
- Redux store initialization in `src/store/`

## Running the Application

### Start the Backend

From the `backend/` directory (with virtual environment activated):

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

To run on a different port:

```bash
python manage.py runserver 0.0.0.0:8080
```

### Start the Frontend

From the `frontend/` directory:

**Development mode**:

```bash
npm run dev
```

The application will be available at `http://localhost:5173/`

**Build for production**:

```bash
npm run build
```

### Run Both Simultaneously

Use two terminal windows:

1. Terminal 1: `cd backend && python manage.py runserver`
2. Terminal 2: `cd frontend && npm run dev`

## API Documentation

The API endpoints are organized by feature:

- **Authentication**: `/api/auth/` - Login, register, token refresh
- **Profiles**: `/api/profiles/` - User profile management
- **Posts**: `/api/posts/` - Create, retrieve, update, delete posts
- **Comments**: `/api/comments/` - Manage post comments
- **Likes**: `/api/likes/` - Like/unlike functionality
- **Feed**: `/api/feed/` - Personalized user feed
- **Follow**: `/api/follow/` - Follow/unfollow users

## Testing

### Run Backend Tests

From the `backend/` directory:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_views.py
```

Run with coverage:

```bash
pytest --cov=accounts --cov=posts
```

### Run Frontend Linting

From the `frontend/` directory:

```bash
npm run lint
```

### Frontend Build Check

```bash
npm run build
```
