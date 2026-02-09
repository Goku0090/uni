# Contributing to UniSinq

Thank you for your interest in contributing to UniSinq! We welcome all contributions, from bug reports to new features. Please read these guidelines before getting started.

## 📋 Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Provide constructive feedback
- Report issues promptly
- Respect intellectual property

## 🚀 Getting Started

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/uni.git
cd uni
```

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r auth_project/requirements.txt
pip install -r auth_project/requirements_dev.txt  # Dev dependencies

# Setup environment file
cp auth_project/.env.template auth_project/.env
# Edit .env with your local settings

# Run migrations
cd auth_project
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development servers
# Terminal 1:
python manage.py runserver

# Terminal 2:
daphne -b 0.0.0.0 -p 8001 auth_project.asgi:application
```

### Verify Setup

Visit http://localhost:8000 and verify the application loads correctly.

## 🔄 Development Workflow

### 1. Create Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/description-of-feature
# Or for bug fixes:
git checkout -b fix/description-of-bug
```

### 2. Make Changes

- Keep commits atomic and focused
- Write clear commit messages
- Test your changes locally
- Update documentation

### 3. Write/Update Tests

For new features, add tests:

```bash
cd auth_project
python manage.py test accounts.tests.YourTestClass
```

For bug fixes, add a test that reproduces the bug.

### 4. Format Code

```bash
# Format with Black
black auth_project --line-length=100

# Sort imports
isort --profile black auth_project

# Check style
flake8 auth_project --max-line-length=100
```

### 5. Run Tests

```bash
cd auth_project
python manage.py test --verbosity=2
```

### 6. Commit Changes

Use conventional commit messages:

```bash
git add .
git commit -m "type: brief description

Longer description explaining the change (optional)

- bullet point details
- more details

Fixes #123
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style (no logic change)
- `refactor:` Code restructuring
- `test:` Adding/updating tests
- `chore:` Maintenance, dependencies

**Examples:**
```
feat: add video call integration
fix: resolve WebSocket connection timeout
docs: update API documentation
refactor: simplify comment rendering logic
```

### 7. Push Changes

```bash
git push origin feature/description-of-feature
```

### 8. Create Pull Request

1. Go to https://github.com/Goku0090/uni/pulls
2. Click "New Pull Request"
3. Select your branch
4. Fill out PR template completely
5. Request reviewers
6. Submit

## 📝 Coding Guidelines

### Python Style

Follow PEP 8 and Django conventions:

```python
# Good
def create_project(user, title, description):
    """Create a new project for the given user."""
    project = Project.objects.create(
        owner=user,
        title=title,
        description=description,
    )
    return project

# Bad
def create_proj(u, t, d):
    p=Project.objects.create(owner=u,title=t,description=d)
    return p
```

### Django Best Practices

```python
# Models
class MyModel(models.Model):
    """Description of model."""
    name = models.CharField(max_length=100, help_text="Help text")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['name'])]
    
    def __str__(self):
        return self.name

# Views
def my_view(request):
    """Docstring describing view."""
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Process form
            pass
    else:
        form = MyForm()
    
    context = {'form': form}
    return render(request, 'template.html', context)

# APIs
class MySerializer(serializers.ModelSerializer):
    """Serializer for MyModel."""
    
    class Meta:
        model = MyModel
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']
```

### Documentation

Include docstrings for all functions/classes:

```python
def get_matching_collaborators(user, limit=10):
    """
    Get top collaborator matches for a user based on skill similarity.
    
    Args:
        user: User instance to find matches for
        limit: Maximum number of matches to return (default: 10)
    
    Returns:
        QuerySet of User instances ordered by match score
    
    Raises:
        ValueError: If user has no profile
    """
    if not hasattr(user, 'studentprofile'):
        raise ValueError(f"User {user.id} has no profile")
    
    # Implementation
    return matches
```

## 🧪 Testing

### Write Tests

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import Project

class ProjectTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_project_creation(self):
        """Test that projects can be created."""
        project = Project.objects.create(
            owner=self.user,
            title='Test Project'
        )
        self.assertEqual(project.owner, self.user)
    
    def test_project_view_requires_login(self):
        """Test that project view requires authentication."""
        client = Client()
        response = client.get('/project/1/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
```

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test accounts.tests.ProjectTests

# Run specific test method
python manage.py test accounts.tests.ProjectTests.test_project_creation

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📚 Documentation

If your changes affect the public API or user-facing features, update:

- `COMPREHENSIVE_CODE_ANALYSIS_FINAL_2026.md` - Technical details
- `ARCHITECTURE_DIAGRAM_VISUAL_2026.md` - Architecture diagrams (if needed)
- `CODEBASE_QUICK_REFERENCE_GUIDE_2026.md` - Developer reference (if needed)
- `README.md` - Usage and setup (if needed)

## 🔍 Code Review

Your PR will be reviewed by maintainers. They may:

- Request changes
- Ask for clarification
- Suggest improvements
- Run tests

Please respond to feedback promptly and make requested changes.

## ✅ Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added (complex logic)
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] Tests pass locally
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear
- [ ] PR description is complete

## 🎯 What We're Looking For

### Good Contributions

- ✅ Clear, well-tested code
- ✅ Helpful commit messages
- ✅ Updated documentation
- ✅ Follows project conventions
- ✅ Responsive to feedback
- ✅ Minimal scope (focus on one thing)

### Areas We Need Help

- Bug fixes (see open issues)
- Documentation improvements
- Test coverage increases
- Performance optimizations
- Feature implementations (check roadmap)
- UI/UX improvements

## 📋 Issue Labels

**Priority:**
- `critical` - Critical bug, security issue
- `high` - Important feature or bug
- `medium` - Standard priority
- `low` - Nice to have

**Type:**
- `bug` - Bug report
- `enhancement` - Feature request
- `documentation` - Docs improvement
- `good first issue` - Good for beginners

**Status:**
- `help wanted` - Need contributor help
- `in progress` - Currently being worked on
- `needs discussion` - Needs more details
- `needs testing` - Needs QA

## 🤝 Support & Questions

- **Issues:** GitHub Issues for bugs/features
- **Discussions:** GitHub Discussions for questions
- **Email:** Include email contact (if applicable)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [Django Channels](https://channels.readthedocs.io/)
- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Git Guide](https://git-scm.com/doc)

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in README
- Recognized in discussions

---

**Thank you for contributing to UniSinq!** 🎉

If you have questions, feel free to ask in discussions or open an issue.

Happy coding! 🚀
