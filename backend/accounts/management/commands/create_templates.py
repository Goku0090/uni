"""
Management command to create default project templates
Run: python manage.py create_templates
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import ProjectTemplate


class Command(BaseCommand):
    help = 'Create default project templates for users to use when posting projects'

    def handle(self, *args, **options):
        templates_data = [
            {
                'name': 'Web Development Platform',
                'category': 'web',
                'description': 'Build a full-stack web application with modern tech stack.',
                'icon': '🌐',
                'template_title': 'My Web Application',
                'template_description': 'A scalable web platform built with modern technologies.',
                'template_technologies': ['React', 'Node.js', 'PostgreSQL', 'Docker', 'Tailwind CSS'],
                'template_looking_for': ['Full-stack Developer', 'Frontend Developer', 'Backend Developer', 'DevOps Engineer'],
                'template_collaboration_needs': 'Looking for developers passionate about web technologies',
                'suggested_timeline': '3-6 months',
                'suggested_team_size': '3-5 people',
                'difficulty_level': 'intermediate',
                'is_featured': True,
            },
            {
                'name': 'Mobile App Development',
                'category': 'mobile',
                'description': 'Create a cross-platform mobile application for iOS and Android.',
                'icon': '📱',
                'template_title': 'Cross-Platform Mobile App',
                'template_description': 'A mobile app that works on both iOS and Android devices.',
                'template_technologies': ['React Native', 'Firebase', 'Expo', 'Redux'],
                'template_looking_for': ['Mobile Developer', 'UI/UX Designer', 'QA Tester'],
                'template_collaboration_needs': 'Looking for mobile developers and designers',
                'suggested_timeline': '2-4 months',
                'suggested_team_size': '2-3 people',
                'difficulty_level': 'intermediate',
                'is_featured': True,
            },
            {
                'name': 'AI/ML Project',
                'category': 'ai',
                'description': 'Build intelligent systems using machine learning and deep learning.',
                'icon': '🤖',
                'template_title': 'AI-Powered Solution',
                'template_description': 'An intelligent application powered by machine learning models.',
                'template_technologies': ['Python', 'TensorFlow', 'PyTorch', 'Jupyter', 'Scikit-learn'],
                'template_looking_for': ['ML Engineer', 'Data Scientist', 'Python Developer'],
                'template_collaboration_needs': 'Looking for ML engineers and data scientists',
                'suggested_timeline': '4-6 months',
                'suggested_team_size': '2-4 people',
                'difficulty_level': 'advanced',
                'is_featured': True,
            },
            {
                'name': 'Data Analysis Dashboard',
                'category': 'data',
                'description': 'Create data visualizations and analytics dashboards.',
                'icon': '📊',
                'template_title': 'Business Analytics Dashboard',
                'template_description': 'A comprehensive dashboard for data visualization and insights.',
                'template_technologies': ['Python', 'Pandas', 'Tableau', 'SQL', 'D3.js'],
                'template_looking_for': ['Data Analyst', 'Database Admin', 'Data Scientist', 'Frontend Developer'],
                'template_collaboration_needs': 'Looking for data professionals and developers',
                'suggested_timeline': '2-3 months',
                'suggested_team_size': '2-3 people',
                'difficulty_level': 'intermediate',
                'is_featured': False,
            },
            {
                'name': 'Blockchain Application',
                'category': 'blockchain',
                'description': 'Develop a decentralized application using blockchain technology.',
                'icon': '⛓️',
                'template_title': 'Decentralized App (DApp)',
                'template_description': 'A blockchain-based application with smart contracts.',
                'template_technologies': ['Solidity', 'Web3.js', 'Ethereum', 'Hardhat', 'React'],
                'template_looking_for': ['Smart Contract Dev', 'Blockchain Dev', 'Security Auditor'],
                'template_collaboration_needs': 'Looking for blockchain developers and security experts',
                'suggested_timeline': '3-6 months',
                'suggested_team_size': '2-4 people',
                'difficulty_level': 'advanced',
                'is_featured': False,
            },
            {
                'name': 'IoT Smart Device',
                'category': 'iot',
                'description': 'Build connected IoT devices and systems.',
                'icon': '📡',
                'template_title': 'Smart IoT System',
                'template_description': 'Connected devices communicating through IoT platforms.',
                'template_technologies': ['Arduino', 'Raspberry Pi', 'MQTT', 'Python', 'Node.js'],
                'template_looking_for': ['Embedded Systems Engineer', 'IoT Developer', 'Hardware Engineer'],
                'template_collaboration_needs': 'Looking for IoT and embedded systems developers',
                'suggested_timeline': '3-4 months',
                'suggested_team_size': '2-3 people',
                'difficulty_level': 'advanced',
                'is_featured': False,
            },
        ]

        created_count = 0
        updated_count = 0

        for template_data in templates_data:
            template, created = ProjectTemplate.objects.update_or_create(
                name=template_data['name'],
                defaults=template_data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'[+] Created template: {template.name}')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'[*] Updated template: {template.name}')
                )
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n[COMPLETE] Template creation finished!\n'
                f'  Created: {created_count}\n'
                f'  Updated: {updated_count}\n'
                f'  Total: {created_count + updated_count}'
            )
        )
