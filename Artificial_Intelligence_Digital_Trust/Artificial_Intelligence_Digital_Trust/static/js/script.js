/* =========================================================
   AI & DIGITAL TRUST — MAIN SCRIPT
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- 1. LOADER ---------- */
  const loader = document.getElementById('loader');
  window.addEventListener('load', () => {
    setTimeout(() => loader && loader.classList.add('hidden'), 400);
  });
  // Fallback in case 'load' already fired
  setTimeout(() => loader && loader.classList.add('hidden'), 1500);

  /* ---------- 2. THEME TOGGLE (dark/light) ---------- */
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = themeToggle ? themeToggle.querySelector('i') : null;
  const savedTheme = getCookie('theme');

  function applyTheme(theme) {
    if (theme === 'light') {
      document.body.classList.add('light-theme');
      if (themeIcon) { themeIcon.classList.remove('fa-moon'); themeIcon.classList.add('fa-sun'); }
    } else {
      document.body.classList.remove('light-theme');
      if (themeIcon) { themeIcon.classList.remove('fa-sun'); themeIcon.classList.add('fa-moon'); }
    }
  }
  applyTheme(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isLight = document.body.classList.contains('light-theme');
      const next = isLight ? 'dark' : 'light';
      applyTheme(next);
      setCookie('theme', next, 365);
    });
  }

  function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${d.toUTCString()};path=/`;
  }
  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  /* ---------- 3. NAVBAR SCROLL + MOBILE TOGGLE ---------- */
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 20);
    toggleScrollTopBtn();
  });

  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
  }

  // Mobile dropdown toggle
  document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', (e) => {
      if (window.innerWidth <= 860) {
        e.preventDefault();
        toggle.closest('.dropdown').classList.toggle('open');
      }
    });
  });

  /* ---------- 4. SCROLL REVEAL ANIMATIONS ---------- */
  const revealEls = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealEls.forEach(el => observer.observe(el));

  /* ---------- 5. ANIMATED COUNTERS ---------- */
  const counters = document.querySelectorAll('.counter');
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => counterObserver.observe(c));

  function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-target'), 10) || 0;
    let current = 0;
    const duration = 1200;
    const stepTime = Math.max(Math.floor(duration / Math.max(target, 1)), 20);
    const step = () => {
      current += 1;
      el.textContent = current;
      if (current < target) setTimeout(step, stepTime);
      else el.textContent = target;
    };
    if (target > 0) step(); else el.textContent = '0';
  }

  /* ---------- 6. SCROLL TO TOP ---------- */
  const scrollTopBtn = document.getElementById('scrollTopBtn');
  function toggleScrollTopBtn() {
    if (!scrollTopBtn) return;
    scrollTopBtn.classList.toggle('visible', window.scrollY > 400);
  }
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ---------- 7. ACCORDION (About AI / Digital Trust FAQ) ---------- */
  document.querySelectorAll('.accordion-item').forEach(item => {
    const header = item.querySelector('.accordion-header');
    if (!header) return;
    header.addEventListener('click', () => {
      const alreadyActive = item.classList.contains('active');
      item.closest('.accordion').querySelectorAll('.accordion-item').forEach(i => i.classList.remove('active'));
      if (!alreadyActive) item.classList.add('active');
    });
  });

  /* ---------- 8. SITE SEARCH (client-side, static page index) ---------- */
  const searchIndex = [
    { title: 'Home', url: window.SITE_URLS?.index || '/' },
    { title: 'About AI', url: window.SITE_URLS?.about || '/about' },
    { title: 'Machine Learning', url: (window.SITE_URLS?.about || '/about') + '#ml' },
    { title: 'Deep Learning', url: (window.SITE_URLS?.about || '/about') + '#dl' },
    { title: 'Generative AI', url: (window.SITE_URLS?.about || '/about') + '#genai' },
    { title: 'Digital Trust', url: window.SITE_URLS?.digital_trust || '/digital-trust' },
    { title: 'Data Privacy', url: window.SITE_URLS?.digital_trust || '/digital-trust' },
    { title: 'Cyber Security', url: window.SITE_URLS?.digital_trust || '/digital-trust' },
    { title: 'AI Challenges', url: window.SITE_URLS?.challenges || '/challenges' },
    { title: 'Deepfakes', url: window.SITE_URLS?.challenges || '/challenges' },
    { title: 'Bias in AI', url: window.SITE_URLS?.challenges || '/challenges' },
    { title: 'AI Solutions', url: window.SITE_URLS?.solutions || '/solutions' },
    { title: 'Explainable AI', url: window.SITE_URLS?.solutions || '/solutions' },
    { title: 'AI Quiz', url: window.SITE_URLS?.quiz || '/quiz' },
    { title: 'Trust Calculator', url: window.SITE_URLS?.calculator || '/calculator' },
    { title: 'AI News', url: window.SITE_URLS?.news || '/news' },
    { title: 'About Us', url: window.SITE_URLS?.about_us || '/about-us' },
    { title: 'Contact', url: window.SITE_URLS?.contact || '/contact' },
  ];

  const searchInput = document.getElementById('siteSearch');
  const searchResults = document.getElementById('searchResults');
  if (searchInput && searchResults) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim().toLowerCase();
      if (!q) { searchResults.classList.remove('active'); searchResults.innerHTML = ''; return; }
      const matches = searchIndex.filter(item => item.title.toLowerCase().includes(q));
      searchResults.innerHTML = matches.length
        ? matches.map(m => `<a href="${m.url}">${m.title}</a>`).join('')
        : '<div class="no-result">No results found</div>';
      searchResults.classList.add('active');
    });
    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.classList.remove('active');
      }
    });
  }

});
