document.addEventListener('DOMContentLoaded', () => {
  // Mapeamento de atalhos (corrige links que não têm seção correspondente)
  const shortcutMap = {
    'explorar': 'tradutor'
  };

  // função utilitária de scroll
  function scrollToId(targetId) {
    const mapped = shortcutMap[targetId] || targetId;
    const target = document.getElementById(mapped);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return true;
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return false;
    }
  }

  // ===== substituído: listeners diretos mais confiáveis =====
  // Captura todos os links âncora no documento
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const href = anchor.getAttribute('href');
      if (!href || href === '#') return;
      e.preventDefault();
      const targetId = href.slice(1);
      scrollToId(targetId);
    });
  });

  // Garante que botões específicos com id também acionem (caso não sejam anchors)
  ['btn-sobre', 'btn-tradutor', 'cta-tradutor'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('click', (e) => {
      const href = el.getAttribute && el.getAttribute('href');
      const dataTarget = el.dataset && el.dataset.target;
      const targetRef = href || dataTarget;
      if (!targetRef || !targetRef.startsWith('#')) return;
      e.preventDefault();
      scrollToId(targetRef.slice(1));
    });
  });
  // ==========================================================

  // Destacar link ativo conforme a seção visível
  const navLinks = Array.from(document.querySelectorAll('.main-nav .nav-link'));
  const sections = Array.from(document.querySelectorAll('section[id]'));

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const id = entry.target.id;
        const link = navLinks.find(a => {
          const href = a.getAttribute('href') || '';
          const target = href.startsWith('#') ? href.slice(1) : '';
          return target === id || (target === 'explorar' && id === 'tradutor');
        });
        if (link) {
          if (entry.isIntersecting) {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
          }
        }
      });
    }, { root: null, rootMargin: '0px', threshold: 0.45 });

    sections.forEach(s => io.observe(s));
  } else {
    window.addEventListener('scroll', () => {
      let current = sections[0];
      for (const s of sections) {
        const rect = s.getBoundingClientRect();
        if (rect.top <= window.innerHeight * 0.3) current = s;
      }
      navLinks.forEach(l => l.classList.remove('active'));
      const active = navLinks.find(a => {
        const href = a.getAttribute('href') || '';
        const target = href.startsWith('#') ? href.slice(1) : '';
        return target === current.id || (target === 'explorar' && current.id === 'tradutor');
      });
      if (active) active.classList.add('active');
    }, { passive: true });
  }

  // Botão de idioma (troca visual e atributo lang do documento)
  const langBtn = document.getElementById('language');
  const langFloating = document.querySelector('.lang-floating');
  if (langBtn) {
    langBtn.addEventListener('click', () => {
      const html = document.documentElement;
      if (html.lang === 'en') {
        html.lang = 'pt-BR';
        langBtn.textContent = 'Português - Brasil';
        if (langFloating) langFloating.textContent = 'Português - Brasil';
        langBtn.setAttribute('aria-label', 'Mudar idioma para Inglês');
      } else {
        html.lang = 'en';
        langBtn.textContent = 'English - US';
        if (langFloating) langFloating.textContent = 'English - US';
        langBtn.setAttribute('aria-label', 'Change language to Portuguese');
      }
    });
  }
});