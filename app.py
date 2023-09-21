from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_session import Session
from datetime import timedelta
from functools import wraps
from database import init_app
from models.Clientes import db, Cliente
from models.VentasEncabezados import db, VentaEncabezado

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Configurar la sesión para que caduque después de 2 horas de inactividad
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

Session(app)


# Configura la conexión a la base de datos desde database.py
init_app(app)


# Datos de ejemplo: usuarios y permisos
usuarios = {
    'victor.lm': {
        'password': 'victor.lm',
        'permisos': {
            'tarjetas': ['crear', 'consultar'],
            'clientes': ['crear', 'consultar'],
            'cobros': ['crear', 'consultar']
        }
    },
    'adrian.ad': {
        'password': 'adrian.ad',
        'permisos': {
            'tarjetas': ['crear', 'consultar'],
            'clientes': ['crear', 'consultar'],
            'cobros': ['crear', 'consultar']
        }
    },    
    'fray.lm': {
        'password': 'fray.lm',
        'permisos': {
            'tarjetas': ['crear', 'consultar'],
            'clientes': ['crear'],
            'cobros': ['crear', 'consultar']
        }
    },
    'parra.pa': {
        'password': 'parra.pa',
        'permisos': {
            'tarjetas': [],
            'clientes': ['consultar'],
            'cobros': ['crear', 'consultar']
        }
    },
  
    'auxiliar.au': {
        'password': 'auxiliar123',
        'permisos': {}
    }
}


# Decorador para requerir inicio de sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Página de inicio
@app.route('/')
def inicio():
    # Verificar si el usuario ya está autenticado
    if 'usuario' in session:
        return redirect(url_for('menu', usuario=session['usuario']))
    
    return render_template('bienvenida.html')

# Página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verificar si el usuario ya está autenticado
    if 'usuario' in session:
        return redirect(url_for('menu', usuario=session['usuario']))

    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        if usuario in usuarios and usuarios[usuario]['password'] == password:
            session['usuario'] = usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('menu', usuario=usuario))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Cierra la sesión del usuario
    flash('Has cerrado sesión', 'success')  # Opcional: muestra un mensaje de éxito
    return redirect(url_for('login'))  # Redirige al usuario a la página de inicio de sesión


# Página principal con menú
@app.route('/menu/<usuario>')
@login_required
def menu(usuario):
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."

    permisos = usuarios.get(usuario, {}).get('permisos', {})
    return render_template('menu.html', permisos=permisos, usuario=usuario)

# ... Resto de las rutas para las secciones como tarjetas, clientes, cobros, etc.

# Submenús para tarjetas y clientes
@app.route('/menu/tarjetas/<usuario>')
@login_required
def tarjetas(usuario):
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."
    permisosTarjetas = usuarios.get(usuario, {}).get('permisos', {}).get('tarjetas', [])
    permisos = usuarios.get(usuario, {}).get('permisos', {})
    if 'tarjetas' in permisosTarjetas:
        return render_template('tarjetas.html', permisos=permisos, usuario=usuario)
    else:
        return "No tienes permisos para ver esta página."

@app.route('/menu/clientes/<usuario>')
@login_required
def clientes(usuario):
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."
    permisosClientes = usuarios.get(usuario, {}).get('permisos', {}).get('clientes', [])
    permisos = usuarios.get(usuario, {}).get('permisos', {})
    if 'clientes' in permisosClientes:
        return render_template('clientes.html', permisos=permisos, usuario=usuario)
    else:
        return "No tienes permisos para ver esta página."

@app.route('/menu/cobros/<usuario>')
@login_required
def cobros(usuario):
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."
    permisosCobros = usuarios.get(usuario, {}).get('permisos', {}).get('cobros', [])
    permisos = usuarios.get(usuario, {}).get('permisos', {})
    if 'cobros' in permisosCobros:
        return render_template('cobros.html', permisos=permisos, usuario=usuario)
    else:
        return "No tienes permisos para ver esta página."

# Submenús para crear y consultar tarjetas/clientes
@app.route('/menu/tarjetas/crear/<usuario>')
@login_required
def crear_tarjeta(usuario):
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."
    permisosCrear = usuarios.get(usuario, {}).get('permisos', {}).get('tarjetas', [])
    permisos = usuarios.get(usuario, {}).get('permisos', {})
    if 'crear' in permisosCrear:
        return render_template('crear_tarjeta.html', permisos=permisos, usuario=usuario)
    else:
        return "No tienes permisos para ver esta página."

@app.route('/menu/tarjetas/consultar/<usuario>')
@login_required
def consultar_tarjeta(usuario):
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."
    permisosConsultar = usuarios.get(usuario, {}).get('permisos', {}).get('tarjetas', [])
    permisos = usuarios.get(usuario, {}).get('permisos', {})
    if 'consultar' in permisosConsultar:
        return render_template('consultar_tarjeta.html', permisos=permisos, usuario=usuario)
    else:
        return "No tienes permisos para ver esta página."

@app.route('/menu/clientes/crear/<usuario>')
@login_required
def crear_cliente(usuario):
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."
    permisosCrear = usuarios.get(usuario, {}).get('permisos', {}).get('clientes', [])
    permisos = usuarios.get(usuario, {}).get('permisos', {})
    if 'crear' in permisosCrear:
        return render_template('crear_cliente.html', permisos=permisos, usuario=usuario)
    else:
        return "No tienes permisos para ver esta página."



# @app.route('/menu/clientes/consultar/<usuario>')
# @login_required
# def consultar_cliente(usuario):
#     if usuario != session['usuario']:
#         return "Acceso denegado: No puedes acceder a esta página."
#     permisosConsultar = usuarios.get(usuario, {}).get('permisos', {}).get('clientes', [])
#     permisos = usuarios.get(usuario, {}).get('permisos', {})
#     if 'consultar' in permisosConsultar:
#         return render_template('consultar_cliente.html', permisos=permisos, usuario=usuario)
#     else:
#         return "No tienes permisos para ver esta página."


@app.route('/menu/clientes/consultar/<usuario>')
@login_required
def consultar_cliente(usuario):
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."
    permisosConsultar = usuarios.get(usuario, {}).get('permisos', {}).get('clientes', [])
    permisos = usuarios.get(usuario, {}).get('permisos', {})
    if 'consultar' in permisosConsultar:
        # Realiza la consulta a la base de datos para obtener los clientes
        clientes = Cliente.query.all()  # Esto supone que tienes un modelo Cliente

        # Renderiza la plantilla y pasa los clientes como argumento
        return render_template('consultar_cliente.html', permisos=permisos, usuario=usuario, clientes=clientes)
    else:
        return "No tienes permisos para ver esta página."




@app.route('/menu/cobros/crear/<usuario>')
@login_required
def crear_cobro(usuario):
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."
    permisosCrear = usuarios.get(usuario, {}).get('permisos', {}).get('cobros', [])
    permisos = usuarios.get(usuario, {}).get('permisos', {})
    if 'crear' in permisosCrear:
        return render_template('crear_cobro.html', permisos=permisos, usuario=usuario)
    else:
        return "No tienes permisos para ver esta página."

@app.route('/menu/cobros/consultar/<usuario>', methods=['GET', 'POST'])
@login_required
def consultar_cobro(usuario):
    connection = None  # <-- Inicialización de la variable connection
    resultados = None
    if usuario != session['usuario']:
        return "Acceso denegado: No puedes acceder a esta página."
    permisosConsultar = usuarios.get(usuario, {}).get('permisos', {}).get('cobros', [])
    permisos = usuarios.get(usuario, {}).get('permisos', {})
    
    # if request.method == 'POST':
    #     id_venta = request.form['id_venta']
    #     connection = conectar_db()

    # if connection:
    #     resultados = ejecutar_consultas(connection, id_venta)
    #     connection.close()

    if 'consultar' in permisosConsultar:
        return render_template('consultar_cobro.html', permisos=permisos, usuario=usuario)
    else:
        return "No tienes permisos para ver esta página."


if __name__ == '__main__':
   app.run(debug=True, port=8000)
