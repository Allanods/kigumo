/**
 * Kigumo Bendera High School - Main Interactive JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Navbar scroll effect
  const navbar = document.querySelector('.site-navbar');
  const backToTopBtn = document.querySelector('.back-to-top-btn');

  window.addEventListener('scroll', function () {
    const scrollY = window.scrollY;
    
    if (navbar) {
      if (scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }

    if (backToTopBtn) {
      if (scrollY > 350) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    }
  });

  // 2. Back to top button action
  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // 3. Auto dismiss alert messages after 5 seconds
  const autoAlerts = document.querySelectorAll('.alert-dismissible');
  autoAlerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 5000);
  });

  // 4. Gallery Category Filter
  const filterBtns = document.querySelectorAll('.filter-btn');
  const galleryItems = document.querySelectorAll('.gallery-item-wrapper');

  if (filterBtns.length > 0 && galleryItems.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        filterBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');

        const filter = this.getAttribute('data-filter');

        galleryItems.forEach(item => {
          const category = item.getAttribute('data-category');
          if (filter === 'all' || category === filter) {
            item.style.display = 'block';
            item.classList.add('animate-fade-in');
          } else {
            item.style.display = 'none';
            item.classList.remove('animate-fade-in');
          }
        });
      });
    });
  }

  // 5. Gallery Lightbox Modal Handler
  const galleryCards = document.querySelectorAll('.gallery-item');
  const lightboxModal = document.getElementById('galleryLightboxModal');
  const lightboxImg = document.getElementById('lightboxImage');
  const lightboxTitle = document.getElementById('lightboxTitle');
  const lightboxCategory = document.getElementById('lightboxCategory');

  if (galleryCards.length > 0 && lightboxModal && lightboxImg) {
    galleryCards.forEach(card => {
      card.addEventListener('click', function () {
        const img = this.querySelector('img');
        const title = this.querySelector('.gallery-caption-title')?.textContent || 'School Gallery';
        const category = this.querySelector('.gallery-caption-category')?.textContent || 'Campus';

        if (img) {
          lightboxImg.src = img.src;
          lightboxImg.alt = img.alt || title;
        }
        if (lightboxTitle) lightboxTitle.textContent = title;
        if (lightboxCategory) lightboxCategory.textContent = category;

        const modal = new bootstrap.Modal(lightboxModal);
        modal.show();
      });
    });
  }

  // 6. Mobile off-canvas link click auto-close
  const offcanvasEl = document.getElementById('mobileNavOffcanvas');
  if (offcanvasEl) {
    const navLinks = offcanvasEl.querySelectorAll('.nav-link, .dropdown-item');
    navLinks.forEach(link => {
      link.addEventListener('click', function () {
        const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasEl);
        if (offcanvas) {
          offcanvas.hide();
        }
      });
    });
  }

  // 7. Feedback Form Reference Code Generator (Interactive simulation)
  const feedbackForm = document.getElementById('grievanceForm');
  const refCodeOutput = document.getElementById('generatedRefCode');
  const refCodeContainer = document.getElementById('refCodeContainer');

  if (feedbackForm && refCodeOutput && refCodeContainer) {
    feedbackForm.addEventListener('submit', function (e) {
      // Allow form submission, but generate a tracking code for user visual reassurance
      const randomId = 'KB-' + Math.floor(100000 + Math.random() * 900000);
      refCodeOutput.textContent = randomId;
      refCodeContainer.classList.remove('d-none');
    });
  }

  // 8. Reveal-on-scroll (progressive enhancement; skipped for reduced motion)
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reducedMotion || revealEls.length === 0) {
      revealEls.forEach(el => el.classList.add('visible'));
    } else {
      const revealObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

      revealEls.forEach(el => revealObserver.observe(el));
    }
  } else {
    revealEls.forEach(el => el.classList.add('visible'));
  }
});
