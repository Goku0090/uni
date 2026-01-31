#!/usr/bin/env python
"""
Performance Monitoring Script for UniSync
Monitors database queries, cache hit rates, and response times
"""

import os
import sys
import django
import time
from datetime import datetime, timedelta
from django.db import connection
from django.core.cache import cache
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from accounts.models import Project, StudentProfile, Connection, Message, Activity
from django.db.models import Count, Avg
from django.utils import timezone

class PerformanceMonitor:
    """Monitor application performance metrics"""

    def __init__(self):
        self.start_time = time.time()

    def get_database_stats(self):
        """Get database performance statistics"""
        print("Database Performance Analysis")
        print("=" * 50)

        # Query execution time
        start = time.time()
        projects_count = Project.objects.count()
        profiles_count = StudentProfile.objects.count()
        connections_count = Connection.objects.count()
        messages_count = Message.objects.count()
        db_query_time = time.time() - start

        print(f"Total Records:")
        print(f"   Projects: {projects_count}")
        print(f"   Profiles: {profiles_count}")
        print(f"   Connections: {connections_count}")
        print(f"   Messages: {messages_count}")
        print(".3f")

        # Database connection info
        print(f"\nDatabase Connections: {len(connection.queries)} queries executed")
        if connection.queries:
            total_query_time = sum(float(q.get('time', 0)) for q in connection.queries)
            print(".3f")
            print(f"   Average query time: {total_query_time / len(connection.queries):.3f}s")

        return {
            'projects_count': projects_count,
            'profiles_count': profiles_count,
            'connections_count': connections_count,
            'messages_count': messages_count,
            'db_query_time': db_query_time
        }

    def get_cache_stats(self):
        """Get cache performance statistics"""
        print("\nCache Performance Analysis")
        print("=" * 50)

        # Test cache operations
        cache_start = time.time()

        # Test cache set/get
        test_key = 'performance_test_key'
        test_value = {'test': 'data', 'timestamp': time.time()}
        cache.set(test_key, test_value, 60)

        retrieved_value = cache.get(test_key)
        cache_hit = retrieved_value == test_value

        cache_time = time.time() - cache_start

        print(f"Cache Status: {'Working' if cache_hit else 'Issues detected'}")
        print(".3f")

        # Check our application caches
        app_caches = [
            'project_categories',
            'project_technologies',
        ]

        print(f"\nApplication Cache Status:")
        for cache_key in app_caches:
            cached_data = cache.get(cache_key)
            status = "Cached" if cached_data is not None else "Not cached"
            print(f"   {cache_key}: {status}")

        return {
            'cache_working': cache_hit,
            'cache_response_time': cache_time
        }

    def get_index_stats(self):
        """Analyze database indexes effectiveness"""
        print("\nDatabase Index Analysis")
        print("=" * 50)

        # Test query performance with and without indexes
        print("Testing query performance...")

        # Test StudentProfile queries (should use indexes)
        start = time.time()
        profiles_by_college = StudentProfile.objects.filter(college__icontains='IIT')[:10]
        college_query_time = time.time() - start

        start = time.time()
        profiles_by_location = StudentProfile.objects.filter(location__icontains='Delhi')[:10]
        location_query_time = time.time() - start

        start = time.time()
        recent_projects = Project.objects.filter(created_at__gte=timezone.now() - timedelta(days=7))[:10]
        project_query_time = time.time() - start

        print(".3f")
        print(".3f")
        print(".3f")

        return {
            'college_query_time': college_query_time,
            'location_query_time': location_query_time,
            'project_query_time': project_query_time
        }

    def get_recommendations(self, stats):
        """Provide performance recommendations"""
        print("\nPerformance Recommendations")
        print("=" * 50)

        recommendations = []

        # Database recommendations
        if stats.get('db_query_time', 0) > 1.0:
            recommendations.append("WARNING: Database queries are slow. Consider adding more indexes or optimizing queries.")

        # Cache recommendations
        if not stats.get('cache_working', False):
            recommendations.append("ERROR: Cache is not working properly. Check Redis/memcached configuration.")

        if stats.get('cache_response_time', 0) > 0.1:
            recommendations.append("SLOW: Cache response time is high. Consider using Redis instead of database cache.")

        # Index recommendations
        if stats.get('college_query_time', 0) > 0.5:
            recommendations.append("SLOW: College queries are slow. Ensure proper indexes on StudentProfile.college.")

        if stats.get('location_query_time', 0) > 0.5:
            recommendations.append("SLOW: Location queries are slow. Ensure proper indexes on StudentProfile.location.")

        if not recommendations:
            recommendations.append("SUCCESS: All performance metrics look good!")

        for rec in recommendations:
            print(rec)

        return recommendations

    def run_full_analysis(self):
        """Run complete performance analysis"""
        print("UniSync Performance Monitor")
        print("=" * 50)
        print(f"Analysis started at: {datetime.now()}")
        print()

        # Run all analyses
        db_stats = self.get_database_stats()
        cache_stats = self.get_cache_stats()
        index_stats = self.get_index_stats()

        # Combine all stats
        all_stats = {**db_stats, **cache_stats, **index_stats}

        # Get recommendations
        recommendations = self.get_recommendations(all_stats)

        # Summary
        total_time = time.time() - self.start_time
        print(".2f")

        return {
            'stats': all_stats,
            'recommendations': recommendations,
            'total_analysis_time': total_time
        }

def main():
    """Main function to run performance monitoring"""
    monitor = PerformanceMonitor()
    results = monitor.run_full_analysis()

    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"performance_report_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write("UniSync Performance Report\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now()}\n\n")

        f.write("Database Stats:\n")
        for key, value in results['stats'].items():
            if isinstance(value, float):
                f.write(f"  {key}: {value:.3f}\n")
            else:
                f.write(f"  {key}: {value}\n")

        f.write("\nRecommendations:\n")
        for rec in results['recommendations']:
            f.write(f"  {rec}\n")

        f.write(".2f")

    print(f"\nReport saved to: {filename}")

if __name__ == '__main__':
    main()
