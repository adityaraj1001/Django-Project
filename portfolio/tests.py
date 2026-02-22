from django.test import TestCase
from django.urls import reverse
from .models import Project

class PortfolioTests(TestCase):
    def setUp(self):
        Project.objects.create(
            title="Test Project",
            description="Testing description",
            tech_stack="Python, Django",
            github="https://github.com",
            slug="test-project"
        )

    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_projects_list_status_code(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_status_code(self):
        response = self.client.get(reverse('project_detail', kwargs={'slug': 'test-project'}))
        self.assertEqual(response.status_code, 200)