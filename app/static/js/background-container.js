function calculateSquaresForScreenSize() {
  const width = window.innerWidth;
  
  if (width >= 1200) {
    return 100; // Large screens: 10x10 grid
  } else if (width >= 992) {
    return 80;  // Medium-large screens: 8x10 grid
  } else if (width >= 768) {
    return 60;  // Medium screens: 6x10 grid
  } else if (width >= 576) {
    return 40;  // Small screens: 5x8 grid
  } else {
    return 20;  // Extra small screens: 4x5 grid
  }
}

function createSquares(totalSquares, background) {
    background.innerHTML = ''; // Clear existing squares
    for (let i = 0; i < totalSquares; i++) {
        const square = document.createElement('div');
        square.classList.add('square');
        background.appendChild(square);
    }
}

document.addEventListener("DOMContentLoaded", () => {
  const background = document.querySelector(".dynamic-background");

  // Create squares based on screen size
  const totalSquares = calculateSquaresForScreenSize();
  createSquares(totalSquares, background);

  // Update squares when window is resized
  window.addEventListener('resize', () => {
    const newTotalSquares = calculateSquaresForScreenSize();
    createSquares(newTotalSquares, background);
  });

  // Change opacity of squares every 2 seconds
  setInterval(() => {
    const squares = document.querySelectorAll('.square');
    squares.forEach(square => {
        square.style.opacity = (Math.random() * 0.9 + 0.8).toFixed(2);
    });
  }, 2000);
});
