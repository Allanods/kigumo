from django.test import TestCase, Client
from django.urls import reverse


class SchoolWebPagesTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_all_pages_render_successfully(self):
        pages = [
            ('home', 'pages/home.html'),
            ('about', 'pages/about.html'),
            ('academics', 'pages/academics.html'),
            ('admissions', 'pages/admissions.html'),
            ('student_life', 'pages/student_life.html'),
            ('departments', 'pages/departments.html'),
            ('news', 'pages/news.html'),
            ('gallery', 'pages/gallery.html'),
            ('contact', 'pages/contact.html'),
            ('feedback', 'pages/feedback.html'),
        ]
        for url_name, template_name in pages:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)
                self.assertTemplateUsed(response, 'base.html')
                self.assertContains(response, 'KIGUMO BENDERA')

    def test_contact_form_post(self):
        response = self.client.post(reverse('contact'), {
            'full_name': 'Mary Wambui',
            'email': 'mary@example.com',
            'phone': '0712345678',
            'inquiry_type': 'Admissions',
            'subject': 'Inquiry on Form 1 Intake',
            'message': 'Please share details regarding reporting dates.',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you, Mary Wambui')

    def test_feedback_form_post(self):
        response = self.client.post(reverse('feedback'), {
            'reporter_type': 'Parent/Guardian',
            'feedback_category': 'Academic Standards',
            'full_name': 'Parent James',
            'contact_info': 'james@example.com',
            'subject': 'Commendation on Math Clinics',
            'description': 'The weekend math clinics have noticeably improved my sons grades.',
            'desired_outcome': 'Keep up the great program.',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your submission under')
