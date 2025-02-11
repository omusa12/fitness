# Fitness App API Documentation

## Overview
This document provides comprehensive documentation for the Fitness App REST API. The API enables client applications to interact with the fitness platform's core functionalities including user management, workout programs, nutrition tracking, messaging, and more.

## Base URL
```
https://api.fitnessapp.com/v1
```

## Authentication
The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Error Handling
The API uses conventional HTTP response codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error responses follow this format:
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Detailed error message"
    }
}
```

## API Endpoints

### Authentication

#### POST /auth/register
Register a new user.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CLIENT" // or "TRAINER"
}
```

**Response:**
```json
{
    "id": "user_id",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CLIENT",
    "token": "jwt_token"
}
```

#### POST /auth/login
Authenticate a user.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "securepassword"
}
```

**Response:**
```json
{
    "token": "jwt_token",
    "user": {
        "id": "user_id",
        "email": "user@example.com",
        "role": "CLIENT"
    }
}
```

### Programs

#### GET /programs
Get list of workout programs.

**Query Parameters:**
- `trainer_id` (optional): Filter by trainer
- `client_id` (optional): Filter by client
- `status` (optional): Filter by status (ACTIVE, COMPLETED, DRAFT)

**Response:**
```json
{
    "programs": [
        {
            "id": "program_id",
            "name": "Weight Loss Program",
            "description": "12-week weight loss program",
            "trainer": {
                "id": "trainer_id",
                "name": "Trainer Name"
            },
            "start_date": "2024-02-11",
            "status": "ACTIVE",
            "workouts": [
                {
                    "id": "workout_id",
                    "name": "Full Body Workout",
                    "description": "Complete full body workout routine",
                    "duration": 60,
                    "section_type": "WARMUP"
                }
            ]
        }
    ]
}
```

#### POST /programs
Create a new workout program.

**Request Body:**
```json
{
    "name": "Weight Loss Program",
    "description": "12-week weight loss program",
    "client_id": "client_id",
    "start_date": "2024-02-11",
    "workouts": [
        {
            "name": "Full Body Workout",
            "description": "Complete full body workout routine",
            "duration": 60,
            "section_type": "WARMUP",
            "exercises": [
                {
                    "exercise_id": "exercise_id",
                    "sets": 3,
                    "reps": 12,
                    "rest_time": 60
                }
            ]
        }
    ]
}
```

### Nutrition

#### GET /nutrition/meals
Get user's meal entries.

**Query Parameters:**
- `date` (optional): Filter by date (YYYY-MM-DD)
- `meal_type` (optional): Filter by meal type (BREAKFAST, LUNCH, DINNER, SNACK)

**Response:**
```json
{
    "meals": [
        {
            "id": "meal_id",
            "date": "2024-02-11",
            "meal_type": "BREAKFAST",
            "foods": [
                {
                    "id": "food_id",
                    "name": "Oatmeal",
                    "serving_size": "100g",
                    "calories": 307,
                    "protein": 10,
                    "carbs": 55,
                    "fat": 5
                }
            ],
            "total_calories": 307,
            "total_protein": 10,
            "total_carbs": 55,
            "total_fat": 5
        }
    ]
}
```

#### POST /nutrition/meals
Log a new meal entry.

**Request Body:**
```json
{
    "date": "2024-02-11",
    "meal_type": "BREAKFAST",
    "foods": [
        {
            "food_id": "food_id",
            "serving_size": "100g"
        }
    ]
}
```

### Messaging

#### GET /messages/conversations
Get user's conversations.

**Response:**
```json
{
    "conversations": [
        {
            "id": "conversation_id",
            "participants": [
                {
                    "id": "user_id",
                    "name": "User Name"
                }
            ],
            "last_message": {
                "id": "message_id",
                "content": "Message content",
                "sender_id": "user_id",
                "timestamp": "2024-02-11T10:30:00Z"
            },
            "unread_count": 2
        }
    ]
}
```

#### POST /messages/send
Send a new message.

**Request Body:**
```json
{
    "conversation_id": "conversation_id",
    "content": "Message content"
}
```

### Forum

#### GET /forum/posts
Get forum posts.

**Query Parameters:**
- `category` (optional): Filter by category
- `page` (optional): Page number for pagination
- `limit` (optional): Number of posts per page

**Response:**
```json
{
    "posts": [
        {
            "id": "post_id",
            "title": "Post title",
            "content": "Post content",
            "author": {
                "id": "user_id",
                "name": "Author Name"
            },
            "created_at": "2024-02-11T10:30:00Z",
            "category": "NUTRITION",
            "likes_count": 5,
            "comments_count": 3
        }
    ],
    "total": 100,
    "page": 1,
    "limit": 10
}
```

#### POST /forum/posts
Create a new forum post.

**Request Body:**
```json
{
    "title": "Post title",
    "content": "Post content",
    "category": "NUTRITION"
}
```

### Video Sessions

#### GET /sessions/live
Get available live sessions.

**Query Parameters:**
- `trainer_id` (optional): Filter by trainer
- `date` (optional): Filter by date (YYYY-MM-DD)
- `status` (optional): Filter by status (SCHEDULED, ONGOING, COMPLETED)

**Response:**
```json
{
    "sessions": [
        {
            "id": "session_id",
            "title": "HIIT Workout Session",
            "trainer": {
                "id": "trainer_id",
                "name": "Trainer Name"
            },
            "start_time": "2024-02-11T15:00:00Z",
            "duration": 60,
            "max_participants": 10,
            "current_participants": 5,
            "status": "SCHEDULED"
        }
    ]
}
```

#### POST /sessions/live
Create a new live session (Trainer only).

**Request Body:**
```json
{
    "title": "HIIT Workout Session",
    "start_time": "2024-02-11T15:00:00Z",
    "duration": 60,
    "max_participants": 10,
    "description": "High-intensity interval training session"
}
```

## Rate Limiting
The API implements rate limiting to ensure fair usage:
- Authentication endpoints: 5 requests per minute
- Other endpoints: 60 requests per minute

## Websocket Endpoints

### Real-time Messaging
```
ws://api.fitnessapp.com/ws/messages/{conversation_id}/
```

### Live Session Chat
```
ws://api.fitnessapp.com/ws/sessions/{session_id}/chat/
```

### Live Session Video Stream
```
ws://api.fitnessapp.com/ws/sessions/{session_id}/stream/
```

## SDK Examples
Code examples for common operations using our official SDKs will be provided in separate documentation.
