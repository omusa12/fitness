# fitness_app_new

A new Flutter project.

## Getting Started

# Flutter Frontend Feature Implementation Guide

## 1. User Authentication & Role Management
### Screens:
- **Role Selection Screen**
- **Registration Screen** (Email + OAuth)
- **Login Screen**
- **Admin Dashboard** (Role management, analytics)

### Features:
- Firebase Auth integration for OAuth (Google/Apple)
- Role-based navigation flow
- Admin controls for user role assignment
- Secure token storage with flutter_secure_storage

---

## 2. Client Management (Trainer Perspective)
### Screens:
- **Client List View**
- **Client Profile Screen**
- **Progress Dashboard** (Charts/graphs)
- **AI Calorie Log Review**

### Features:
- DataGrid for client overview
- Chart widgets (Syncfusion/Flutter Charts)
- Comment system for calorie log feedback
- Push notifications for client updates

---

## 3. Workout Program Management
### Screens:
- **Workout Creator** (Drag-and-drop UI)
- **Template Library**
- **Program Assignment Screen**
- **Exercise Demo Gallery**

### Features:
- Interactive timeline widget for workout plans
- Video embedding for exercise demos
- Bulk selection for group assignments
- Progress tracking visualization

---

## 4. Community Features
### Screens:
- **Forum List View**
- **Thread Screen**
- **New Post Composition**
- **Notification Center**

### Features:
- Rich text editor for posts
- @mention functionality
- Real-time updates with Socket.io/Streams
- Moderation controls (delete/pin posts)

---

## 5. AI-Powered Nutrition Tracking
### Screens:
- **Camera Capture UI**
- **Meal Log Timeline**
- **Calorie Summary View**
- **Food Detail Overlay**

### Features:
- Image_picker integration with camera/gallery
- Loading states during AI processing
- Editable calorie adjustment interface
- Weekly/Monthly nutrition reports

---

## 6. Video Class Integration
### Screens:
- **Class Schedule Calendar**
- **Video Call Interface**
- **Recording Library**
- **Q&A Chat Overlay**

### Features:
- Twilio/Zoom SDK integration
- Screen sharing toggle
- Chat message persistence
- Recording playback with seek controls

---

## 7. Progress Tracking & Analytics
### Screens:
- **Personal Stats Dashboard**
- **Workout Completion Log**
- **Goal Tracking Interface**
- **Achievement System**

### Features:
- Interactive charts with date filtering
- Photo progress comparison slider
- Badge reward system
- Export to PDF functionality

---

## Technical Requirements:
### State Management:
- Provider/Riverpod for global state
- Bloc/Cubit for complex features
- Hive for local caching

### Key Packages:
- camera: ^0.10.0+1
- image_picker: ^0.8.7+3
- charts_flutter: ^0.12.0
- flutter_video_chat: ^1.0.0 (Twilio)
- firebase_core: ^2.8.0

### Performance Considerations:
- Image compression before upload
- Pagination for long lists
- Background sync for data updates
- Offline-first approach for critical data

---

## Testing Plan:
1. Widget tests for all core components
2. Integration tests for key user flows:
   - Photo upload → AI processing → Log entry
   - Workout creation → Assignment → Client tracking
3. Performance testing for video calls
4. Security testing for role-based access

---

## UI/UX Requirements:
- Consistent design system across all screens
- Accessibility compliance (WCAG 2.1)
- Localized text support
- Dark/light theme toggle
- Loading/error states for all async operations
