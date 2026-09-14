from django.urls import path
from . import admin_views

urlpatterns = [
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/contacts/', admin_views.admin_contact_list, name='admin_contact_list'),
    path('admin-dashboard/contacts/<int:pk>/', admin_views.admin_contact_detail, name='admin_contact_detail'),
    path('admin-dashboard/contacts/<int:pk>/delete/', admin_views.admin_contact_delete, name='admin_contact_delete'),
    path('admin-dashboard/feedback/', admin_views.admin_feedback_list, name='admin_feedback_list'),
    path('admin-dashboard/feedback/<int:pk>/', admin_views.admin_feedback_detail, name='admin_feedback_detail'),
    path('admin-dashboard/feedback/<int:pk>/delete/', admin_views.admin_feedback_delete, name='admin_feedback_delete'),
]
