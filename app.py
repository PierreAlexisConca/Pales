from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_conn
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_secreta")

# ================================
# 🌐 RUTAS PRINCIPALES
# ================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/coleccion')
def coleccion():
    category = request.args.get('category')
    return render_template('categories.html', selected_category=category)

@app.route('/ofertas')
def ofertas():
    category = request.args.get('category')
    return render_template('ofertas.html', selected_category=category)

@app.route('/cuenta')
def cuenta():
    return render_template('mi-cuenta.html')

@app.route('/carrito')
def carrito():
    return render_template('cart.html')

@app.route('/registro')
def registro():
    return render_template('register.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/confirmacion-compra')
def confirmacion_compra():
    return render_template('purchase_confirmation.html')

@app.route('/estado-pedido')
def estado_pedido():
    return render_template('estado-pedido.html')

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

# ================================
# 💬 FORMULARIO DE CONTACTO
# ================================

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            con = get_conn()
            cur = con.cursor()
            cur.execute("""
                INSERT INTO contact_messages (name, email, message)
                VALUES (%s, %s, %s)
            """, (name, email, message))
            con.commit()
            flash("✅ Tu mensaje ha sido enviado correctamente.", "success")
        except Exception as e:
            print("ERROR CONTACTO:", e)
            flash("❌ Hubo un problema al enviar el mensaje.", "error")
        finally:
            cur.close()
            con.close()

        return redirect(url_for('contacto'))

    return render_template('contacto.html')

# ================================
# 👤 USUARIOS (REGISTRO / LOGIN / LOGOUT)
# ================================

# ✅ Registrar usuario
@app.route('/register', methods=['POST'])
def register():
    nombre = request.form['name']
    email = request.form['email']
    password = request.form['password']

    password_hash = generate_password_hash(password)

    try:
        con = get_conn()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO usuarios (nombre, email, password)
            VALUES (%s, %s, %s)
        """, (nombre, email, password_hash))

        con.commit()
        flash("✅ Cuenta creada con éxito. Ahora inicia sesión.", "success")

    except Exception as e:
        print("ERROR REGISTRO:", e)
        flash("❌ Este correo ya está registrado o ocurrió un error.", "error")
    finally:
        cur.close()
        con.close()

    return redirect(url_for('cuenta'))

# ✅ Iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        con = get_conn()
        cur = con.cursor()
        cur.execute("SELECT id, password FROM usuarios WHERE email = %s", (email,))
        usuario = cur.fetchone()
    except Exception as e:
        print("ERROR LOGIN:", e)
        flash("❌ Error interno al iniciar sesión.", "error")
        return redirect(url_for('cuenta'))
    finally:
        cur.close()
        con.close()

    if usuario and check_password_hash(usuario[1], password):
        session['usuario_id'] = usuario[0]
        flash("✅ Sesión iniciada correctamente.", "success")
        return redirect(url_for('index'))
    else:
        flash("❌ Correo o contraseña incorrectos.", "error")
        return redirect(url_for('cuenta'))

# ✅ Cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash("👋 Sesión cerrada.", "info")
    return redirect(url_for('index'))

# ================================
# 🚀 INICIO DE LA APLICACIÓN
# ================================
if __name__ == '__main__':
    app.run(debug=True)
