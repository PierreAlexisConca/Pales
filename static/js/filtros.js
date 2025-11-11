// Variables para guardar los filtros seleccionados
let tallaSeleccionada = null;
let colorSeleccionado = null;

// Seleccionamos todos los botones de talla
const tallaButtons = document.querySelectorAll("[data-filter-talla]");
// Seleccionamos todos los botones de color
const colorButtons = document.querySelectorAll("[data-filter-color]");
// Seleccionamos todos los productos
const products = document.querySelectorAll(".producto");

// Evento para los botones de talla
tallaButtons.forEach(boton => {
    boton.addEventListener("click", () => {
        tallaSeleccionada = boton.getAttribute("data-filter-talla");

        // Activar clase seleccionada
        tallaButtons.forEach(btn => btn.classList.remove("selected"));
        boton.classList.add("selected");

        filtrarProductos();
    });
});

// Evento para los botones de color
colorButtons.forEach(boton => {
    boton.addEventListener("click", () => {
        colorSeleccionado = boton.getAttribute("data-filter-color");

        // Activar clase seleccionada
        colorButtons.forEach(btn => btn.classList.remove("selected"));
        boton.classList.add("selected");

        filtrarProductos();
    });
});

// Función para filtrar productos
function filtrarProductos() {
    products.forEach(product => {
        const productSize = product.getAttribute("data-size");
        const productColor = product.getAttribute("data-color");

        // Validación
        const tallaCoincide = !tallaSeleccionada || productSize.includes(tallaSeleccionada);
        const colorCoincide = !colorSeleccionado || productColor === colorSeleccionado;

        if (tallaCoincide && colorCoincide) {
            product.style.display = "block";
        } else {
            product.style.display = "none";
        }
    });
}
