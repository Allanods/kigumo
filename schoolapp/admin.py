from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SchoolProfile, CoreValue, LeadershipMember, CampusFacility,
    Department, AdmissionStep, AdmissionFAQ, SportsDiscipline, StudentClub,
    NewsCategory, NewsArticle, SchoolEvent, SchoolCircular,
    GalleryCategory, GalleryImage, ContactMessage, FeedbackSubmission
)

# Custom Admin Site Headers
admin.site.site_header = "Kigumo Bendera High School Management"
admin.site.site_title = "Kigumo Bendera Admin"
admin.site.index_title = "School Administration & Website Content Control"


@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Core Identity & Contacts", {
            "fields": (
                ("school_name", "subtitle"),
                "motto",
                ("phone", "email"),
                ("physical_address", "postal_address"),
                ("office_hours", "term_status"),
                "registration_code",
            )
        }),
        ("Homepage Hero & Counters", {
            "fields": (
                "hero_badge",
                "hero_headline",
                "hero_subtext",
                ("stat_students", "stat_teachers"),
                ("stat_university", "stat_clubs_sports"),
            )
        }),
        ("Office of the Principal", {
            "fields": (
                ("principal_name", "principal_title"),
                "principal_quote",
                "principal_desk_note",
                "principal_photo",
            )
        }),
        ("Vision, Mission & About Stories", {
            "fields": (
                "vision",
                "mission",
                "about_short",
                "about_full",
            )
        }),
        ("Admissions & Fees Information", {
            "fields": (
                "admission_hotline",
                "boarding_levy_guideline",
                "bank_payment_details",
            )
        }),
        ("Branding & Social Media Links", {
            "fields": (
                "logo",
                ("facebook_url", "twitter_url"),
                ("youtube_url", "linkedin_url"),
            )
        }),
    )

    def has_add_permission(self, request):
        # Prevent adding more than one SchoolProfile instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(LeadershipMember)
class LeadershipMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'role', 'bio')


@admin.register(CampusFacility)
class CampusFacilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'badge_text', 'hod_name', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'subjects', 'hod_name', 'description')


@admin.register(AdmissionStep)
class AdmissionStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order')
    list_editable = ('order',)
    ordering = ('step_number', 'order')


@admin.register(AdmissionFAQ)
class AdmissionFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')


@admin.register(SportsDiscipline)
class SportsDisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtitle', 'icon_class', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'description')


@admin.register(StudentClub)
class StudentClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'description')


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_date', 'is_featured', 'is_published')
    list_filter = ('category', 'is_featured', 'is_published', 'published_date')
    list_editable = ('is_featured', 'is_published')
    search_fields = ('title', 'summary', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    actions = ['make_published', 'make_unpublished', 'mark_featured']

    @admin.action(description="Publish selected articles")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Unpublish selected articles")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Mark selected as featured")
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)


@admin.register(SchoolEvent)
class SchoolEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'time', 'venue', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active', 'event_date')
    list_editable = ('is_featured', 'is_active')
    search_fields = ('title', 'venue', 'description')
    date_hierarchy = 'event_date'


@admin.register(SchoolCircular)
class SchoolCircularAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title', 'description')


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    prepopulated_fields = {'code': ('name',)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    list_editable = ('order', 'is_featured')
    search_fields = ('title',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'inquiry_type', 'subject', 'colored_status', 'created_at')
    list_filter = ('status', 'inquiry_type', 'created_at')
    list_editable = ()
    search_fields = ('full_name', 'email', 'phone', 'subject', 'message')
    readonly_fields = ('created_at', 'full_name', 'email', 'phone', 'inquiry_type', 'subject', 'message')
    date_hierarchy = 'created_at'
    actions = ['mark_resolved', 'mark_in_progress']

    @admin.display(description="Status")
    def colored_status(self, obj):
        colors = {
            'NEW': '#DC2626',
            'IN_PROGRESS': '#D97706',
            'RESOLVED': '#059669',
        }
        color = colors.get(obj.status, '#4B5563')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8em;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.action(description="Mark selected messages as Resolved")
    def mark_resolved(self, request, queryset):
        queryset.update(status='RESOLVED')

    @admin.action(description="Mark selected messages as In Progress")
    def mark_in_progress(self, request, queryset):
        queryset.update(status='IN_PROGRESS')


@admin.register(FeedbackSubmission)
class FeedbackSubmissionAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'reporter_type', 'feedback_category', 'is_anonymous', 'full_name', 'colored_status', 'created_at')
    list_filter = ('status', 'reporter_type', 'feedback_category', 'is_anonymous', 'created_at')
    search_fields = ('tracking_code', 'full_name', 'contact_info', 'subject', 'description')
    readonly_fields = ('tracking_code', 'created_at', 'reporter_type', 'feedback_category', 'is_anonymous', 'full_name', 'contact_info', 'subject', 'description', 'desired_outcome')
    date_hierarchy = 'created_at'
    actions = ['mark_resolved', 'mark_under_review']

    @admin.display(description="Status")
    def colored_status(self, obj):
        colors = {
            'NEW': '#DC2626',
            'UNDER_REVIEW': '#D97706',
            'RESOLVED': '#059669',
        }
        color = colors.get(obj.status, '#4B5563')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8em;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.action(description="Mark selected feedback as Resolved")
    def mark_resolved(self, request, queryset):
        queryset.update(status='RESOLVED')

    @admin.action(description="Mark selected feedback as Under Review")
    def mark_under_review(self, request, queryset):
        queryset.update(status='UNDER_REVIEW')
