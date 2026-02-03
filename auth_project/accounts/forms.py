"""
Forms for the accounts app
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import StudentProfile, Project, OTP, Comment


class RegisterForm(UserCreationForm):
    """Enhanced registration form with additional validation"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )

    username = forms.CharField(
        max_length=150,
        min_length=3,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username (3-150 characters)'
        })
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password'
        }),
        help_text='Password must be at least 8 characters long and contain uppercase, lowercase, and digit.'
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    terms_agree = forms.BooleanField(
        required=True,
        label='I agree to the Terms of Service and Privacy Policy'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')

        if not any(c.isupper() for c in password):
            raise ValidationError('Password must contain at least one uppercase letter.')

        if not any(c.islower() for c in password):
            raise ValidationError('Password must contain at least one lowercase letter.')

        if not any(c.isdigit() for c in password):
            raise ValidationError('Password must contain at least one digit.')

        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')

        return cleaned_data


class LoginForm(AuthenticationForm):
    """Enhanced login form"""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        label='Remember me'
    )


class OTPVerificationForm(forms.Form):
    """Form for OTP verification"""

    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Enter 6-digit OTP',
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        }),
        label='OTP Code'
    )

    def clean_otp_code(self):
        otp_code = self.cleaned_data['otp_code']
        if not otp_code.isdigit():
            raise ValidationError("OTP must contain only digits.")
        if len(otp_code) != 6:
            raise ValidationError("OTP must be exactly 6 digits.")
        return otp_code


class StudentProfileForm(forms.ModelForm):
    """Form for editing student profiles"""

    full_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )

    college = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your college/university'
        })
    )

    other_college = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Specify other college'
        })
    )

    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City, State/Country'
        })
    )

    interests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Your interests (comma-separated)'
        })
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Tell us about yourself...'
        })
    )

    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    # Skills as checkboxes
    skills = forms.MultipleChoiceField(
        choices=[
            ('python', 'Python'),
            ('javascript', 'JavaScript'),
            ('java', 'Java'),
            ('cpp', 'C++'),
            ('react', 'React'),
            ('django', 'Django'),
            ('node', 'Node.js'),
            ('html_css', 'HTML/CSS'),
            ('sql', 'SQL'),
            ('git', 'Git'),
            ('docker', 'Docker'),
            ('aws', 'AWS'),
            ('machine_learning', 'Machine Learning'),
            ('data_science', 'Data Science'),
            ('ui_ux', 'UI/UX Design'),
            ('mobile_dev', 'Mobile Development'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    # Project interests as checkboxes
    project_interests = forms.MultipleChoiceField(
        choices=[
            ('web_development', 'Web Development'),
            ('mobile_apps', 'Mobile Applications'),
            ('ai_ml', 'AI/ML Projects'),
            ('data_science', 'Data Science'),
            ('blockchain', 'Blockchain'),
            ('iot', 'IoT Projects'),
            ('game_dev', 'Game Development'),
            ('open_source', 'Open Source'),
            ('research', 'Research Projects'),
            ('startup', 'Startup Ideas'),
            ('social_impact', 'Social Impact'),
            ('education', 'Educational Tools'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    role_preference = forms.ChoiceField(
        choices=[
            ('', '-- Select Role --'),
            ('frontend', 'Frontend Developer'),
            ('backend', 'Backend Developer'),
            ('fullstack', 'Full Stack Developer'),
            ('mobile', 'Mobile Developer'),
            ('data_scientist', 'Data Scientist'),
            ('ml_engineer', 'ML Engineer'),
            ('ui_ux', 'UI/UX Designer'),
            ('product_manager', 'Product Manager'),
            ('devops', 'DevOps Engineer'),
            ('qa_tester', 'QA Tester'),
            ('other', 'Other'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Social links
    github = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://github.com/username'
        })
    )

    linkedin = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://linkedin.com/in/username'
        })
    )

    portfolio = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://yourportfolio.com'
        })
    )

    behance = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://behance.net/username'
        })
    )

    class Meta:
        model = StudentProfile
        fields = [
            'full_name', 'college', 'other_college', 'location',
            'interests', 'bio', 'profile_photo', 'skills', 'project_interests',
            'role_preference', 'github', 'linkedin', 'portfolio', 'behance'
        ]

    def clean_college(self):
        college = self.cleaned_data.get('college')
        if college and len(college.strip()) < 3:
            raise ValidationError("Please enter a valid college name (at least 3 characters).")
        return college

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if full_name and len(full_name.strip()) < 2:
            raise ValidationError("Full name must be at least 2 characters long.")
        return full_name


class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects"""

    title = forms.CharField(
        max_length=200,
        min_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter project title (5-200 characters)'
        }),
        help_text='Choose a clear, descriptive title for your project'
    )

    description = forms.CharField(
        min_length=20,
        max_length=5000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Describe your project in detail... (20-5000 characters)'
        }),
        help_text='Provide detailed information about your project, goals, and what you hope to achieve'
    )

    technologies = forms.MultipleChoiceField(
        choices=[
            ('python', 'Python'),
            ('javascript', 'JavaScript'),
            ('java', 'Java'),
            ('cpp', 'C++'),
            ('csharp', 'C#'),
            ('php', 'PHP'),
            ('ruby', 'Ruby'),
            ('go', 'Go'),
            ('rust', 'Rust'),
            ('swift', 'Swift'),
            ('kotlin', 'Kotlin'),
            ('react', 'React'),
            ('angular', 'Angular'),
            ('vue', 'Vue.js'),
            ('django', 'Django'),
            ('flask', 'Flask'),
            ('laravel', 'Laravel'),
            ('rails', 'Ruby on Rails'),
            ('spring', 'Spring Boot'),
            ('nodejs', 'Node.js'),
            ('express', 'Express.js'),
            ('html_css', 'HTML/CSS'),
            ('bootstrap', 'Bootstrap'),
            ('tailwind', 'Tailwind CSS'),
            ('sass', 'SASS/SCSS'),
            ('sql', 'SQL'),
            ('mongodb', 'MongoDB'),
            ('postgresql', 'PostgreSQL'),
            ('mysql', 'MySQL'),
            ('redis', 'Redis'),
            ('docker', 'Docker'),
            ('kubernetes', 'Kubernetes'),
            ('aws', 'AWS'),
            ('gcp', 'Google Cloud'),
            ('azure', 'Azure'),
            ('git', 'Git'),
            ('tensorflow', 'TensorFlow'),
            ('pytorch', 'PyTorch'),
            ('opencv', 'OpenCV'),
            ('pandas', 'Pandas'),
            ('numpy', 'NumPy'),
            ('jupyter', 'Jupyter'),
            ('r', 'R'),
            ('tableau', 'Tableau'),
            ('powerbi', 'Power BI'),
            ('figma', 'Figma'),
            ('sketch', 'Sketch'),
            ('photoshop', 'Photoshop'),
            ('illustrator', 'Illustrator'),
            ('blender', 'Blender'),
            ('unity', 'Unity'),
            ('unreal', 'Unreal Engine'),
            ('android', 'Android'),
            ('ios', 'iOS'),
            ('flutter', 'Flutter'),
            ('react_native', 'React Native'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text='Select all technologies you plan to use or are currently using'
    )

    looking_for = forms.MultipleChoiceField(
        choices=[
            ('frontend_dev', 'Frontend Developer'),
            ('backend_dev', 'Backend Developer'),
            ('fullstack_dev', 'Full Stack Developer'),
            ('mobile_dev', 'Mobile Developer'),
            ('ui_ux_designer', 'UI/UX Designer'),
            ('data_scientist', 'Data Scientist'),
            ('ml_engineer', 'ML Engineer'),
            ('devops_engineer', 'DevOps Engineer'),
            ('qa_tester', 'QA Tester'),
            ('product_manager', 'Product Manager'),
            ('business_analyst', 'Business Analyst'),
            ('project_manager', 'Project Manager'),
            ('technical_writer', 'Technical Writer'),
            ('mentor', 'Mentor'),
            ('investor', 'Investor'),
            ('beta_tester', 'Beta Tester'),
            ('graphic_designer', 'Graphic Designer'),
            ('content_creator', 'Content Creator'),
            ('marketing_specialist', 'Marketing Specialist'),
            ('legal_advisor', 'Legal Advisor'),
            ('other', 'Other'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text='What roles are you looking to fill in your project team?'
    )

    category = forms.ChoiceField(
        choices=[
            ('web', 'Web Development'),
            ('mobile', 'Mobile Applications'),
            ('ai', 'AI/ML'),
            ('data', 'Data Science & Analytics'),
            ('blockchain', 'Blockchain & Crypto'),
            ('iot', 'IoT & Hardware'),
            ('game', 'Game Development'),
            ('desktop', 'Desktop Applications'),
            ('api', 'API Development'),
            ('automation', 'Automation & Scripting'),
            ('security', 'Cybersecurity'),
            ('devops', 'DevOps & Infrastructure'),
            ('design', 'Design & Creative'),
            ('education', 'Educational Tools'),
            ('social', 'Social Impact'),
            ('startup', 'Startup & Business'),
            ('research', 'Research & Academic'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Choose the primary category that best describes your project'
    )

    timeline = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 3-6 months, Ongoing, 2 weeks'
        }),
        help_text='Estimated timeline for completion or current phase'
    )

    collaboration_needs = forms.CharField(
        max_length=2000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe what kind of collaboration you need...'
        }),
        help_text='Explain your collaboration needs, commitment level, and what collaborators can expect'
    )

    github_link = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://github.com/username/project-repo'
        }),
        help_text='Link to your GitHub repository (optional but recommended)'
    )

    class Meta:
        model = Project
        fields = [
            'title', 'description', 'technologies', 'looking_for',
            'category', 'timeline', 'collaboration_needs', 'github_link'
        ]

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 5:
            raise ValidationError("Project title must be at least 5 characters long.")
        if len(title) > 200:
            raise ValidationError("Project title cannot exceed 200 characters.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if len(description) < 20:
            raise ValidationError("Project description must be at least 20 characters long.")
        if len(description) > 5000:
            raise ValidationError("Project description cannot exceed 5000 characters.")
        return description

    def clean_github_link(self):
        github_link = self.cleaned_data.get('github_link')
        if github_link:
            if not github_link.startswith(('http://', 'https://')):
                raise ValidationError("GitHub link must be a valid URL starting with http:// or https://")
            if 'github.com' not in github_link.lower():
                raise ValidationError("Please provide a valid GitHub repository URL")
        return github_link


class CustomSocialSignupForm(forms.Form):
    """Custom social signup form for additional user data"""

    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )

    college = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College/University (optional)'
        })
    )

    interests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Your interests (optional)'
        })
    )

    def signup(self, request, user):
        """Save additional profile data during social signup"""
        profile, created = StudentProfile.objects.get_or_create(
            user=user,
            defaults={
                'full_name': self.cleaned_data.get('full_name', ''),
                'college': self.cleaned_data.get('college', ''),
                'interests': self.cleaned_data.get('interests', ''),
                'profile_completed': True
            }
        )

        if not created:
            # Update existing profile
            profile.full_name = self.cleaned_data.get('full_name', profile.full_name)
            profile.college = self.cleaned_data.get('college', profile.college)
            profile.interests = self.cleaned_data.get('interests', profile.interests)
            profile.profile_completed = True
            profile.save()

        return user


# --- COMMENT FORM ---
class CommentForm(forms.ModelForm):
    """Form for adding comments to projects"""
    
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control comment-input',
            'rows': 2,
            'placeholder': 'Share your thoughts on this project...',
            'style': 'resize: none; border-radius: 8px; font-size: 14px;'
        }),
        required=True,
        min_length=1,
        max_length=1000
    )
    
    class Meta:
        model = Comment
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['autofocus'] = False
