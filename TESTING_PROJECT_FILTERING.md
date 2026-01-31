# Testing Project Visibility Filtering

## Manual Testing Guide

### Prerequisites
1. Django development server running
2. At least 2 user accounts created
3. User profiles with skills/college/interests filled

---

## Test Scenario 1: College Match

### Setup

**User A:**
- College: `IIT Delhi`
- Skills: `Python, Django`
- Interests: `Web Development`

**User B:**
- College: `IIT Delhi`
- Skills: `JavaScript, React`
- Project Title: `Social Network App`
- Technologies: `React, Node.js`
- Looking For: `Full Stack Developer`

### Expected Result
When User A views home:
- ✅ Should see User B's project
- ✅ Badge shows "Same College"
- ✅ Score ≥ 30

### Test Steps
1. Login as User A
2. Go to home page
3. Look for "Social Network App"
4. Check for college match badge

---

## Test Scenario 2: Technology Match

### Setup

**User C:**
- College: `MIT`
- Skills: `Python, TensorFlow, Keras`
- Interests: `AI/ML`

**User D:**
- College: `Stanford`
- Skills: `JavaScript, React`
- Project: `Chatbot with AI`
- Technologies: `Python, TensorFlow, Dialogflow`
- Looking For: `AI Engineer, ML Specialist`

### Expected Result
When User C views home:
- ✅ Should see "Chatbot with AI"
- ✅ Badge shows "Common Technologies: Python, TensorFlow"
- ✅ Score ≥ 40 (even though different colleges)

### Test Steps
1. Login as User C
2. Go to home page
3. Verify project appears with tech match badge
4. Check "Python" and "TensorFlow" mentioned

---

## Test Scenario 3: Interest Match

### Setup

**User E:**
- College: `Harvard`
- Skills: `Java`
- Interests: `Backend Development, Microservices`

**User F:**
- College: `Yale`
- Skills: `Java, Spring Boot`
- Project: `Microservices Platform`
- Technologies: `Java, Spring Boot, Docker`
- Looking For: `Backend Developer, Microservices Expert`

### Expected Result
When User E views home:
- ✅ Should see "Microservices Platform"
- ✅ Badge shows "Matching Interests: Microservices"
- ✅ Score ≥ 30

### Test Steps
1. Login as User E
2. Go to home page
3. Find "Microservices Platform"
4. Verify interest match badge

---

## Test Scenario 4: No Match

### Setup

**User G:**
- College: `MIT`
- Skills: `Python, Django`
- Interests: `Backend Development`

**User H:**
- College: `Stanford`
- Skills: `Photoshop, Figma`
- Project: `UI Design System`
- Technologies: `Figma, Sketch`
- Looking For: `UI Designer, UX Designer`

### Expected Result
When User G views home:
- ✅ Should NOT see "UI Design System"
- Or if shown: Badge shows "No Match" with 0 score

### Test Steps
1. Login as User G
2. Go to home page
3. Verify design project doesn't appear (or shows 0% match)

---

## Test Scenario 5: User's Own Project

### Setup

**User I:**
- Posts a project "My Portfolio"
- College: Any
- Technologies: Any

### Expected Result
When User I views home:
- ✅ Always sees own project
- ✅ Badge shows "Perfect Match ⭐" (100%)
- ✅ Shows "Your Project" reason

### Test Steps
1. Login as User I
2. Create new project
3. Go to home page
4. Verify own project appears first with 100% match

---

## Automated Testing

### Unit Test Template

```python
# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import StudentProfile, Project
from accounts.utils import ProjectVisibilityFilter

class ProjectVisibilityFilterTest(TestCase):
    
    def setUp(self):
        """Create test users and projects"""
        # Create User A
        self.user_a = User.objects.create_user(
            username='usera',
            email='a@test.com',
            password='testpass123'
        )
        self.profile_a = StudentProfile.objects.create(
            user=self.user_a,
            college='MIT',
            skills=['Python', 'React', 'Django'],
            interests=['Web Development', 'AI/ML']
        )
        
        # Create User B
        self.user_b = User.objects.create_user(
            username='userb',
            email='b@test.com',
            password='testpass123'
        )
        self.profile_b = StudentProfile.objects.create(
            user=self.user_b,
            college='MIT',
            skills=['JavaScript', 'React']
        )
        
        # Create Project
        self.project = Project.objects.create(
            user=self.user_b,
            title='Social App',
            description='A social networking app',
            technologies=['React', 'Node.js'],
            looking_for=['Full Stack Dev', 'Frontend Dev']
        )
    
    def test_college_match(self):
        """Test that same college projects are visible"""
        visible, details = ProjectVisibilityFilter.get_visible_projects(
            self.user_a,
            Project.objects.all()
        )
        
        # Project should be visible
        self.assertIn(self.project, visible)
        
        # Check score includes college match
        self.assertGreaterEqual(details[self.project.id]['score'], 30)
        
        # Check college mentioned in reasons
        self.assertIn('Same College', details[self.project.id]['reasons'])
    
    def test_technology_match(self):
        """Test that projects with matching tech are visible"""
        visible, details = ProjectVisibilityFilter.get_visible_projects(
            self.user_a,
            Project.objects.all()
        )
        
        # Project should be visible
        self.assertIn(self.project, visible)
        
        # Check score includes tech match
        self.assertGreaterEqual(details[self.project.id]['score'], 40)
        
        # Check tech mentioned in reasons
        reasons = ' '.join(details[self.project.id]['reasons'])
        self.assertIn('React', reasons)
    
    def test_user_own_project(self):
        """Test that user's own projects always match 100%"""
        own_project = Project.objects.create(
            user=self.user_a,
            title='My Project',
            description='My awesome project',
            technologies=['Django'],
            looking_for=['Backend Dev']
        )
        
        visible, details = ProjectVisibilityFilter.get_visible_projects(
            self.user_a,
            Project.objects.all()
        )
        
        # Own project should have 100% match
        self.assertEqual(details[own_project.id]['score'], 100)
        
        # Should say "Your Project"
        self.assertIn('Your Project', details[own_project.id]['reasons'])
    
    def test_sorting_by_score(self):
        """Test that projects are sorted by match score"""
        visible, details = ProjectVisibilityFilter.get_visible_projects(
            self.user_a,
            Project.objects.all()
        )
        
        # Verify descending order
        scores = [details[p.id]['score'] for p in visible]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_string_format_skills(self):
        """Test filtering works with string format skills"""
        user = User.objects.create_user(
            username='user_string',
            email='string@test.com',
            password='testpass123'
        )
        profile = StudentProfile.objects.create(
            user=user,
            college='Stanford',
            skills='Python,Django,React',  # String format
            interests='Web Development'
        )
        
        visible, details = ProjectVisibilityFilter.get_visible_projects(
            user,
            Project.objects.all()
        )
        
        # Project should still be visible (React match)
        self.assertIn(self.project, visible)
```

### Run Tests

```bash
# Run all project visibility tests
python manage.py test accounts.tests.ProjectVisibilityFilterTest

# Run specific test
python manage.py test accounts.tests.ProjectVisibilityFilterTest.test_college_match

# Run with verbose output
python manage.py test accounts.tests.ProjectVisibilityFilterTest -v 2

# Run with coverage
coverage run --source='accounts.utils' manage.py test
coverage report
```

---

## Django Shell Testing

Quick testing without creating test files:

```python
# python manage.py shell

from django.contrib.auth.models import User
from accounts.models import StudentProfile, Project
from accounts.utils import ProjectVisibilityFilter

# Get a user
user = User.objects.first()

# Get their projects
visible_projects, match_details = ProjectVisibilityFilter.get_visible_projects(user)

# Print results
print(f"Visible projects: {len(visible_projects)}")
for project in visible_projects:
    details = match_details.get(project.id, {})
    print(f"\n{project.title}")
    print(f"  Score: {details.get('score', 0)}")
    print(f"  Reasons: {details.get('reasons', [])}")

# Test specific score
print("\nMatch badge for 75% score:")
badge = ProjectVisibilityFilter.get_project_match_badge(75)
print(badge)

# Test compatibility
from accounts.models import Project
project = Project.objects.first()
compat = ProjectVisibilityFilter.get_compatibility_percentage(user, project)
print(f"\nCompatibility with {project.title}: {compat}%")
```

---

## Browser Testing Checklist

- [ ] Login as test user
- [ ] Check profile has college/skills/interests
- [ ] Go to home page
- [ ] Verify projects load
- [ ] Check match badges display
- [ ] Verify project sorting (highest match first)
- [ ] Click on a project
- [ ] Check mobile view (if applicable)
- [ ] Check with different user
- [ ] Verify user's own project shows 100%

---

## Performance Testing

### Check Query Count

```python
from django.test.utils import override_settings
from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext

# In your test
with CaptureQueriesContext() as ctx:
    visible_projects, details = ProjectVisibilityFilter.get_visible_projects(user)
    
print(f"Queries executed: {len(ctx)}")
for query in ctx:
    print(query['sql'])
```

### Check Execution Time

```python
import time
from accounts.utils import ProjectVisibilityFilter

start = time.time()
visible_projects, details = ProjectVisibilityFilter.get_visible_projects(user)
end = time.time()

print(f"Execution time: {(end - start) * 1000:.2f}ms")
```

---

## Testing Different Data Formats

### Format 1: JSONField Lists

```python
profile = StudentProfile.objects.create(
    user=user,
    college='MIT',
    skills=['Python', 'React'],           # List format
    interests=['Web Dev', 'AI/ML']
)
```

### Format 2: String Format

```python
profile = StudentProfile.objects.create(
    user=user,
    college='MIT',
    skills='Python,React',                # String format
    interests='Web Dev, AI/ML'
)
```

### Format 3: Mixed Case

```python
profile = StudentProfile.objects.create(
    user=user,
    college='MIT',
    skills='python, REACT, Django',       # Mixed case
    interests=['web development', 'AI/ML']
)
```

✅ All three formats should work identically!

---

## Debugging Tips

### Print Match Details

```python
visible, details = ProjectVisibilityFilter.get_visible_projects(user)

for project_id, info in details.items():
    print(f"\nProject ID {project_id}:")
    print(f"  Score: {info['score']}")
    print(f"  Has Match: {info['has_match']}")
    print(f"  Reasons: {info['reasons']}")
```

### Check User Profile Data

```python
profile = user.student_profile
print(f"College: {profile.college}")
print(f"Skills: {profile.skills} (type: {type(profile.skills)})")
print(f"Interests: {profile.interests}")
```

### Check Project Data

```python
project = Project.objects.first()
print(f"Title: {project.title}")
print(f"Technologies: {project.technologies} (type: {type(project.technologies)})")
print(f"Looking for: {project.looking_for}")
print(f"Owner college: {project.user.student_profile.college}")
```

---

## Common Test Failures & Solutions

### "Projects not showing"
```python
# Check if user has profile
try:
    profile = user.student_profile
except:
    print("User has no profile")
    
# Check if profile has data
print(profile.college, profile.skills, profile.interests)
```

### "Wrong match score"
```python
# Check data types
print(type(profile.skills))  # Should be list or str
print(type(project.technologies))

# Check data normalization
skills = {'python', 'react'}
techs = {'React', 'Node'}
print(skills.intersection(techs))  # Should find match
```

### "Projects not sorting correctly"
```python
# Check sorting
for p in visible_projects:
    score = details[p.id]['score']
    print(f"{p.title}: {score}")
```

---

## Summary

✅ Manual testing with 5 key scenarios  
✅ Automated unit tests provided  
✅ Django shell testing commands  
✅ Browser testing checklist  
✅ Performance testing guide  
✅ Debugging tips and solutions  

Run through these tests to verify the project filtering is working correctly!
