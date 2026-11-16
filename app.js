/**
 * NEVO TECH - Main Interactive Application Script
 * 3D Tilt Physics, Sound Synth, Modal Estimator, Testimonial Slider, & UI Dynamics
 */

document.addEventListener('DOMContentLoaded', () => {

  // =================================================================
  // 0. STYLISH SMOOTH PRELOADER
  // Handled immediately by inline preloader script in index.html
  // =================================================================

  // =================================================================
  // 1. WEB AUDIO API SYNTHESIZER (CYBER SFX)
  // =================================================================
  let audioCtx = null;
  let isSoundMuted = true; // Default muted for smooth user experience

  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audioCtx = new AudioContext();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  window.playSfx = function(type) {
    // Audio FX disabled
  };

  // Audio FX removed upon request

  // =================================================================
  // 3. 3D CARD TILT WITH SPECULAR GLARE
  // =================================================================
  const tiltCards = document.querySelectorAll('.service-card-3d, .project-card, .about-visual-container');

  tiltCards.forEach(card => {
    if (!card.querySelector('.card-glare') && card.classList.contains('service-card-3d')) {
      const glare = document.createElement('div');
      glare.className = 'card-glare';
      card.appendChild(glare);
    }

    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      // Calculate tilt angles (limit to max 10 deg)
      const rotateX = ((y - centerY) / centerY) * -10;
      const rotateY = ((x - centerX) / centerX) * 10;

      card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`;

      const glare = card.querySelector('.card-glare');
      if (glare) {
        glare.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255, 255, 255, 0.42) 0%, transparent 60%)`;
      }
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      card.style.transition = 'transform 0.5s ease-out';
      const glare = card.querySelector('.card-glare');
      if (glare) {
        glare.style.background = 'none';
      }
    });

    card.addEventListener('mouseenter', () => {
      card.style.transition = 'none';
    });
  });

  // =================================================================
  // 4. ANIMATED STATS COUNTER
  // =================================================================
  const statsElements = document.querySelectorAll('.stat-number');
  let statsTriggered = false;

  function runStatsCounter() {
    statsElements.forEach(el => {
      const target = parseInt(el.getAttribute('data-target') || '0', 10);
      const suffix = el.getAttribute('data-suffix') || '';
      let current = 0;
      const increment = Math.ceil(target / 45);
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        el.textContent = `${current}${suffix}`;
      }, 35);
    });
  }

  const statsSection = document.querySelector('.hero-stats-bar');
  if (statsSection) {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !statsTriggered) {
        statsTriggered = true;
        runStatsCounter();
      }
    }, { threshold: 0.3 });
    observer.observe(statsSection);
  }

  // =================================================================
  // 5. MOBILE MENU
  // =================================================================
  const mobileToggle = document.querySelector('.mobile-toggle');
  const navMenu = document.querySelector('.nav-menu');
  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      if (window.playSfx) playSfx('click');
    });

    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
      });
    });
  }

  // =================================================================
  // 6. PROJECT FILTER TABS
  // =================================================================
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const category = btn.getAttribute('data-filter');

      playSfx('click');

      projectCards.forEach(card => {
        const cardCat = card.getAttribute('data-category');
        if (category === 'all' || cardCat === category) {
          card.style.display = 'flex';
          card.style.animation = 'slideUpFade 0.35s ease';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // =================================================================
  // 7. TESTIMONIAL CAROUSEL
  // =================================================================
  const testimonials = [
    {
      quote: "“The Technical Internship Program at NEVO TECH gave me production Git repository experience, Docker containerization, and weekly mentor code reviews. It was the deciding factor in clearing my engineering interviews.”",
      name: "Aditya Verma",
      title: "Full-Stack Engineering Intern (Placed at Tier-1 Firm)",
      avatar: "assets/client-rohan.svg",
      stars: "★★★★★"
    },
    {
      quote: "“Hands-on exposure to real-world customer transactional datasets, SQL window functions, and interactive PowerBI executive dashboards. The internship bridged academic theory and corporate analytics expectations perfectly.”",
      name: "Sneha Kulkarni",
      title: "Business & Analytics Intern (Data Analyst)",
      avatar: "assets/client-rohan.svg",
      stars: "★★★★★"
    },
    {
      quote: "“NEVO TECH's customized project development and survey-based research reports adhere to impeccable academic and industrial standards. From statistical methodology to IEEE-format documentation, their execution is unmatched.”",
      name: "Dr. Rajesh Sharma",
      title: "Head of Research & Dean, Academic Partner Institution",
      avatar: "assets/client-rohan.svg",
      stars: "★★★★★"
    }
  ];

  let currentTestimonialIndex = 0;
  const quoteEl = document.getElementById('testimonial-quote');
  const authorNameEl = document.getElementById('testimonial-author-name');
  const authorTitleEl = document.getElementById('testimonial-author-title');
  const authorAvatarEl = document.getElementById('testimonial-avatar');
  const dotsContainer = document.getElementById('carousel-dots');

  function renderTestimonial(index) {
    if (!quoteEl) return;
    const item = testimonials[index];

    quoteEl.style.opacity = '0';
    quoteEl.style.transform = 'translateY(10px)';

    setTimeout(() => {
      quoteEl.textContent = item.quote;
      authorNameEl.textContent = item.name;
      authorTitleEl.textContent = item.title;
      if (authorAvatarEl) authorAvatarEl.src = item.avatar;

      quoteEl.style.transition = 'all 0.3s ease';
      quoteEl.style.opacity = '1';
      quoteEl.style.transform = 'translateY(0)';

      // Update dots
      if (dotsContainer) {
        Array.from(dotsContainer.children).forEach((dot, idx) => {
          dot.classList.toggle('active', idx === index);
        });
      }
    }, 200);
  }

  // Dots setup
  if (dotsContainer) {
    dotsContainer.innerHTML = '';
    testimonials.forEach((_, idx) => {
      const dot = document.createElement('div');
      dot.className = `dot ${idx === 0 ? 'active' : ''}`;
      dot.addEventListener('click', () => {
        currentTestimonialIndex = idx;
        renderTestimonial(idx);
        playSfx('click');
      });
      dotsContainer.appendChild(dot);
    });
  }

  const prevBtn = document.getElementById('testimonial-prev');
  const nextBtn = document.getElementById('testimonial-next');

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      currentTestimonialIndex = (currentTestimonialIndex - 1 + testimonials.length) % testimonials.length;
      renderTestimonial(currentTestimonialIndex);
      playSfx('click');
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      currentTestimonialIndex = (currentTestimonialIndex + 1) % testimonials.length;
      renderTestimonial(currentTestimonialIndex);
      playSfx('click');
    });
  }

  // =================================================================
  // 8. INTERACTIVE "GET A QUOTE" ESTIMATOR MODAL
  // =================================================================
  const quoteModal = document.getElementById('quote-modal');
  const openQuoteBtns = document.querySelectorAll('.open-quote-modal');
  const closeQuoteBtn = document.getElementById('close-quote-modal');

  openQuoteBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (navMenu) navMenu.classList.remove('open');
      if (quoteModal) {
        quoteModal.classList.add('active');
        playSfx('modal');
      }
    });
  });

  if (closeQuoteBtn && quoteModal) {
    closeQuoteBtn.addEventListener('click', () => {
      quoteModal.classList.remove('active');
      playSfx('click');
    });
    quoteModal.addEventListener('click', (e) => {
      if (e.target === quoteModal) {
        quoteModal.classList.remove('active');
      }
    });
  }

  // Quote Calculator Logic
  const serviceChips = document.querySelectorAll('.calc-chip[data-service]');
  const budgetSlider = document.getElementById('budget-slider');
  const budgetValDisplay = document.getElementById('budget-value-display');
  const estimateTotalDisplay = document.getElementById('estimate-total-display');

  const basePrices = {
    'tech-internship': 800,
    'business-internship': 700,
    'custom-projects': 2200,
    'survey-research': 1400
  };

  let selectedServices = Array.from(serviceChips)
    .filter(chip => chip.classList.contains('selected'))
    .map(chip => chip.getAttribute('data-service'));

  function updateEstimate() {
    const budget = budgetSlider ? parseInt(budgetSlider.value, 10) : 3000;
    const chipTotal = selectedServices.reduce((sum, s) => sum + (basePrices[s] || 1000), 0);
    const highEstimate = Math.max(budget, chipTotal);
    const lowEstimate = Math.max(500, Math.round(highEstimate * 0.85));
    if (estimateTotalDisplay) {
      estimateTotalDisplay.textContent = `$${lowEstimate.toLocaleString()} – $${highEstimate.toLocaleString()}`;
    }
  }

  serviceChips.forEach(chip => {
    chip.addEventListener('click', () => {
      chip.classList.toggle('selected');
      const service = chip.getAttribute('data-service');
      if (selectedServices.includes(service)) {
        selectedServices = selectedServices.filter(s => s !== service);
      } else {
        selectedServices.push(service);
      }
      playSfx('click');
      updateEstimate();
    });
  });

  if (budgetSlider && budgetValDisplay) {
    budgetSlider.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10);
      budgetValDisplay.textContent = `$${val.toLocaleString()}`;
      updateEstimate();
    });
  }

  updateEstimate();

  // Quote Form Submission with Confetti
  const quoteForm = document.getElementById('quote-form');
  if (quoteForm) {
    quoteForm.addEventListener('submit', (e) => {
      e.preventDefault();
      playSfx('success');

      // Trigger Confetti Celebration if canvas-confetti is loaded
      if (typeof confetti === 'function') {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
      }

      showToast("Quote Request Sent! Our team will contact you within 2 hours.");
      setTimeout(() => {
        if (quoteModal) quoteModal.classList.remove('active');
        quoteForm.reset();
        if (budgetSlider && budgetValDisplay) {
          const resetVal = parseInt(budgetSlider.value, 10);
          budgetValDisplay.textContent = `$${resetVal.toLocaleString()}`;
        }
        selectedServices = Array.from(serviceChips)
          .filter(chip => chip.classList.contains('selected'))
          .map(chip => chip.getAttribute('data-service'));
        updateEstimate();
      }, 1500);
    });
  }

  // =================================================================
  // 9. "WATCH OUR STORY" VIDEO REEL MODAL & TECHNICAL 3D SIMULATION
  // =================================================================
  const storyModal = document.getElementById('story-modal');
  const openStoryBtn = document.getElementById('open-story-modal');
  const closeStoryBtn = document.getElementById('close-story-modal');

  let storySceneInitialized = false;
  function initStoryTechnicalCanvas() {
    if (storySceneInitialized) return;
    const canvas = document.getElementById('story-neural-canvas');
    if (!canvas || typeof THREE === 'undefined') return;

    storySceneInitialized = true;
    const container = document.getElementById('tech-story-3d-canvas');
    const w = (container ? container.clientWidth : 650) || 650;
    const h = 210;

    const sScene = new THREE.Scene();
    const sCam = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
    sCam.position.set(0, 4, 18);
    sCam.lookAt(0, 0, 0);

    const sRen = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    sRen.setSize(w, h);
    sRen.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Rotating Technical Lattice
    const sphereGeo = new THREE.IcosahedronGeometry(4.2, 2);
    const sphereMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0.65 });
    const sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
    sScene.add(sphereMesh);

    // Inner glowing core
    const innerGeo = new THREE.OctahedronGeometry(2.0, 1);
    const innerMat = new THREE.MeshBasicMaterial({ color: 0x89e3f5, wireframe: false });
    const innerMesh = new THREE.Mesh(innerGeo, innerMat);
    sScene.add(innerMesh);

    // Orbital Ring
    const oRingGeo = new THREE.TorusGeometry(6.2, 0.12, 8, 48);
    const oRingMat = new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.8 });
    const oRing = new THREE.Mesh(oRingGeo, oRingMat);
    oRing.rotation.x = Math.PI / 3;
    sScene.add(oRing);

    function loopStory() {
      if (storyModal && storyModal.classList.contains('active')) {
        sphereMesh.rotation.y += 0.014;
        sphereMesh.rotation.x += 0.007;
        innerMesh.rotation.y -= 0.018;
        oRing.rotation.z += 0.015;
        sRen.render(sScene, sCam);
      }
      requestAnimationFrame(loopStory);
    }
    loopStory();
  }

  if (openStoryBtn && storyModal) {
    openStoryBtn.addEventListener('click', (e) => {
      e.preventDefault();
      storyModal.classList.add('active');
      playSfx('modal');
      setTimeout(initStoryTechnicalCanvas, 50);
    });
  }

  if (closeStoryBtn && storyModal) {
    closeStoryBtn.addEventListener('click', () => {
      storyModal.classList.remove('active');
      playSfx('click');
    });
    storyModal.addEventListener('click', (e) => {
      if (e.target === storyModal) {
        storyModal.classList.remove('active');
      }
    });
  }

  // =================================================================
  // 10. PROJECT PREVIEW MODAL
  // =================================================================
  const projectModal = document.getElementById('project-modal');
  const closeProjectModal = document.getElementById('close-project-modal');
  const projectDetails = {
    tech_internship_capstone: {
      title: "Cloud-Native Microservices & AI Pipeline (Internship Capstone)",
      tag: "Technical Internship / Full-Stack & Cloud",
      desc: "Engineered during our 8-week Technical Internship Program. Built with modern microservices, Docker, Kubernetes manifests, and automated GitHub Actions CI/CD. Interns solved real sprint tickets, reviewed pull requests, and delivered containerized API services with sub-40ms latency.",
      stats: ["Production CI/CD", "Docker & Kubernetes", "Live Mentorship", "Verified Certificate"]
    },
    business_analytics_capstone: {
      title: "Omni-Channel Customer Intelligence & Forecast Engine",
      tag: "Business & Analytics Internship / BI",
      desc: "Developed in our Business & Analytics Internship track. Leverages real-world transactional datasets, advanced SQL aggregations, Python predictive modeling, and interactive PowerBI/Tableau executive dashboards for predictive churn and revenue forecasting.",
      stats: ["Predictive ML Models", "SQL & Python BI", "PowerBI Dashboards", "Executive Presentation"]
    },
    custom_technical_project: {
      title: "IoT Smart Edge Automation & Full Technical Documentation",
      tag: "Customized Technical Project / IEEE Standard",
      desc: "Turnkey customized engineering solution delivering clean source code, hardware/software integration, circuit blueprints, unit test suites, and a comprehensive 80+ page IEEE-format project documentation dossier ready for academic or enterprise submission.",
      stats: ["Full Source Code", "IEEE Dossier Included", "Zero Plagiarism", "100% Viva Ready"]
    },
    survey_research_study: {
      title: "FinTech Adoption & Consumer Sentiment Empirical Study",
      tag: "Survey-Based Project & Research Report",
      desc: "Empirical market research report based on 1,200+ respondent survey data. Includes validated questionnaire design, Cronbach's alpha reliability checks, ANOVA and multivariate regression in SPSS/R, and a publication-ready academic manuscript.",
      stats: ["1,200+ Validated Responses", "SPSS / R Analysis", "Publication-Ready", "Comprehensive Methodology"]
    },
    // Backwards-compatible aliases
    devsync: {
      title: "Cloud-Native Microservices & AI Pipeline (Internship Capstone)",
      tag: "Technical Internship / Full-Stack & Cloud",
      desc: "Engineered during our 8-week Technical Internship Program with Docker, Kubernetes, and automated CI/CD pipelines.",
      stats: ["Production CI/CD", "Docker & Kubernetes", "Live Mentorship", "Verified Certificate"]
    },
    heavymachinery: {
      title: "Omni-Channel Customer Intelligence & Forecast Engine",
      tag: "Business & Analytics Internship / BI",
      desc: "Developed in our Business & Analytics Internship track with Python predictive modeling and interactive PowerBI dashboards.",
      stats: ["Predictive ML Models", "SQL & Python BI", "PowerBI Dashboards", "Executive Presentation"]
    },
    collegeportal: {
      title: "IoT Smart Edge Automation & Full Technical Documentation",
      tag: "Customized Technical Project / IEEE Standard",
      desc: "Turnkey customized engineering solution delivering clean source code and comprehensive 80+ page IEEE-format project documentation.",
      stats: ["Full Source Code", "IEEE Dossier Included", "Zero Plagiarism", "100% Viva Ready"]
    }
  };

  window.openProjectModal = function(projectId) {
    const data = projectDetails[projectId];
    if (!data || !projectModal) return;

    document.getElementById('project-modal-title').textContent = data.title;
    document.getElementById('project-modal-tag').textContent = data.tag;
    document.getElementById('project-modal-desc').textContent = data.desc;

    const statsContainer = document.getElementById('project-modal-stats');
    if (statsContainer) {
      statsContainer.innerHTML = data.stats.map(s => `<span class="calc-chip selected">${s}</span>`).join('');
    }

    projectModal.classList.add('active');
    playSfx('modal');
  };

  if (closeProjectModal && projectModal) {
    closeProjectModal.addEventListener('click', () => {
      projectModal.classList.remove('active');
      playSfx('click');
    });
    projectModal.addEventListener('click', (e) => {
      if (e.target === projectModal) {
        projectModal.classList.remove('active');
      }
    });
  }

  // =================================================================
  // 11. TOAST NOTIFICATION HELPER
  // =================================================================
  function showToast(message) {
    const toast = document.getElementById('toast-notification');
    const toastMsg = document.getElementById('toast-message');
    if (toast && toastMsg) {
      toastMsg.textContent = message;
      toast.classList.add('show');
      setTimeout(() => {
        toast.classList.remove('show');
      }, 3500);
    }
  }

  window.showToast = showToast;

  // =================================================================
  // 13. PROFESSIONAL ADVANCED INERTIAL SCROLL ENGINE (APPLE / LINEAR / STRIPE)
  // =================================================================
  let lenis = null;
  let isSmoothScrollActive = true;

  const scrollProgressBar = document.getElementById('scroll-progress-line');
  const scrollProgressCircle = document.getElementById('scroll-progress-circle');
  const backToTopBtn = document.getElementById('back-to-top-btn') || document.querySelector('.back-to-top');
  const navbar = document.querySelector('.navbar');
  const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
  const trackedSections = document.querySelectorAll('section[id], header[id]');

  const CIRCUMFERENCE = 125.66; // 2 * PI * 20 (SVG r=20)

  // Top-tier inertial parameters (buttery smooth, immediate response, natural glide)
  const SCROLL_CONFIG = {
    duration: 1.15,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    orientation: 'vertical',
    gestureOrientation: 'vertical',
    smoothWheel: true,
    wheelMultiplier: 1.02,
    touchMultiplier: 1.0,
    syncTouch: false, // Ensures native 120Hz smooth touch momentum on mobile
    infinite: false,
    autoResize: true
  };

  // Nav Scrollspy: Dynamically highlight the active section in the navbar
  function updateScrollspy(currentY) {
    if (!trackedSections.length || !navLinks.length) return;
    const scrollPos = currentY + window.innerHeight * 0.35;

    let currentSectionId = '';
    trackedSections.forEach(sec => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        currentSectionId = sec.id;
      }
    });

    if (currentSectionId) {
      navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === `#${currentSectionId}`) {
          link.classList.add('active');
        } else if (href && href.startsWith('#')) {
          link.classList.remove('active');
        }
      });
    }
  }

  // Visual indicators update (Top progress line, circular back-to-top ring, navbar elevation)
  function handleScrollUpdate(scroll, progress) {
    // 1. Glowing top progress bar
    if (scrollProgressBar) {
      scrollProgressBar.style.width = `${Math.min(100, Math.max(0, progress * 100)).toFixed(1)}%`;
    }

    // 2. Circular Back-to-Top Progress Ring
    if (scrollProgressCircle) {
      const offset = CIRCUMFERENCE - (progress * CIRCUMFERENCE);
      scrollProgressCircle.style.strokeDashoffset = `${Math.max(0, offset).toFixed(2)}`;
    }

    // 3. Back-to-top button visibility
    if (backToTopBtn) {
      if (scroll > 280) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    }

    // 4. Navbar scroll elevation & backdrop blur
    if (navbar) {
      if (scroll > 35) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }

    // 5. Intelligent Nav Scrollspy
    updateScrollspy(scroll);
  }

  function initSmoothScroll() {
    if (typeof Lenis !== 'undefined') {
      try {
        lenis = new Lenis(SCROLL_CONFIG);

        lenis.on('scroll', ({ scroll, progress }) => {
          handleScrollUpdate(scroll, progress);
        });

        function raf(time) {
          if (lenis && isSmoothScrollActive) {
            lenis.raf(time);
          }
          requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);

        isSmoothScrollActive = true;
        window.lenis = lenis;
      } catch (err) {
        console.warn('Lenis initialization fallback:', err);
        setupNativeScrollFallback();
      }
    } else {
      setupNativeScrollFallback();
    }
  }

  function setupNativeScrollFallback() {
    window.addEventListener('scroll', () => {
      const scroll = window.scrollY || window.pageYOffset;
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      const progress = maxScroll > 0 ? scroll / maxScroll : 0;
      handleScrollUpdate(scroll, progress);
    }, { passive: true });
  }

  // Smooth scroll for all internal anchor links via Lenis
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          if (lenis && isSmoothScrollActive) {
            lenis.scrollTo(targetElement, { offset: -75, duration: 1.15 });
          } else {
            targetElement.scrollIntoView({ behavior: 'smooth' });
          }

          // Close mobile menu if open
          const navMenu = document.querySelector('.nav-menu');
          if (navMenu && navMenu.classList.contains('open')) {
            navMenu.classList.remove('open');
          }
        }
      }
    });
  });

  // Back to Top button click
  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', (e) => {
      e.preventDefault();
      if (lenis && isSmoothScrollActive) {
        lenis.scrollTo(0, { duration: 1.15 });
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  }

  // Initialize smooth scroll engine
  initSmoothScroll();

  // Scroll Reveal 3D Observer with Smooth Cinematic Stagger
  const revealElements = document.querySelectorAll(
    '.section-header, .service-card-3d-wrap, .project-card, .process-card, .industry-card, .testimonial-card, .cta-card-content, .stats-bar, .deliverable-card'
  );
  revealElements.forEach(el => el.classList.add('scroll-reveal-3d'));

  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -25px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    revealElements.forEach(el => el.classList.add('in-view'));
  }


  // =================================================================
  // ONLINE SERVICE ENQUIRY & MODAL SUITE (ZERO AMOUNT ARCHITECTURE)
  // =================================================================
  function initEnquirySuite() {
    const modal = document.getElementById('enquiry-modal');
    const closeBtn = document.getElementById('enquiry-modal-close');
    const enquiryForms = Array.from(document.querySelectorAll('.nevo-enquiry-form'));

    function addHoneypot(form) {
      if (form.querySelector('[name="website"]')) return;
      const wrapper = document.createElement('div');
      wrapper.setAttribute('aria-hidden', 'true');
      wrapper.style.cssText = 'position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden;';
      const input = document.createElement('input');
      input.type = 'text';
      input.name = 'website';
      input.tabIndex = -1;
      input.autocomplete = 'off';
      wrapper.appendChild(input);
      form.appendChild(wrapper);
    }

    enquiryForms.forEach(addHoneypot);

    fetch('/api/public-config')
      .then(response => {
        if (!response.ok) throw new Error('Could not load form configuration');
        return response.json();
      })
      .then(async config => {
        if (!config.turnstileSiteKey) return;
        if (!window.turnstile) {
          await new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
            script.async = true;
            script.defer = true;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
          });
        }

        enquiryForms.forEach(form => {
          const container = document.createElement('div');
          container.className = 'nevo-turnstile';
          const submitBtn = form.querySelector('.btn-enquiry-submit');
          form.insertBefore(container, submitBtn || null);
          form.dataset.turnstileWidgetId = window.turnstile.render(container, {
            sitekey: config.turnstileSiteKey,
            callback: token => { form.dataset.turnstileToken = token; },
            'expired-callback': () => { form.dataset.turnstileToken = ''; },
            'error-callback': () => { form.dataset.turnstileToken = ''; }
          });
        });
      })
      .catch(error => {
        console.warn('[NEVO] Form verification could not be initialized:', error);
      });

    window.openEnquiryModal = function(serviceName) {
      if (!modal) return;

      const lockedWrap = modal.querySelector('#modal-service-locked-wrap');
      const lockedText = modal.querySelector('#modal-service-display-text');
      const hiddenInput = modal.querySelector('#modal-service-input');
      const selectWrap = modal.querySelector('#modal-service-select-wrap');
      const selectEl = modal.querySelector('#modal-service-select');

      if (serviceName && serviceName.trim() !== '') {
        // AUTOMATICALLY TAKE SELECTED SERVICE - DO NOT GIVE OPTIONS
        if (lockedWrap) lockedWrap.style.display = 'block';
        if (lockedText) lockedText.textContent = serviceName;
        if (hiddenInput) {
          hiddenInput.value = serviceName;
          hiddenInput.disabled = false;
        }
        if (selectWrap) selectWrap.style.display = 'none';
        if (selectEl) selectEl.disabled = true;
      } else {
        // Fallback only if opened without a specific service
        if (lockedWrap) lockedWrap.style.display = 'none';
        if (hiddenInput) hiddenInput.disabled = true;
        if (selectWrap) {
          selectWrap.style.display = 'block';
          if (selectEl) selectEl.disabled = false;
        }
      }

      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    };

    window.selectHomeService = function(serviceName) {
      const homeLockedWrap = document.getElementById('home-service-locked-wrap');
      const homeLockedText = document.getElementById('home-service-display-text');
      const homeHiddenInput = document.getElementById('home-service-input');
      const homeSelectWrap = document.getElementById('home-service-select-wrap');
      const homeSelect = document.getElementById('home-service');

      if (serviceName && serviceName.trim() !== '') {
        if (homeLockedWrap) homeLockedWrap.style.display = 'block';
        if (homeLockedText) homeLockedText.textContent = serviceName;
        if (homeHiddenInput) {
          homeHiddenInput.value = serviceName;
          homeHiddenInput.disabled = false;
        }
        if (homeSelectWrap) homeSelectWrap.style.display = 'none';
        if (homeSelect) homeSelect.disabled = true;
      } else {
        if (homeLockedWrap) homeLockedWrap.style.display = 'none';
        if (homeHiddenInput) homeHiddenInput.disabled = true;
        if (homeSelectWrap) homeSelectWrap.style.display = 'block';
        if (homeSelect) homeSelect.disabled = false;
      }
    };

    // Check URL parameters for preselected service
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const serviceParam = urlParams.get('service');
      if (serviceParam) {
        window.selectHomeService(serviceParam);
      }
    } catch (e) {
      // Ignore URL parsing errors
    }

    window.closeEnquiryModal = function() {
      if (!modal) return;
      modal.classList.remove('active');
      document.body.style.overflow = '';
    };

    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.closeEnquiryModal();
      });
    }

    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          window.closeEnquiryModal();
        }
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
        window.closeEnquiryModal();
      }
    });

    // Wire up all .service-enquiry-btn triggers
    document.querySelectorAll('.service-enquiry-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const service = btn.getAttribute('data-service') || '';
        window.openEnquiryModal(service);
      });
    });

    // Direct Gmail Web Composer Opener
    document.querySelectorAll('.social-icon-gmail, a[href*="nevotechsolutions@gmail.com"]').forEach(el => {
      el.addEventListener('click', (e) => {
        const targetUrl = el.getAttribute('href') || '';
        if (targetUrl.startsWith('mailto:') || !targetUrl.includes('mail.google.com')) {
          e.preventDefault();
          window.open('https://mail.google.com/mail/?view=cm&fs=1&to=nevotechsolutions@gmail.com&su=Enquiry%20for%20NEVO%20TECH', '_blank', 'noopener,noreferrer');
        }
      });
    });

    // Wire up all .nevo-enquiry-form forms across all pages
    enquiryForms.forEach(form => {
      form.addEventListener('submit', (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector('.btn-enquiry-submit');
        const originalHtml = submitBtn ? submitBtn.innerHTML : 'Submit Enquiry';

        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = `
            <svg class="spin-icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" style="animation: spin 0.8s linear infinite;">
              <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-linecap="round"/>
            </svg>
            <span>Submitting Enquiry...</span>
          `;
        }

        const formData = new FormData(form);
        const fullName = formData.get('fullName') || 'there';
        const service = formData.get('service') || 'our programs';
        const email = formData.get('email') || '';
        const phone = formData.get('phone') || '';
        const institution = formData.get('institution') || '';
        const domain = formData.get('domain') || '';
        const message = formData.get('message') || '';

        if (form.dataset.turnstileWidgetId && !form.dataset.turnstileToken) {
          showToast('Please complete the verification before submitting.');
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalHtml;
          }
          return;
        }

        const payload = {
          fullName: fullName,
          email: email,
          phone: phone,
          service: service,
          institution: institution,
          domain: domain,
          message: message,
          website: formData.get('website') || '',
          captchaToken: form.dataset.turnstileToken || ''
        };

        fetch('/api/enquiries', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
        .then(async response => {
          const data = await response.json().catch(() => ({}));
          if (!response.ok || !data.success) {
            throw new Error(data.error || 'Your enquiry could not be submitted. Please try again.');
          }

          const parentCard = form.parentElement;
          const successDiv = document.createElement('div');
          successDiv.className = 'form-success-alert';
          const icon = document.createElement('div');
          icon.className = 'form-success-icon';
          icon.textContent = '✓';
          const heading = document.createElement('h4');
          heading.textContent = `Thank You, ${fullName}!`;
          const confirmation = document.createElement('p');
          confirmation.textContent = `Your enquiry for ${service} has been received. Our team will contact you at ${email}.`;
          const anotherButton = document.createElement('button');
          anotherButton.type = 'button';
          anotherButton.className = 'btn-enquiry-submit';
          anotherButton.style.cssText = 'max-width:200px;margin-top:1rem;padding:0.6rem 1.2rem;font-size:0.85rem;';
          anotherButton.textContent = 'Submit Another Enquiry';
          successDiv.append(icon, heading, confirmation, anotherButton);

          form.style.display = 'none';
          parentCard.appendChild(successDiv);
          anotherButton.addEventListener('click', () => {
            form.reset();
            form.style.display = '';
            successDiv.remove();
            form.dataset.turnstileToken = '';
            if (form.dataset.turnstileWidgetId && window.turnstile) {
              window.turnstile.reset(form.dataset.turnstileWidgetId);
            }
            if (window.closeEnquiryModal) window.closeEnquiryModal();
          });
        })
        .catch(error => {
          showToast(error.message || 'We could not submit your enquiry. Please try again.');
          if (form.dataset.turnstileWidgetId && window.turnstile) {
            window.turnstile.reset(form.dataset.turnstileWidgetId);
            form.dataset.turnstileToken = '';
          }
        })
        .finally(() => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalHtml;
          }
        });
      });
    });
  }

  // Initialize Enquiry Suite
  initEnquirySuite();

});
