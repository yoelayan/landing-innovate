// Navbar scroll behavior
document.addEventListener('DOMContentLoaded', function() {
  var mainNav = document.getElementById('mainNav');
  
  // Function to handle scroll events
  function handleScroll() {
    if (window.scrollY > 100) {
      mainNav.classList.add('navbar-scrolled');
    } else {
      mainNav.classList.remove('navbar-scrolled');
    }
  }
  
  // Add scroll event listener
  window.addEventListener('scroll', handleScroll);
  
  // Initial check in case the page loads scrolled
  handleScroll();
  
  // Smooth scroll for navbar links
  document.querySelectorAll('#mainNav a.nav-link, #mainNav a.contact-btn').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.startsWith('#')) {
        e.preventDefault();
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          const headerOffset = 80; // Adjust offset for navbar height
          const elementPosition = targetElement.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
          
          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
          
          // Close mobile menu if open
          const navbarToggler = document.querySelector('.navbar-toggler');
          const navbarCollapse = document.querySelector('.navbar-collapse');
          if (navbarCollapse.classList.contains('show')) {
            navbarToggler.click();
          }
        }
      }
    });
  });
  
  // Inicializar Swiper para los logos de clientes
  initClientsSwiper();
});

// Inicialización del swiper de clientes
function initClientsSwiper() {
  if (document.querySelector('.clients-swiper')) {
    new Swiper('.clients-swiper', {
      slidesPerView: 2,
      spaceBetween: 10,
      loop: true,
      autoplay: {
        delay: 2500,
        disableOnInteraction: false,
      },
      pagination: {
        el: '.clients-pagination',
        clickable: true,
      },
      breakpoints: {
        // when window width is >= 576px
        576: {
          slidesPerView: 3,
          spaceBetween: 20
        },
        // when window width is >= 768px
        768: {
          slidesPerView: 4,
          spaceBetween: 30
        },
        // when window width is >= 992px
        992: {
          slidesPerView: 5,
          spaceBetween: 40
        }
      }
    });
  }
}

// Efecto de confetti explosivo al hacer clic en el contenedor del logo
document.addEventListener('DOMContentLoaded', () => {
  const logoEl = document.querySelector(".logo");
  if (logoEl) {
    logoEl.addEventListener("click", (event) => {
      const rect = logoEl.getBoundingClientRect();
      const originX = ((rect.left + rect.right) / 2) / window.innerWidth;
      const originY = ((rect.top + rect.bottom) / 2) / window.innerHeight;
      
      confetti({
        particleCount: 100,
        startVelocity: 55,
        spread: 360,
        origin: { x: originX, y: originY },
        colors: ['#bb0000', '#ffffff', '#2d2742', '#f9c74f', '#90be6d']
      });
    });
  }
}); 