from django.db import models
from django.utils import timezone


class SchoolProfile(models.Model):
    """
    Singleton model to manage general school information, contacts,
    hero banner content, and administrative text.
    """
    school_name = models.CharField(max_length=200, default="Kigumo Bendera High School")
    subtitle = models.CharField(max_length=200, default="High School • Murang'a")
    motto = models.CharField(
        max_length=250,
        default="Shaping Minds. Building Character. Inspiring Excellence.",
        help_text="Official school motto/tagline"
    )
    about_short = models.TextField(
        default="A premier government-aided secondary boarding school dedicated to nurturing young minds into intellectual giants, disciplined leaders, and ethically grounded global citizens.",
        help_text="Short description displayed in the footer and intro widgets"
    )
    about_full = models.TextField(
        default="Kigumo Bendera High School is a distinguished public secondary boarding school situated in the tranquil, lush environment of Kigumo, Murang'a County. Designed to cultivate academic ambition and principled character, the school has nurtured generations of young scholars into national leaders, engineers, doctors, teachers, entrepreneurs, and public servants.",
        help_text="Full background story displayed on the About Us page"
    )
    vision = models.TextField(
        default="To be a premier national center of holistic secondary education, producing principled, innovative, and competitive scholars."
    )
    mission = models.TextField(
        default="To deliver quality, inclusive, and transformative education through rigorous academic mentorship, disciplined co-curricular engagements, and moral instruction."
    )
    phone = models.CharField(
        max_length=50,
        default="0710336023",
        help_text="Primary telephone number (displayed as 0710336023, links to tel:+254710336023)"
    )
    email = models.EmailField(
        default="kabiraallan79@gmail.com",
        help_text="Primary school email address (links to mailto:kabiraallan79@gmail.com)"
    )
    physical_address = models.CharField(
        max_length=300,
        default="Kigumo Sub-County, Murang'a County, Kenya"
    )
    postal_address = models.CharField(
        max_length=200,
        default="P.O. Box ... Kigumo, Kenya",
        blank=True
    )
    office_hours = models.CharField(
        max_length=150,
        default="Mon - Fri: 8:00 AM - 5:00 PM"
    )
    term_status = models.CharField(
        max_length=100,
        default="Term 1 In Session",
        help_text="Top bar status badge text"
    )
    registration_code = models.CharField(
        max_length=100,
        default="[School Registration Code]",
        blank=True
    )

    # Hero Banner Customization
    hero_badge = models.CharField(
        max_length=200,
        default="Premier Center of Academic & Moral Excellence"
    )
    hero_headline = models.CharField(
        max_length=200,
        default="KIGUMO BENDERA HIGH SCHOOL"
    )
    hero_subtext = models.TextField(
        default='"Shaping Minds. Building Character. Inspiring Excellence." A premier secondary boarding school in Murang\'a County dedicated to transformative education and exemplary leadership.'
    )

    # Key Statistics (Homepage Counters)
    stat_students = models.CharField(max_length=50, default="1,200+", verbose_name="Enrolled Scholars")
    stat_teachers = models.CharField(max_length=50, default="45+", verbose_name="Experienced Tutors")
    stat_university = models.CharField(max_length=50, default="100%", verbose_name="University Prep")
    stat_clubs_sports = models.CharField(max_length=50, default="28+", verbose_name="Clubs & Sports")

    # Principal's Desk
    principal_name = models.CharField(max_length=150, default="[Principal's Name]")
    principal_title = models.CharField(max_length=150, default="Chief Principal")
    principal_quote = models.TextField(
        default="At Kigumo Bendera High School, we believe that education is not merely the transmission of facts, but the ignition of intellect and the steadfast cultivation of character."
    )
    principal_desk_note = models.TextField(
        default="Welcome to Kigumo Bendera High School. For years, our institution has stood as a beacon of academic rigor, self-discipline, and holistic transformation in Murang'a County. Our students are challenged in state-of-the-art laboratories, mentored by passionate faculty, and empowered through rich sporting and co-curricular programs."
    )
    principal_photo = models.ImageField(upload_to='principal/', blank=True, null=True)

    # Media & Social Links
    logo = models.ImageField(upload_to='branding/', blank=True, null=True, help_text="Custom logo if overriding SVG default")
    facebook_url = models.URLField(blank=True, default='#')
    twitter_url = models.URLField(blank=True, default='#')
    youtube_url = models.URLField(blank=True, default='#')
    linkedin_url = models.URLField(blank=True, default='#')

    # Admissions & Financial Guidance
    admission_hotline = models.CharField(max_length=50, default="0710336023")
    boarding_levy_guideline = models.CharField(
        max_length=200,
        default="[Insert Ministry-Approved Fee: KSh. XX,XXX per annum]",
        blank=True
    )
    bank_payment_details = models.CharField(
        max_length=250,
        default="[Bank Name / Branch / Account Number]",
        blank=True
    )

    class Meta:
        verbose_name = "School Profile & General Information"
        verbose_name_plural = "School Profile & General Information"

    def __str__(self):
        return f"{self.school_name} Profile"

    @classmethod
    def get_solo(cls):
        """Retrieve the singleton instance or initialize one with safe defaults."""
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj


class CoreValue(models.Model):
    """Core values displayed on the About Us page and institutional profiles."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=100,
        default="bi bi-shield-lock-fill",
        help_text="Bootstrap Icon class name (e.g. bi bi-trophy-fill, bi bi-hammer)"
    )
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Core Value"
        verbose_name_plural = "Core Values"

    def __str__(self):
        return self.title


class LeadershipMember(models.Model):
    """Board of Management, Principal, and Deputy leadership personnel."""
    CATEGORY_CHOICES = [
        ('BOM', 'Board of Management'),
        ('ADMIN', 'School Administration'),
        ('FACULTY', 'Senior Master / Head of Section'),
    ]

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, help_text="e.g. BOM Chairperson, Chief Principal, Deputy Principal")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ADMIN')
    bio = models.TextField(blank=True, help_text="Brief professional bio or portfolio description")
    photo = models.ImageField(upload_to='leadership/', blank=True, null=True)
    photo_url = models.URLField(max_length=500, blank=True, help_text="Optional fallback image URL")
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Leadership Member"
        verbose_name_plural = "Leadership & Administration"

    def __str__(self):
        return f"{self.name} - {self.role}"


class CampusFacility(models.Model):
    """Physical infrastructure highlights (Science Labs, ICT, Library, Hostels, Fields)."""
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, default="bi bi-building")
    photo = models.ImageField(upload_to='facilities/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Campus Facility"
        verbose_name_plural = "Campus Facilities"

    def __str__(self):
        return self.title


class Department(models.Model):
    """Academic faculties and operational departments."""
    CATEGORY_CHOICES = [
        ('ACADEMIC', 'Academic Faculty'),
        ('OPERATIONAL', 'Operational / Boarding Division'),
        ('SUPPORT', 'Student Support / Welfare'),
    ]

    name = models.CharField(max_length=150, help_text="e.g. Department of Sciences")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ACADEMIC')
    badge_text = models.CharField(max_length=100, default="Core STEM", help_text="e.g. Core STEM, Analytical, Welfare")
    subjects = models.CharField(max_length=300, blank=True, help_text="e.g. Biology • Chemistry • Physics")
    description = models.TextField()
    hod_name = models.CharField(max_length=150, default="[HOD Name]", help_text="Head of Department")
    facilities_summary = models.CharField(max_length=200, default="Dedicated Laboratories", blank=True)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name


class AdmissionStep(models.Model):
    """Steps in the 4-stage admission roadmap."""
    step_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['step_number', 'order']
        verbose_name = "Admission Step"
        verbose_name_plural = "Admission Roadmap Steps"

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class AdmissionFAQ(models.Model):
    """Frequently Asked Questions for prospective students and guardians."""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Admission FAQ"
        verbose_name_plural = "Admission FAQs"

    def __str__(self):
        return self.question


class SportsDiscipline(models.Model):
    """Athletics and games disciplines on the Student Life page."""
    name = models.CharField(max_length=100, help_text="e.g. Football (Soccer), Rugby 7s & 15s")
    subtitle = models.CharField(max_length=150, default="Competitive Squad")
    description = models.TextField()
    icon_class = models.CharField(max_length=100, default="bi bi-trophy")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Sports Discipline"
        verbose_name_plural = "Sports & Athletics Disciplines"

    def __str__(self):
        return self.name


class StudentClub(models.Model):
    """Clubs and societies for co-curricular student life."""
    name = models.CharField(max_length=150, help_text="e.g. Science & Robotics Club")
    description = models.TextField()
    icon_class = models.CharField(max_length=100, default="bi bi-robot")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Student Club / Society"
        verbose_name_plural = "Student Clubs & Societies"

    def __str__(self):
        return self.name


class NewsCategory(models.Model):
    """Categories for news articles and dispatches."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    """News articles and official announcements."""
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=260, unique=True)
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    summary = models.TextField(help_text="Short abstract displayed in cards")
    content = models.TextField(blank=True, help_text="Full article narrative")
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, help_text="Fallback image URL if no file uploaded")
    author = models.CharField(max_length=150, default="Office of the Principal")
    published_date = models.DateField(default=timezone.now)
    is_featured = models.BooleanField(default=False, help_text="Show in featured headline banners")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles & Announcements"

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.featured_image:
            return self.featured_image.url
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=700&auto=format&fit=crop"


class SchoolEvent(models.Model):
    """Upcoming events, term dates, and calendar appointments."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    time = models.CharField(max_length=100, default="9:00 AM - 1:00 PM")
    venue = models.CharField(max_length=200, default="School Main Hall")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['event_date']
        verbose_name = "School Event"
        verbose_name_plural = "School Events & Calendar"

    def __str__(self):
        return f"{self.title} ({self.event_date})"

    @property
    def day_display(self):
        return self.event_date.strftime("%d")

    @property
    def month_display(self):
        return self.event_date.strftime("%b").upper()


class SchoolCircular(models.Model):
    """Downloadable circulars and official PDF memos."""
    title = models.CharField(max_length=200, help_text="e.g. Term 1 Parent Circular.pdf")
    document = models.FileField(upload_to='circulars/', blank=True, null=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "School Circular"
        verbose_name_plural = "Official Circulars & Downloads"

    def __str__(self):
        return self.title


class GalleryCategory(models.Model):
    """Categories for the photo gallery."""
    name = models.CharField(max_length=100)
    code = models.SlugField(max_length=100, unique=True, help_text="e.g. academics, sports, campus, events")

    class Meta:
        ordering = ['name']
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """School gallery media items."""
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.CASCADE,
        related_name='images'
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, help_text="Fallback image URL if no file uploaded")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1541829070764-84a7d30dd3f3?q=80&w=800&auto=format&fit=crop"


class ContactMessage(models.Model):
    """Inquiries submitted through the Contact Us form."""
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    inquiry_type = models.CharField(max_length=100, default='General')
    subject = models.CharField(max_length=250)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    admin_notes = models.TextField(blank=True, help_text="Internal notes by administration (never shown publicly)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.full_name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"


class FeedbackSubmission(models.Model):
    """Submissions from the confidential Feedback & Grievance portal."""
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('UNDER_REVIEW', 'Under Review'),
        ('RESOLVED', 'Resolved'),
    ]

    tracking_code = models.CharField(max_length=50, unique=True, db_index=True)
    reporter_type = models.CharField(max_length=100)
    feedback_category = models.CharField(max_length=150)
    is_anonymous = models.BooleanField(default=False)
    full_name = models.CharField(max_length=150, blank=True)
    contact_info = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=250)
    description = models.TextField()
    desired_outcome = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    admin_notes = models.TextField(blank=True, help_text="Internal review findings and committee notes (confidential)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Feedback & Grievance"
        verbose_name_plural = "Feedback & Grievance Submissions"

    def __str__(self):
        return f"[{self.tracking_code}] {self.subject} ({self.status})"
