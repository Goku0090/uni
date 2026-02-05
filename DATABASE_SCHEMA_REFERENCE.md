# UniSync Database Schema Reference

## User & Authentication Tables

### 1. `auth_user` (Django built-in)
Primary user authentication table.
```sql
CREATE TABLE auth_user (
  id INTEGER PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL,
  email VARCHAR(254) UNIQUE,
  password VARCHAR(128),
  first_name VARCHAR(150),
  last_name VARCHAR(150),
  is_staff BOOLEAN,
  is_active BOOLEAN,
  is_superuser BOOLEAN,
  date_joined TIMESTAMP,
  last_login TIMESTAMP
);
```

**Relationships**:
- StudentProfile (1:1)
- Project (1:M) - as owner
- Comment (1:M) - as author
- Message (1:M) - as sender/receiver
- Connection (1:M) - as sender/receiver
- Like (1:M)
- Follow (1:M)
- ChatRoom (1:M) - as owner
- Activity (1:M)
- Notification (1:M)

---

### 2. `accounts_studentprofile`
Extended user profile information.
```sql
CREATE TABLE accounts_studentprofile (
  id BIGINT PRIMARY KEY,
  user_id INT UNIQUE NOT NULL,
  full_name VARCHAR(100),
  college VARCHAR(200),
  other_college VARCHAR(200),
  location VARCHAR(100),
  interests JSONB DEFAULT '[]',  -- Array of interest tags
  bio TEXT,
  profile_photo VARCHAR(100),    -- File path
  skills JSONB DEFAULT '[]',      -- Array of skill tags
  project_interests JSONB DEFAULT '[]',
  role_preference VARCHAR(50),    -- Backend, Frontend, Full Stack, etc.
  github VARCHAR(200),            -- URL
  linkedin VARCHAR(200),          -- URL
  portfolio VARCHAR(200),         -- URL
  behance VARCHAR(200),           -- URL
  profile_completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
```

**Indexes**:
- user_id (UNIQUE)
- college
- profile_completed

---

### 3. `accounts_otp`
One-time password for authentication.
```sql
CREATE TABLE accounts_otp (
  id BIGINT PRIMARY KEY,
  email VARCHAR(254),
  otp_code VARCHAR(6),
  purpose VARCHAR(20),           -- login, registration, reset
  is_used BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP,
  expires_at TIMESTAMP
);
```

**Indexes**:
- email, purpose
- created_at

**Constraints**:
- Purpose values: login, registration, reset

---

## Social & Connection Tables

### 4. `accounts_connection`
Connection requests between users.
```sql
CREATE TABLE accounts_connection (
  id BIGINT PRIMARY KEY,
  sender_id INT NOT NULL,
  receiver_id INT NOT NULL,
  status VARCHAR(10) DEFAULT 'pending',  -- pending, accepted, rejected
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES auth_user(id),
  FOREIGN KEY (receiver_id) REFERENCES auth_user(id),
  UNIQUE(sender_id, receiver_id)
);
```

**Indexes**:
- sender_id, status
- receiver_id, status
- created_at

---

### 5. `accounts_follow`
Users following projects or other users.
```sql
CREATE TABLE accounts_follow (
  id BIGINT PRIMARY KEY,
  user_id INT NOT NULL,
  follows_user_id INT,              -- NULL if following project
  follows_project_id INT,           -- NULL if following user
  created_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id),
  FOREIGN KEY (follows_user_id) REFERENCES auth_user(id),
  FOREIGN KEY (follows_project_id) REFERENCES accounts_project(id)
);
```

**Constraints**:
- Either follows_user_id OR follows_project_id must be NOT NULL

---

### 6. `accounts_like`
Likes on projects and comments.
```sql
CREATE TABLE accounts_like (
  id BIGINT PRIMARY KEY,
  user_id INT NOT NULL,
  project_id INT,                  -- NULL if liking comment
  comment_id INT,                  -- NULL if liking project
  created_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id),
  FOREIGN KEY (project_id) REFERENCES accounts_project(id),
  FOREIGN KEY (comment_id) REFERENCES accounts_comment(id)
);
```

---

## Project Tables

### 7. `accounts_project`
Main project listings.
```sql
CREATE TABLE accounts_project (
  id BIGINT PRIMARY KEY,
  owner_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  visibility VARCHAR(20) DEFAULT 'draft',  -- public, private, draft
  status VARCHAR(20) DEFAULT 'planning',   -- planning, in_progress, completed, on_hold
  tags JSONB DEFAULT '[]',                 -- Array of technology tags
  collaboration_needs JSONB DEFAULT '[]',  -- Array of needed roles
  github_link VARCHAR(500),
  demo_link VARCHAR(500),
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (owner_id) REFERENCES auth_user(id)
);
```

**Indexes**:
- owner_id
- visibility
- status
- created_at

**Full-text Search Index**:
- title, description (for search optimization)

---

### 8. `accounts_projectteam`
Team management for projects.
```sql
CREATE TABLE accounts_projectteam (
  id BIGINT PRIMARY KEY,
  project_id INT UNIQUE NOT NULL,
  name VARCHAR(255),
  description TEXT,
  created_at TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES accounts_project(id)
);
```

---

### 9. `accounts_projectteammember`
Team membership for projects.
```sql
CREATE TABLE accounts_projectteammember (
  id BIGINT PRIMARY KEY,
  team_id INT NOT NULL,
  user_id INT NOT NULL,
  role VARCHAR(50),                -- Lead, Developer, Designer, etc.
  joined_at TIMESTAMP,
  FOREIGN KEY (team_id) REFERENCES accounts_projectteam(id),
  FOREIGN KEY (user_id) REFERENCES auth_user(id),
  UNIQUE(team_id, user_id)
);
```

---

### 10. `accounts_projectteaminvitation`
Team membership invitations.
```sql
CREATE TABLE accounts_projectteaminvitation (
  id BIGINT PRIMARY KEY,
  team_id INT NOT NULL,
  email VARCHAR(254),
  invited_by_id INT NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',  -- pending, accepted, rejected
  created_at TIMESTAMP,
  FOREIGN KEY (team_id) REFERENCES accounts_projectteam(id),
  FOREIGN KEY (invited_by_id) REFERENCES auth_user(id)
);
```

---

### 11. `accounts_projecttask`
Individual tasks within projects.
```sql
CREATE TABLE accounts_projecttask (
  id BIGINT PRIMARY KEY,
  project_id INT NOT NULL,
  title VARCHAR(255),
  description TEXT,
  assigned_to_id INT,
  status VARCHAR(20) DEFAULT 'todo',  -- todo, in_progress, review, done
  priority VARCHAR(20) DEFAULT 'medium',
  due_date DATE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES accounts_project(id),
  FOREIGN KEY (assigned_to_id) REFERENCES auth_user(id)
);
```

---

### 12. `accounts_projectmilestone`
Project milestones/phases.
```sql
CREATE TABLE accounts_projectmilestone (
  id BIGINT PRIMARY KEY,
  project_id INT NOT NULL,
  name VARCHAR(255),
  description TEXT,
  due_date DATE,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES accounts_project(id)
);
```

---

## Comment Tables

### 13. `accounts_comment`
Comments on projects and activities.
```sql
CREATE TABLE accounts_comment (
  id BIGINT PRIMARY KEY,
  project_id INT,                  -- NULL for activity comments
  author_id INT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  is_edited BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (project_id) REFERENCES accounts_project(id),
  FOREIGN KEY (author_id) REFERENCES auth_user(id)
);
```

**Indexes**:
- project_id, created_at
- author_id

---

## Message Tables

### 14. `accounts_message`
Direct messages between users.
```sql
CREATE TABLE accounts_message (
  id BIGINT PRIMARY KEY,
  sender_id INT NOT NULL,
  receiver_id INT,                 -- NULL if sent to chat_room
  chat_room_id INT,                -- NULL if direct message
  content TEXT,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES auth_user(id),
  FOREIGN KEY (receiver_id) REFERENCES auth_user(id),
  FOREIGN KEY (chat_room_id) REFERENCES accounts_chatroom(id)
);
```

**Indexes**:
- sender_id, created_at
- receiver_id, is_read
- chat_room_id
- created_at

---

### 15. `accounts_messagefile`
File attachments for messages.
```sql
CREATE TABLE accounts_messagefile (
  id BIGINT PRIMARY KEY,
  message_id INT NOT NULL,
  file VARCHAR(100),
  file_name VARCHAR(255),
  file_size INT,
  mime_type VARCHAR(100),
  uploaded_at TIMESTAMP,
  FOREIGN KEY (message_id) REFERENCES accounts_message(id)
);
```

---

### 16. `accounts_messagereaction`
Emoji reactions on messages.
```sql
CREATE TABLE accounts_messagereaction (
  id BIGINT PRIMARY KEY,
  message_id INT NOT NULL,
  user_id INT NOT NULL,
  emoji VARCHAR(10),
  created_at TIMESTAMP,
  FOREIGN KEY (message_id) REFERENCES accounts_message(id),
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
```

---

### 17. `accounts_messagereadstatus`
Track message read status per user.
```sql
CREATE TABLE accounts_messagereadstatus (
  id BIGINT PRIMARY KEY,
  message_id INT NOT NULL,
  user_id INT NOT NULL,
  is_read BOOLEAN DEFAULT FALSE,
  read_at TIMESTAMP,
  FOREIGN KEY (message_id) REFERENCES accounts_message(id),
  FOREIGN KEY (user_id) REFERENCES auth_user(id),
  UNIQUE(message_id, user_id)
);
```

---

## Chat Tables

### 18. `accounts_chatroom`
Group chat rooms.
```sql
CREATE TABLE accounts_chatroom (
  id BIGINT PRIMARY KEY,
  name VARCHAR(255),
  description TEXT,
  owner_id INT NOT NULL,
  project_id INT,                  -- NULL if not linked to project
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (owner_id) REFERENCES auth_user(id),
  FOREIGN KEY (project_id) REFERENCES accounts_project(id)
);
```

---

### 19. `accounts_chatroommember`
Members of chat rooms.
```sql
CREATE TABLE accounts_chatroommember (
  id BIGINT PRIMARY KEY,
  chat_room_id INT NOT NULL,
  user_id INT NOT NULL,
  joined_at TIMESTAMP,
  FOREIGN KEY (chat_room_id) REFERENCES accounts_chatroom(id),
  FOREIGN KEY (user_id) REFERENCES auth_user(id),
  UNIQUE(chat_room_id, user_id)
);
```

---

## Activity & Notification Tables

### 20. `accounts_activity`
User activity log for feed.
```sql
CREATE TABLE accounts_activity (
  id BIGINT PRIMARY KEY,
  user_id INT NOT NULL,
  activity_type VARCHAR(50),       -- project_created, comment_added, etc.
  description TEXT,
  content_type_id INT,             -- For GenericForeignKey
  object_id INT,
  timestamp TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
```

**Indexes**:
- user_id, timestamp
- timestamp
- activity_type

---

### 21. `accounts_notification`
Notifications for users.
```sql
CREATE TABLE accounts_notification (
  id BIGINT PRIMARY KEY,
  user_id INT NOT NULL,
  notification_type VARCHAR(50),   -- connection_request, project_comment, etc.
  message TEXT,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP,
  data JSONB,                      -- Additional context (IDs, links)
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
```

**Indexes**:
- user_id, is_read
- user_id, created_at
- created_at

---

### 22. `accounts_userstatus`
User online status.
```sql
CREATE TABLE accounts_userstatus (
  id BIGINT PRIMARY KEY,
  user_id INT UNIQUE NOT NULL,
  is_online BOOLEAN DEFAULT FALSE,
  last_seen TIMESTAMP,
  status_message VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
```

---

## File & Storage Tables

### 23. `accounts_file`
General file storage.
```sql
CREATE TABLE accounts_file (
  id BIGINT PRIMARY KEY,
  owner_id INT NOT NULL,
  file_name VARCHAR(255),
  file VARCHAR(100),
  file_size INT,
  mime_type VARCHAR(100),
  uploaded_at TIMESTAMP,
  FOREIGN KEY (owner_id) REFERENCES auth_user(id)
);
```

---

## Social Apps Tables (Django-Allauth)

### 24. `socialaccount_socialapp`
OAuth app configurations.
```sql
CREATE TABLE socialaccount_socialapp (
  id INTEGER PRIMARY KEY,
  provider VARCHAR(30),            -- google, github
  name VARCHAR(40),
  client_id VARCHAR(191),
  secret VARCHAR(191)
);
```

---

### 25. `socialaccount_socialaccount`
User social account links.
```sql
CREATE TABLE socialaccount_socialaccount (
  id BIGINT PRIMARY KEY,
  user_id INT NOT NULL,
  provider VARCHAR(30),
  uid VARCHAR(255),
  extra_data JSONB,
  date_joined TIMESTAMP,
  last_login TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
```

---

### 26. `accounts_userstats`
User statistics tracking.
```sql
CREATE TABLE accounts_userstats (
  id BIGINT PRIMARY KEY,
  user_id INT UNIQUE NOT NULL,
  total_projects INT DEFAULT 0,
  total_contributions INT DEFAULT 0,
  total_connections INT DEFAULT 0,
  profile_views INT DEFAULT 0,
  updated_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
```

---

## Query Examples

### Get All Projects by User
```sql
SELECT * FROM accounts_project 
WHERE owner_id = 123 
ORDER BY created_at DESC;
```

### Get All Accepted Connections for User
```sql
SELECT * FROM accounts_connection 
WHERE (sender_id = 123 OR receiver_id = 123)
AND status = 'accepted'
ORDER BY updated_at DESC;
```

### Get Recent Messages for User
```sql
SELECT m.*, u.username, u.email
FROM accounts_message m
JOIN auth_user u ON m.sender_id = u.id
WHERE m.receiver_id = 123
ORDER BY m.created_at DESC
LIMIT 20;
```

### Get Comments for Project with Author Info
```sql
SELECT c.*, u.username, u.email, p.full_name
FROM accounts_comment c
JOIN auth_user u ON c.author_id = u.id
JOIN accounts_studentprofile p ON u.id = p.user_id
WHERE c.project_id = 1
ORDER BY c.created_at DESC;
```

### Get Unread Notifications
```sql
SELECT * FROM accounts_notification
WHERE user_id = 123 AND is_read = FALSE
ORDER BY created_at DESC;
```

### Get Chat Rooms for User
```sql
SELECT cr.* 
FROM accounts_chatroom cr
JOIN accounts_chatroommember crm ON cr.id = crm.chat_room_id
WHERE crm.user_id = 123
ORDER BY cr.created_at DESC;
```

### Get User Statistics
```sql
SELECT 
  u.id, u.username,
  COUNT(DISTINCT p.id) as total_projects,
  COUNT(DISTINCT c.id) as total_connections,
  COUNT(DISTINCT f.id) as total_following
FROM auth_user u
LEFT JOIN accounts_project p ON u.id = p.owner_id
LEFT JOIN accounts_connection c ON (u.id = c.sender_id OR u.id = c.receiver_id) AND c.status = 'accepted'
LEFT JOIN accounts_follow f ON u.id = f.user_id
WHERE u.id = 123
GROUP BY u.id;
```

---

## Key Relationships (ER Summary)

```
User (1) --> (M) StudentProfile
User (1) --> (M) Project (as owner)
User (1) --> (M) Comment
User (1) --> (M) Message
User (1) --> (M) Connection (sender/receiver)
User (1) --> (M) Follow
User (1) --> (M) Like
User (1) --> (M) Activity
User (1) --> (M) Notification
User (1) --> (M) ChatRoom (as owner)

Project (1) --> (M) Comment
Project (1) --> (M) ProjectTeam
Project (1) --> (M) ProjectTask
Project (1) --> (M) ProjectMilestone
Project (1) --> (M) Like
Project (1) --> (M) Follow

ProjectTeam (1) --> (M) ProjectTeamMember
ProjectTeam (1) --> (M) ProjectTeamInvitation

ChatRoom (1) --> (M) ChatRoomMember
ChatRoom (1) --> (M) Message

Message (M) --> (1) ChatRoom
Message (1) --> (M) MessageFile
Message (1) --> (M) MessageReaction
Message (1) --> (M) MessageReadStatus
```

---

## Performance Optimization

### Recommended Indexes

```sql
-- User lookups
CREATE INDEX idx_user_email ON auth_user(email);
CREATE INDEX idx_user_username ON auth_user(username);

-- Project searches
CREATE INDEX idx_project_owner ON accounts_project(owner_id);
CREATE INDEX idx_project_visibility ON accounts_project(visibility);
CREATE INDEX idx_project_created ON accounts_project(created_at DESC);

-- Message queries
CREATE INDEX idx_message_receiver_read ON accounts_message(receiver_id, is_read);
CREATE INDEX idx_message_chatroom ON accounts_message(chat_room_id);

-- Connection queries
CREATE INDEX idx_connection_receiver_status ON accounts_connection(receiver_id, status);

-- Comment queries
CREATE INDEX idx_comment_project ON accounts_comment(project_id, created_at DESC);

-- Notification queries
CREATE INDEX idx_notification_user_read ON accounts_notification(user_id, is_read, created_at DESC);

-- Full-text search (PostgreSQL)
CREATE INDEX idx_project_search ON accounts_project USING GIN (to_tsvector('english', title || ' ' || description));
```

---

## Backup & Maintenance

### Backup Command
```bash
python manage.py dumpdata > backup.json
```

### Restore Command
```bash
python manage.py loaddata backup.json
```

### Database Optimization
```sql
VACUUM ANALYZE;  -- PostgreSQL optimization
```

---

## Summary

The UniSync database includes 26 main tables organized into:
- **User Management**: auth_user, StudentProfile, OTP
- **Social Features**: Connection, Follow, Like
- **Projects**: Project, ProjectTeam, ProjectTask, ProjectMilestone
- **Communication**: Message, ChatRoom, Comment
- **Activity**: Activity, Notification, UserStats
- **File Storage**: File, MessageFile
- **OAuth**: SocialApp, SocialAccount

Total relationships: 40+ foreign key relationships with proper indexing for optimal query performance.
