from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ProductoForm, ClienteForm, ProveedorForm, FacturaForm
from forms.usuario_form import RegistroForm, LoginForm # <--- Formularios de usuario
from conexion.conexion import obtener_conexion 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user # <--- Flask-Login
from werkzeug.security import generate_password_hash, check_password_hash # <--- Seguridad de contraseñas

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN DE FLASK-WTF Y CSRF
# ==========================================
app.config["SECRET_KEY"] = "ecuavoysmusic-clave-secreta-2026"

# ==========================================
# CONFIGURACIÓN DE LOGIN MANAGER
# ==========================================
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Por favor, inicie sesión para acceder a esta página."
login_manager.login_message_category = "warning"

# Clase de usuario requerida por Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Función para cargar el usuario desde MySQL
@login_manager.user_loader
def load_user(user_id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if usuario:
        return User(id=usuario['id'], username=usuario['username'])
    return None

# ==========================================
# DATOS GENERALES DEL SISTEMA
# ==========================================
nombre_sistema = "ECUAVOYSMUSIC"

informacion = {
    "empresa": "ECUAVOYSMUSIC",
    "descripcion": "Venta de música, librerías, paquetes remix y recursos para DJs.",
    "estado": "Activo"
}

# ==========================================
# DATOS TEMPORALES (Se mantienen igual)
# ==========================================
clientes = [{"nombre": "Cliente 1", "correo": "cliente1@gmail.com", "telefono": "0999999999"}]
proveedores = [{"nombre": "Proveedor Musical", "empresa": "Music Ecuador", "telefono": "0977777777"}]
facturas = [{"numero": "001-001-000001", "cliente": "Cliente 1", "total": 25.00}]

# ==========================================
# PÁGINA PRINCIPAL
# ==========================================
@app.route("/")
def inicio():
    return render_template("index.html", nombre_sistema=nombre_sistema, informacion=informacion)

# ==========================================
# RUTAS DE AUTENTICACIÓN (LOGIN Y REGISTRO)
# ==========================================
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
        
    form = RegistroForm()
    if form.validate_on_submit():
        # Encriptamos la contraseña antes de guardarla (obligatorio)
        hash_password = generate_password_hash(form.password.data)
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)", 
                           (form.username.data, hash_password))
            conn.commit()
            flash("Usuario registrado correctamente. Ahora puede iniciar sesión.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash("El nombre de usuario ya existe. Elija otro.", "danger")
        finally:
            cursor.close()
            conn.close()
            
    return render_template("registro.html", form=form, nombre_sistema=nombre_sistema)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
        
    form = LoginForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (form.username.data,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        # Comparamos la contraseña encriptada de la BD con la que escribió el usuario
        if usuario and check_password_hash(usuario['password_hash'], form.password.data):
            user_obj = User(id=usuario['id'], username=usuario['username'])
            login_user(user_obj)
            flash(f"Bienvenido al sistema, {usuario['username']}.", "success")
            return redirect(url_for('inicio'))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
            
    return render_template("login.html", form=form, nombre_sistema=nombre_sistema)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('login'))


# ==========================================
# MÓDULO DE PRODUCTOS (AHORA PROTEGIDO)
# ==========================================
@app.route("/productos")
@login_required
def productos_lista():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True) 
    cursor.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, c.nombre as categoria 
        FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        ORDER BY p.id DESC
    """)
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("productos.html", productos=productos, nombre_sistema=nombre_sistema)

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "INSERT INTO productos (nombre, descripcion, precio, stock, categoria_id) VALUES (%s, %s, %s, %s, %s)"
        valores = (form.nombre.data, form.descripcion.data, form.precio.data, form.stock.data, form.categoria_id.data)
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        flash("Producto registrado correctamente.", "success")
        return redirect(url_for("productos_lista"))
    return render_template("forms/producto_form.html", form=form, nombre_sistema=nombre_sistema)

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    form = ProductoForm()
    
    if form.validate_on_submit():
        sql = "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, categoria_id=%s WHERE id=%s"
        valores = (form.nombre.data, form.descripcion.data, form.precio.data, form.stock.data, form.categoria_id.data, id)
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        flash("Producto actualizado correctamente.", "success")
        return redirect(url_for("productos_lista"))
    else:
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
        if producto:
            form.nombre.data = producto['nombre']
            form.descripcion.data = producto['descripcion']
            form.precio.data = producto['precio']
            form.stock.data = producto['stock']
            form.categoria_id.data = producto['categoria_id']
        cursor.close()
        conn.close()
        
    return render_template("forms/producto_form.html", form=form, nombre_sistema=nombre_sistema, editando=True)

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    sql = "DELETE FROM productos WHERE id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Producto eliminado correctamente.", "danger")
    return redirect(url_for("productos_lista"))


# ==========================================
# RUTAS DE CLIENTES, PROVEEDORES Y FACTURAS (PROTEGIDAS)
# ==========================================
@app.route("/clientes")
@login_required
def clientes_lista():
    return render_template("clientes.html", clientes=clientes, nombre_sistema=nombre_sistema)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        clientes.append({"nombre": form.nombre.data, "correo": form.correo.data, "telefono": form.telefono.data})
        flash("Cliente registrado correctamente.", "success")
        return redirect(url_for("clientes_lista"))
    return render_template("forms/cliente_form.html", form=form, nombre_sistema=nombre_sistema)

@app.route("/proveedores")
@login_required
def proveedores_lista():
    return render_template("proveedores.html", proveedores=proveedores, nombre_sistema=nombre_sistema)

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        proveedores.append({"nombre": form.nombre.data, "empresa": form.empresa.data, "telefono": form.telefono.data})
        flash("Proveedor registrado correctamente.", "success")
        return redirect(url_for("proveedores_lista"))
    return render_template("forms/proveedor_form.html", form=form, nombre_sistema=nombre_sistema)

@app.route("/facturacion")
@login_required
def facturacion_lista():
    return render_template("facturacion.html", facturas=facturas, nombre_sistema=nombre_sistema)

@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def nueva_factura():
    form = FacturaForm()
    if form.validate_on_submit():
        facturas.append({"numero": form.numero.data, "cliente": form.cliente.data, "total": form.total.data})
        flash("Factura registrada correctamente.", "success")
        return redirect(url_for("facturacion_lista"))
    return render_template("forms/factura_form.html", form=form, nombre_sistema=nombre_sistema)

# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)