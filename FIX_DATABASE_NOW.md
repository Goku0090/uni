# ⚡ FIX DATABASE SCHEMA NOW (2 MINUTES)

## 🔴 The Issue
```
Database column missing: accounts_studentprofile.created_at
Result: Login queries fail
```

## ✅ The Fix (3 Commands)

### 1. Stop Server
```bash
# Press Ctrl+C in terminal
```

### 2. Apply Migrations
```bash
cd e:\login\auth_project
python manage.py migrate
```

### 3. Restart Server
```bash
python manage.py runserver
```

---

## 🧪 Test

```
1. Go to http://localhost:8000/login/
2. Enter username/email
3. Enter password
4. Click Login
5. Should see: "OTP sent to email@example.com"
```

---

## 📋 What Happens

```
Step 1: Stop Django
        ↓
Step 2: Run migrations
        ↓
        Django updates database
        Adds missing columns
        ↓
Step 3: Restart Django
        ↓
Step 4: Test login
        ↓
        ✅ Works!
```

---

## 🎯 Commands Summary

```bash
# 1. Navigate to project
cd e:\login\auth_project

# 2. Apply database migrations
python manage.py migrate

# 3. Check status
python manage.py showmigrations accounts

# 4. Restart server
python manage.py runserver

# 5. Test: go to localhost:8000/login/
```

---

## ✅ Success Indicators

After running migrate:
- ✅ No errors shown
- ✅ "Operation to perform" complete
- ✅ Can login with username
- ✅ Can login with email
- ✅ OTP email received

---

## ❌ If Migration Fails

### Common Issue: "No migrations to apply"
**This is OK!** Means migrations already applied
**Action**: Just restart server and test login

### If Real Error
```bash
# Create missing migrations
python manage.py makemigrations accounts

# Apply them
python manage.py migrate
```

---

## 🔍 Verify It Worked

```bash
python diagnose_login.py
# Should show all [OK] marks
```

---

*Time: 2 minutes*  
*Action: DO THIS NOW*  
*Impact: Unblocks login completely*
