from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from .models import ContactMessage, FeedbackSubmission


@staff_member_required
def admin_dashboard(request):
    """Dashboard overview with statistics and recent items."""
    total_contacts = ContactMessage.objects.count()
    new_contacts = ContactMessage.objects.filter(status='NEW').count()
    total_feedback = FeedbackSubmission.objects.count()
    new_feedback = FeedbackSubmission.objects.filter(status='NEW').count()

    recent_contacts = ContactMessage.objects.order_by('-created_at')[:5]
    recent_feedback = FeedbackSubmission.objects.order_by('-created_at')[:5]

    context = {
        'total_contacts': total_contacts,
        'new_contacts': new_contacts,
        'total_feedback': total_feedback,
        'new_feedback': new_feedback,
        'recent_contacts': recent_contacts,
        'recent_feedback': recent_feedback,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


@staff_member_required
def admin_contact_list(request):
    """List contact messages with search, filter, and pagination."""
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    contacts = ContactMessage.objects.all()

    if query:
        contacts = contacts.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(subject__icontains=query) |
            Q(message__icontains=query)
        )
    if status_filter:
        contacts = contacts.filter(status=status_filter)

    contacts = contacts.order_by('-created_at')
    paginator = Paginator(contacts, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
    }
    return render(request, 'admin_dashboard/contact_list.html', context)


@staff_member_required
def admin_contact_detail(request, pk):
    """View and edit a single contact message."""
    contact = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        # Update status and admin notes if provided
        status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '').strip()
        if status in dict(ContactMessage.STATUS_CHOICES):
            contact.status = status
        contact.admin_notes = admin_notes
        contact.save()
        messages.success(request, 'Contact message updated.')
        return redirect('admin_contact_detail', pk=pk)
    return render(request, 'admin_dashboard/contact_detail.html', {'contact': contact})


@staff_member_required
def admin_contact_delete(request, pk):
    contact = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact message deleted.')
        return redirect('admin_contact_list')
    return render(request, 'admin_dashboard/contact_confirm_delete.html', {'contact': contact})


@staff_member_required
def admin_feedback_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    feedback_qs = FeedbackSubmission.objects.all()
    if query:
        feedback_qs = feedback_qs.filter(
            Q(full_name__icontains=query) |
            Q(contact_info__icontains=query) |
            Q(subject__icontains=query) |
            Q(description__icontains=query)
        )
    if status_filter:
        feedback_qs = feedback_qs.filter(status=status_filter)
    feedback_qs = feedback_qs.order_by('-created_at')
    paginator = Paginator(feedback_qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_dashboard/feedback_list.html', {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
    })


@staff_member_required
def admin_feedback_detail(request, pk):
    feedback = get_object_or_404(FeedbackSubmission, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '').strip()
        if status in dict(FeedbackSubmission.STATUS_CHOICES):
            feedback.status = status
        feedback.admin_notes = admin_notes
        feedback.save()
        messages.success(request, 'Feedback updated.')
        return redirect('admin_feedback_detail', pk=pk)
    return render(request, 'admin_dashboard/feedback_detail.html', {'feedback': feedback})


@staff_member_required
def admin_feedback_delete(request, pk):
    feedback = get_object_or_404(FeedbackSubmission, pk=pk)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback deleted.')
        return redirect('admin_feedback_list')
    return render(request, 'admin_dashboard/feedback_confirm_delete.html', {'feedback': feedback})
