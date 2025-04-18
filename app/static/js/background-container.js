

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

  // Crear los cuadrados dinámicamente
  createSquares(100, background);

  // Cambiar la opacidad de los cuadrados cada 0.8 segundos
  setInterval(() => {
    const squares = document.querySelectorAll('.square');
    squares.forEach(square => {
        square.style.opacity = (Math.random() * 0.9 + 0.8).toFixed(2);
    });
}, 2000);
});
