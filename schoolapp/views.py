import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import (
    SchoolProfile, CoreValue, LeadershipMember, CampusFacility,
    Department, AdmissionStep, AdmissionFAQ, SportsDiscipline, StudentClub,
    NewsCategory, NewsArticle, SchoolEvent, SchoolCircular,
    GalleryCategory, GalleryImage, ContactMessage, FeedbackSubmission
)


def home(request):
    """Homepage view querying dynamic school profile, recent news, events, and pillars."""
    profile = SchoolProfile.get_solo()
    recent_news = NewsArticle.objects.filter(is_published=True)[:3]
    upcoming_events = SchoolEvent.objects.filter(is_active=True)[:3]
    pillars = CoreValue.objects.all()[:4]

    context = {
        'profile': profile,
        'recent_news': recent_news,
        'upcoming_events': upcoming_events,
        'pillars': pillars,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    """About Us page: History, Vision, Mission, Values, Leadership, Facilities."""
    profile = SchoolProfile.get_solo()
    core_values = CoreValue.objects.all()
    leadership_members = LeadershipMember.objects.filter(is_active=True)
    facilities = CampusFacility.objects.all()

    context = {
        'profile': profile,
        'core_values': core_values,
        'leadership_members': leadership_members,
        'facilities': facilities,
    }
    return render(request, 'pages/about.html', context)


def academics(request):
    """Academics page: Curriculum pathways, departments, support programs."""
    profile = SchoolProfile.get_solo()
    departments = Department.objects.filter(is_active=True, category='ACADEMIC')

    context = {
        'profile': profile,
        'academic_departments': departments,
    }
    return render(request, 'pages/academics.html', context)


def admissions(request):
    """Admissions page: Intake roadmap steps, fees guidance, and FAQ accordion."""
    profile = SchoolProfile.get_solo()
    steps = AdmissionStep.objects.all()
    faqs = AdmissionFAQ.objects.filter(is_active=True)

    context = {
        'profile': profile,
        'admission_steps': steps,
        'faqs': faqs,
    }
    return render(request, 'pages/admissions.html', context)


def student_life(request):
    """Student Life: Sports disciplines, clubs & societies, boarding life."""
    sports = SportsDiscipline.objects.all()
    clubs = StudentClub.objects.all()

    context = {
        'sports_disciplines': sports,
        'student_clubs': clubs,
    }
    return render(request, 'pages/student_life.html', context)


def departments(request):
    """Departments: Sciences, Math, Languages, Humanities, Welfare."""
    all_departments = Department.objects.filter(is_active=True)

    context = {
        'departments_list': all_departments,
    }
    return render(request, 'pages/departments.html', context)


def news(request):
    """News & Events: Full articles, event calendar, official circulars."""
    featured_news = NewsArticle.objects.filter(is_published=True, is_featured=True).first()
    news_articles = NewsArticle.objects.filter(is_published=True)
    upcoming_events = SchoolEvent.objects.filter(is_active=True)
    circulars = SchoolCircular.objects.all()

    context = {
        'featured_news': featured_news,
        'news_articles': news_articles,
        'upcoming_events': upcoming_events,
        'circulars': circulars,
    }
    return render(request, 'pages/news.html', context)


def gallery(request):
    """Photo Gallery: Dynamic categories and images with lightbox support."""
    categories = GalleryCategory.objects.all()
    gallery_items = GalleryImage.objects.select_related('category').all()

    context = {
        'categories': categories,
        'gallery_items': gallery_items,
    }
    return render(request, 'pages/gallery.html', context)


def contact(request):
    """Contact page: Displays office info and saves submissions to ContactMessage model."""
    profile = SchoolProfile.get_solo()

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        inquiry_type = request.POST.get('inquiry_type', 'General')
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if full_name and email and subject and message_text:
            ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                inquiry_type=inquiry_type,
                subject=subject,
                message=message_text,
                status='NEW'
            )
            messages.success(
                request,
                f"Thank you, {full_name}. Your inquiry regarding '{inquiry_type}' has been successfully logged into the school administration system. Our administrative desk will reach out to you."
            )
        else:
            messages.error(request, "Please complete all mandatory fields before submitting.")

        return redirect('contact')

    return render(request, 'pages/contact.html', {'profile': profile})


def feedback(request):
    """Feedback & Grievance Portal: Saves confidential records to FeedbackSubmission model."""
    if request.method == 'POST':
        reporter_type = request.POST.get('reporter_type', 'General')
        feedback_category = request.POST.get('feedback_category', 'General')
        is_anonymous = request.POST.get('is_anonymous') == 'true'
        full_name = '' if is_anonymous else request.POST.get('full_name', '').strip()
        contact_info = '' if is_anonymous else request.POST.get('contact_info', '').strip()
        subject = request.POST.get('subject', '').strip()
        description = request.POST.get('description', '').strip()
        desired_outcome = request.POST.get('desired_outcome', '').strip()

        # Generate unique tracking code
        tracking_code = f"KB-{random.randint(100000, 999999)}"

        if subject and description:
            FeedbackSubmission.objects.create(
                tracking_code=tracking_code,
                reporter_type=reporter_type,
                feedback_category=feedback_category,
                is_anonymous=is_anonymous,
                full_name=full_name,
                contact_info=contact_info,
                subject=subject,
                description=description,
                desired_outcome=desired_outcome,
                status='NEW'
            )
            messages.success(
                request,
                f"Your submission has been safely registered under reference code [{tracking_code}]. The School Grievance Committee will assess the matter with utmost confidentiality."
            )
        else:
            messages.error(request, "Please provide the headline and description of your submission.")

        return redirect('feedback')

    return render(request, 'pages/feedback.html')
