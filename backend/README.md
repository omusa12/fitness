# Fitness Application

A comprehensive fitness management system built with Django that allows trainers and clients to manage workouts, nutrition, and communication.

## Features

- User Management (Trainers & Clients)
- Workout Programs
- Exercise Library
- Nutrition Tracking
- Messaging System
- Client Progress Tracking

## Technical Stack

- Django
- SQLite
- HTML/CSS/JavaScript
- Bootstrap (for styling)

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create .env file with required environment variables
6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`

## Project Structure

- `fitness_app/` - Main project configuration
- `users/` - User management and authentication
- `workouts/` - Exercise and workout management
- `programs/` - Training program management
- `nutrition/` - Meal and nutrition tracking
- `messaging/` - Communication system
- `trainers/` - Trainer-specific functionality
