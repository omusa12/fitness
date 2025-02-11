# Forum API Requirements

## Models Required

### ForumPost
```python
class ForumPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    media_url = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts')
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']
```

### ForumComment
```python
class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
```

## API Endpoints Required

### Posts

#### GET /api/forum/posts/
Get paginated list of forum posts
```json
Response:
{
    "posts": [
        {
            "id": "string",
            "user": {
                "id": "string",
                "username": "string",
                "avatar_url": "string"
            },
            "content": "string",
            "media_url": "string",
            "timestamp": "datetime",
            "like_count": "integer",
            "comment_count": "integer",
            "is_liked": "boolean"
        }
    ],
    "next_page": "string",
    "previous_page": "string"
}
```

#### POST /api/forum/posts/
Create a new forum post
```json
Request:
{
    "content": "string",
    "media_url": "string"
}

Response:
{
    "id": "string",
    "user": {
        "id": "string",
        "username": "string",
        "avatar_url": "string"
    },
    "content": "string",
    "media_url": "string",
    "timestamp": "datetime",
    "like_count": 0,
    "comment_count": 0,
    "is_liked": false
}
```

#### POST /api/forum/posts/{id}/like/
Toggle like on a post
```json
Response:
{
    "is_liked": "boolean",
    "like_count": "integer"
}
```

### Comments

#### GET /api/forum/posts/{id}/comments/
Get comments for a post
```json
Response:
{
    "comments": [
        {
            "id": "string",
            "user": {
                "id": "string",
                "username": "string",
                "avatar_url": "string"
            },
            "content": "string",
            "timestamp": "datetime"
        }
    ],
    "next_page": "string",
    "previous_page": "string"
}
```

#### POST /api/forum/posts/{id}/comments/
Add a comment to a post
```json
Request:
{
    "content": "string"
}

Response:
{
    "id": "string",
    "user": {
        "id": "string",
        "username": "string",
        "avatar_url": "string"
    },
    "content": "string",
    "timestamp": "datetime"
}
```

### Media Upload

#### POST /api/forum/upload/
Upload media for a post
```json
Request:
multipart/form-data
{
    "file": "binary"
}

Response:
{
    "url": "string"
}
```

## Implementation Requirements

1. Authentication & Authorization
   - All endpoints require authentication
   - Users can only edit/delete their own posts and comments
   - Implement rate limiting for post creation and likes

2. Media Handling
   - Support image uploads (JPEG, PNG)
   - Implement file size limits
   - Generate thumbnails for better performance
   - Store media files in cloud storage (e.g., S3)

3. Performance Considerations
   - Implement pagination for posts and comments
   - Cache frequently accessed posts
   - Optimize media delivery using CDN
   - Use database indexes for faster queries

4. Real-time Features
   - Implement WebSocket connections for:
     - New post notifications
     - Like updates
     - Comment notifications
   - Consider using Django Channels

5. Data Validation
   - Validate media file types and sizes
   - Sanitize text content
   - Implement profanity filters
   - Validate URLs

6. Error Handling
   - Implement proper error responses
   - Handle concurrent like operations
   - Manage file upload errors
   - Handle network timeouts

## Database Indexes
```python
class ForumPost:
    class Meta:
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user']),
        ]

class ForumComment:
    class Meta:
        indexes = [
            models.Index(fields=['post', 'timestamp']),
            models.Index(fields=['user']),
        ]
```

## Caching Strategy
1. Cache popular posts
2. Cache like counts
3. Cache user profiles
4. Implement cache invalidation on updates

## Testing Requirements
1. Unit tests for models and views
2. Integration tests for API endpoints
3. Load testing for concurrent operations
4. Media upload testing
5. WebSocket connection testing

## Security Considerations
1. Implement CORS policies
2. Validate file uploads
3. Prevent XSS attacks
4. Rate limit API endpoints
5. Implement request signing for media uploads