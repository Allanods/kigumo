from .models import SchoolProfile


def school_context(request):
    """
    Context processor to inject the SchoolProfile singleton into all templates.
    Guarantees that phone, email, motto, and addresses are accessible globally
    in base.html, navbar.html, footer.html, and all pages without query repetition.
    """
    try:
        profile = SchoolProfile.get_solo()
    except Exception:
        profile = None

    return {
        'school_profile': profile,
    }
