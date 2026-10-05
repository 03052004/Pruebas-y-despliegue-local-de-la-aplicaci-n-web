// ==========================================
// VARIABLES
// ==========================================

const form = document.getElementById("formRegistro");
const lista = document.getElementById("listaRegistros");
const total = document.getElementById("totalRegistros");
const mensaje = document.getElementById("mensaje");

// Spinner Bootstrap
const spinner = document.getElementById("spinnerCarga");

// Campos del formulario
const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

// Mensajes de error
const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

// ==========================================
// ARREGLO DE REGISTROS
// ==========================================

let registros = [

    {
        nombre: "Pack Discotequero 2026",
        descripcion: "Música remix actualizada para DJs profesionales.",
        categoria: "Música Remix"
    },

    {
        nombre: "Librerías DJ Premium",
        descripcion: "Sonidos, efectos y herramientas para producción musical.",
        categoria: "Librerías DJ"
    },

    {
        nombre: "Eventos Especiales",
        descripcion: "Servicio musical para bodas, fiestas y eventos.",
        categoria: "Eventos"
    }

];

// ==========================================
// VALIDACIONES
// ==========================================

// Validar Nombre
function validarNombre() {

    if (nombre.value.trim().length < 3) {

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        errorNombre.textContent =
            "El nombre debe tener al menos 3 caracteres.";

        return false;

    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    errorNombre.textContent = "";

    return true;

}

// Validar Descripción
function validarDescripcion() {

    if (descripcion.value.trim().length < 10) {

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        errorDescripcion.textContent =
            "La descripción debe tener al menos 10 caracteres.";

        return false;

    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    errorDescripcion.textContent = "";

    return true;

}

// Validar Categoría
function validarCategoria() {

    if (categoria.value === "") {

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        errorCategoria.textContent =
            "Seleccione una categoría.";

        return false;

    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    errorCategoria.textContent = "";

    return true;

}

// ==========================================
// EVENTOS DE VALIDACIÓN
// ==========================================

nombre.addEventListener("input", validarNombre);

descripcion.addEventListener("input", validarDescripcion);

categoria.addEventListener("change", validarCategoria);

// ==========================================
// MOSTRAR REGISTROS
// ==========================================

function mostrarRegistros() {

    lista.innerHTML = "";

    if (registros.length === 0) {

        lista.innerHTML = `
            <div class="col-12">
                <div class="alert alert-warning text-center">
                    No existen registros disponibles.
                </div>
            </div>
        `;

    } else {

        registros.forEach((registro, indice) => {

            // Columna
            const columna = document.createElement("div");
            columna.className = "col-lg-4 col-md-6 mb-4";

            // Card
            const tarjeta = document.createElement("div");
            tarjeta.className = "card h-100 shadow";

            // Body
            const cuerpo = document.createElement("div");
            cuerpo.className = "card-body";

            // Título
            const titulo = document.createElement("h5");
            titulo.className = "card-title";
            titulo.textContent = registro.nombre;

            // Descripción
            const descripcionTexto = document.createElement("p");
            descripcionTexto.className = "card-text";
            descripcionTexto.innerHTML =
                `<strong>Descripción:</strong><br>${registro.descripcion}`;

            // Categoría
            const categoriaTexto = document.createElement("p");
            categoriaTexto.innerHTML =
                `<strong>Categoría:</strong> ${registro.categoria}`;

            // Botón eliminar
            const boton = document.createElement("button");

            boton.textContent = "Eliminar";

            boton.className = "btn btn-danger w-100";

            boton.addEventListener("click", function () {

                eliminarRegistro(indice);

            });

            // Agregar elementos

            cuerpo.appendChild(titulo);
            cuerpo.appendChild(descripcionTexto);
            cuerpo.appendChild(categoriaTexto);
            cuerpo.appendChild(boton);

            tarjeta.appendChild(cuerpo);

            columna.appendChild(tarjeta);

            lista.appendChild(columna);

        });

    }

    total.textContent = registros.length;

}

// ==========================================
// ELIMINAR REGISTRO
// ==========================================

function eliminarRegistro(indice) {

    if (confirm("¿Está seguro de eliminar este registro?")) {

        registros.splice(indice, 1);

        mensaje.innerHTML = `
            <div class="alert alert-warning">
                Registro eliminado correctamente.
            </div>
        `;

        mostrarRegistros();

    }

} 
// ==========================================
// AGREGAR REGISTRO
// ==========================================

form.addEventListener("submit", function(e){

    e.preventDefault();


    // Ejecutar validaciones

    const nombreValido = validarNombre();

    const descripcionValida = validarDescripcion();

    const categoriaValida = validarCategoria();



    if(
        !nombreValido ||
        !descripcionValida ||
        !categoriaValida
    ){

        mensaje.innerHTML = `

            <div class="alert alert-danger">

                Complete correctamente todos los campos.

            </div>

        `;

        return;

    }



    // Mostrar spinner

    spinner.classList.remove("d-none");



    // Simulación de carga

    setTimeout(function(){



        // Crear nuevo registro

        const nuevoRegistro = {

            nombre: nombre.value,

            descripcion: descripcion.value,

            categoria: categoria.value

        };



        // Guardar registro

        registros.push(nuevoRegistro);



        // Actualizar cards

        mostrarRegistros();



        // Mensaje éxito

        mensaje.innerHTML = `

            <div class="alert alert-success">

                Registro agregado correctamente.

            </div>

        `;



        // Ocultar spinner

        spinner.classList.add("d-none");



        // Limpiar formulario

        form.reset();



        // Quitar estilos de validación

        nombre.classList.remove("is-valid");

        descripcion.classList.remove("is-valid");

        categoria.classList.remove("is-valid");



    },1000);



});



// ==========================================
// CARGAR REGISTROS AL INICIAR LA PÁGINA
// ==========================================

mostrarRegistros();