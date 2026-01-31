import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Load spaCy model (will download if not present)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class StudentProfileNLP:
    """NLP utilities for student profile analysis"""

    # Technical skills and programming languages
    TECH_SKILLS = {
        'programming_languages': [
            'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'typescript', 'go', 'rust', 'scala', 'r', 'matlab', 'perl', 'lua', 'dart',
            'html', 'css', 'sql', 'bash', 'powershell', 'assembly'
        ],
        'frameworks': [
            'django', 'flask', 'fastapi', 'react', 'angular', 'vue', 'svelte', 'express',
            'spring', 'laravel', 'rails', 'asp.net', 'tensorflow', 'pytorch', 'keras',
            'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn'
        ],
        'tools': [
            'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'linux', 'windows',
            'macos', 'vscode', 'vim', 'intellij', 'pycharm', 'jupyter', 'postman',
            'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch'
        ]
    }

    # Interest categories
    INTEREST_CATEGORIES = {
        'ai_ml': ['artificial intelligence', 'machine learning', 'deep learning', 'neural networks',
                 'computer vision', 'nlp', 'natural language processing', 'data science', 'analytics'],
        'web_dev': ['web development', 'frontend', 'backend', 'fullstack', 'api', 'rest', 'graphql'],
        'mobile_dev': ['mobile development', 'android', 'ios', 'react native', 'flutter', 'swiftui'],
        'blockchain': ['blockchain', 'cryptocurrency', 'ethereum', 'solidity', 'web3', 'defi'],
        'cybersecurity': ['cybersecurity', 'security', 'ethical hacking', 'penetration testing'],
        'game_dev': ['game development', 'unity', 'unreal engine', 'godot'],
        'iot': ['internet of things', 'iot', 'embedded systems', 'arduino', 'raspberry pi'],
        'design': ['ui/ux', 'design', 'figma', 'adobe', 'photoshop', 'illustrator']
    }

    @staticmethod
    def preprocess_text(text):
        """Clean and preprocess text for analysis"""
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Tokenize
        tokens = word_tokenize(text)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]

        # Lemmatize
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return ' '.join(tokens)

    @staticmethod
    def extract_skills(text):
        """Extract technical skills from text"""
        if not text:
            return []

        processed_text = StudentProfileNLP.preprocess_text(text)
        found_skills = []

        # Check for programming languages
        for lang in StudentProfileNLP.TECH_SKILLS['programming_languages']:
            if lang in processed_text or lang.replace('+', ' plus') in processed_text:
                found_skills.append(lang)

        # Check for frameworks
        for framework in StudentProfileNLP.TECH_SKILLS['frameworks']:
            if framework in processed_text:
                found_skills.append(framework)

        # Check for tools
        for tool in StudentProfileNLP.TECH_SKILLS['tools']:
            if tool in processed_text:
                found_skills.append(tool)

        return list(set(found_skills))  # Remove duplicates

    @staticmethod
    def analyze_interests(text):
        """Analyze interests and categorize them"""
        if not text:
            return {}

        processed_text = StudentProfileNLP.preprocess_text(text)
        interest_scores = {}

        for category, keywords in StudentProfileNLP.INTEREST_CATEGORIES.items():
            score = 0
            for keyword in keywords:
                if keyword in processed_text:
                    score += 1
            if score > 0:
                interest_scores[category] = score

        # Sort by relevance
        return dict(sorted(interest_scores.items(), key=lambda x: x[1], reverse=True))

    @staticmethod
    def extract_keywords(text, max_keywords=10):
        """Extract important keywords using TF-IDF"""
        if not text or len(text.strip()) < 10:
            return []

        try:
            # Simple keyword extraction using spaCy
            doc = nlp(text)
            keywords = []

            # Extract nouns and proper nouns
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                    keywords.append(token.text.lower())

            # Remove duplicates and get top keywords
            keywords = list(set(keywords))
            return keywords[:max_keywords]
        except:
            return []

    @staticmethod
    def analyze_sentiment(text):
        """Analyze sentiment of text"""
        if not text:
            return {'polarity': 0, 'subjectivity': 0}

        try:
            blob = TextBlob(text)
            return {
                'polarity': round(blob.sentiment.polarity, 2),
                'subjectivity': round(blob.sentiment.subjectivity, 2)
            }
        except:
            return {'polarity': 0, 'subjectivity': 0}

    @staticmethod
    def calculate_profile_completeness(profile_data):
        """Calculate how complete a profile is"""
        fields = [
            'full_name', 'college', 'location', 'interests', 'bio',
            'skills', 'project_interests', 'github', 'linkedin'
        ]

        completed = 0
        for field in fields:
            value = profile_data.get(field)
            if value and str(value).strip():
                completed += 1

        return round((completed / len(fields)) * 100, 1)

    @staticmethod
    def suggest_improvements(profile_data):
        """Suggest improvements for profile completeness"""
        suggestions = []

        if not profile_data.get('profile_photo'):
            suggestions.append("Add a profile photo to make your profile more personal")

        if not profile_data.get('bio') or len(profile_data.get('bio', '')) < 50:
            suggestions.append("Write a detailed bio (at least 50 characters) describing your experience and goals")

        if not profile_data.get('skills'):
            suggestions.append("Add your technical skills to help others find you for collaborations")

        if not profile_data.get('project_interests'):
            suggestions.append("Specify project types you're interested in to get relevant collaboration opportunities")

        if not profile_data.get('github') and not profile_data.get('portfolio'):
            suggestions.append("Add your GitHub or portfolio link to showcase your work")

        return suggestions

    @staticmethod
    def match_profiles(profile1, profile2):
        """Calculate similarity between two profiles"""
        try:
            # Combine relevant text fields
            text1 = f"{profile1.get('bio', '')} {profile1.get('interests', '')} {' '.join(profile1.get('skills', []))}"
            text2 = f"{profile2.get('bio', '')} {profile2.get('interests', '')} {' '.join(profile2.get('skills', []))}"

            if not text1.strip() or not text2.strip():
                return 0.0

            # Vectorize texts
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([text1, text2])

            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

            return round(similarity * 100, 1)
        except:
            return 0.0


class ProjectVisibilityFilter:
    """Filter projects based on user profile compatibility"""

    @staticmethod
    def get_visible_projects(user, all_projects=None):
        """
        Get projects visible to a user based on:
        1. Same college (high priority)
        2. Same technologies used (high priority)
        3. Same interests/preferences (medium priority)
        4. All other projects shown with lower priority
        
        Args:
            user: The user to filter projects for
            all_projects: QuerySet of projects (if None, all projects fetched)
            
        Returns:
            Tuple of (all_projects_sorted_by_relevance, match_details)
        """
        if all_projects is None:
            from .models import Project
            all_projects = Project.objects.all().order_by('-created_at')
        
        # Handle unauthenticated users - show all projects
        if not user or not user.is_authenticated:
            visible_projects = list(all_projects)
            match_details = {}
            for project in visible_projects:
                match_details[project.id] = {
                    'score': 0,
                    'reasons': ["Browse all projects"],
                    'has_match': False
                }
            return visible_projects, match_details
        
        try:
            user_profile = user.student_profile
        except:
            # User has no profile - show all projects but mark user's own as priority
            visible_projects = list(all_projects)
            match_details = {}
            for project in visible_projects:
                if project.user == user:
                    match_details[project.id] = {
                        'score': 100,
                        'reasons': ["Your Project"],
                        'has_match': True
                    }
                else:
                    match_details[project.id] = {
                        'score': 0,
                        'reasons': ["Complete your profile for better matches"],
                        'has_match': False
                    }
            # Sort: user's projects first
            visible_projects.sort(
                key=lambda p: match_details[p.id]['score'],
                reverse=True
            )
            return visible_projects, match_details
        
        visible_projects = []
        match_details = {}
        
        user_interests = set()
        user_skills = set()
        user_college = user_profile.college or ""
        
        # Normalize user interests (handle both list and string)
        if user_profile.interests:
            if isinstance(user_profile.interests, list):
                user_interests = set(str(i).lower().strip() for i in user_profile.interests if i)
            elif isinstance(user_profile.interests, str):
                user_interests = set(i.lower().strip() for i in user_profile.interests.split(',') if i)
        
        # Normalize user skills (handle both list and string)
        if user_profile.skills:
            if isinstance(user_profile.skills, list):
                user_skills = set(str(s).lower().strip() for s in user_profile.skills if s)
            elif isinstance(user_profile.skills, str):
                user_skills = set(s.lower().strip() for s in user_profile.skills.split(',') if s)
        
        # Process all projects - ALWAYS INCLUDE THEM
        for project in all_projects:
            match_score = 0
            match_reasons = []
            
            # Try to get project owner's profile (if it exists)
            try:
                project_user_profile = project.user.student_profile
            except:
                project_user_profile = None
            
            # 1. Show user's own projects with HIGHEST priority
            if project.user == user:
                match_score = 100
                match_reasons = ["Your Project"]
            else:
                # 2. College Match (HIGH PRIORITY)
                if user_college and project_user_profile:
                    project_college = project_user_profile.college or ""
                    if user_college.lower() == project_college.lower():
                        match_score += 30
                        match_reasons.append("Same College")
                
                # 3. Technologies Match (HIGH PRIORITY)
                if user_skills:
                    project_techs = set()
                    if project.technologies:
                        if isinstance(project.technologies, list):
                            project_techs = set(str(t).lower().strip() for t in project.technologies if t)
                        elif isinstance(project.technologies, str):
                            project_techs = set(t.lower().strip() for t in project.technologies.split(',') if t)
                    
                    # Check for common technologies
                    tech_intersection = user_skills.intersection(project_techs)
                    if tech_intersection:
                        match_score += 40
                        match_reasons.append(f"Uses: {', '.join(list(tech_intersection)[:2])}")
                
                # 4. Interests/Preferences Match (MEDIUM PRIORITY)
                if user_interests:
                    project_looking_for = set()
                    if project.looking_for:
                        if isinstance(project.looking_for, list):
                            project_looking_for = set(str(l).lower().strip() for l in project.looking_for if l)
                        elif isinstance(project.looking_for, str):
                            project_looking_for = set(l.lower().strip() for l in project.looking_for.split(',') if l)
                    
                    # Check for common interests/preferences
                    interest_intersection = user_interests.intersection(project_looking_for)
                    if interest_intersection:
                        match_score += 20
                        match_reasons.append(f"Seeks: {', '.join(list(interest_intersection)[:2])}")
                
                # If no matches found, still show with low priority
                if match_score == 0:
                    match_reasons = ["Explore this project"]
            
            # Add ALL projects to visible list (don't filter out any)
            visible_projects.append(project)
            match_details[project.id] = {
                'score': match_score,
                'reasons': match_reasons,
                'has_match': match_score > 0
            }
        
        # Sort by match score (highest first, so user's projects at top)
        visible_projects.sort(
            key=lambda p: match_details[p.id]['score'],
            reverse=True
        )
        
        return visible_projects, match_details

    @staticmethod
    def get_project_match_badge(match_score):
        """Get badge color and text based on match score"""
        if match_score >= 80:
            return {
                'color': 'green',
                'text': 'Perfect Match',
                'emoji': '⭐'
            }
        elif match_score >= 60:
            return {
                'color': 'blue',
                'text': 'Good Match',
                'emoji': '👍'
            }
        elif match_score >= 30:
            return {
                'color': 'yellow',
                'text': 'Some Match',
                'emoji': '👀'
            }
        else:
            return {
                'color': 'gray',
                'text': 'No Match',
                'emoji': '💤'
            }

    @staticmethod
    def get_compatibility_percentage(user, project):
        """Calculate compatibility percentage for a user and project"""
        match_score = 0
        total_criteria = 0
        
        try:
            user_profile = user.student_profile
        except:
            return 0
        
        # 1. College (worth 33%)
        total_criteria += 1
        if user_profile.college and project.user.student_profile.college:
            if user_profile.college.lower() == project.user.student_profile.college.lower():
                match_score += 1
        
        # 2. Technologies (worth 33%)
        total_criteria += 1
        user_skills = set()
        if user_profile.skills:
            if isinstance(user_profile.skills, list):
                user_skills = set(str(s).lower().strip() for s in user_profile.skills)
            elif isinstance(user_profile.skills, str):
                user_skills = set(s.lower().strip() for s in user_profile.skills.split(','))
        
        project_techs = set()
        if project.technologies:
            if isinstance(project.technologies, list):
                project_techs = set(str(t).lower().strip() for t in project.technologies)
            elif isinstance(project.technologies, str):
                project_techs = set(t.lower().strip() for t in project.technologies.split(','))
        
        if user_skills and project_techs and user_skills.intersection(project_techs):
            match_score += 1
        
        # 3. Interests (worth 33%)
        total_criteria += 1
        user_interests = set()
        if user_profile.interests:
            if isinstance(user_profile.interests, list):
                user_interests = set(str(i).lower().strip() for i in user_profile.interests)
            elif isinstance(user_profile.interests, str):
                user_interests = set(i.lower().strip() for i in user_profile.interests.split(','))
        
        project_looking = set()
        if project.looking_for:
            if isinstance(project.looking_for, list):
                project_looking = set(str(l).lower().strip() for l in project.looking_for)
            elif isinstance(project.looking_for, str):
                project_looking = set(l.lower().strip() for l in project.looking_for.split(','))
        
        if user_interests and project_looking and user_interests.intersection(project_looking):
            match_score += 1
        
        # Calculate percentage
        percentage = (match_score / total_criteria * 100) if total_criteria > 0 else 0
        return round(percentage)
