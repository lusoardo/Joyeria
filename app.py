from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="joyeria"
)
cursor = conexion.cursor()

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/CargarClientes')
def clientes():
    query = "SELECT * FROM Cliente"
    cursor.execute(query)
    CargarCliente = cursor.fetchall()
    return render_template('CargarClientes.html', Clientes=CargarCliente)

@app.route('/agregar_clientes', methods=['POST'])
def agregar_clientes():
    nombre = request.form.get('Nombre')
    apellido = request.form.get('Apellido')
    telefono = request.form.get('Telefono')

    query = 'INSERT INTO Cliente (Nombre, Apellido, Telefono) VALUES (%s, %s, %s)'
    cursor.execute(query, (nombre, apellido, telefono))
    conexion.commit()
    return redirect(url_for('clientes'))

@app.route('/modificar_cliente', methods=['POST'])
def modificar_cliente():
    ID_Cliente = request.form.get('ID')
    nombre = request.form.get('Nombre')
    apellido = request.form.get('Apellido')
    telefono = request.form.get('Telefono')

    query = 'UPDATE Cliente SET Nombre = %s, Apellido = %s, Telefono = %s WHERE ID_Cliente = %s'
    cursor.execute(query, (nombre, apellido, telefono, ID_Cliente))
    conexion.commit()
    return redirect(url_for('clientes'))

@app.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    ID_Cliente = request.form.get('ID')

    query = 'DELETE FROM Cliente WHERE ID_Cliente = %s'
    cursor.execute(query, (ID_Cliente,))
    conexion.commit()
    return redirect(url_for('clientes'))

# Página para productos
@app.route('/productos')
def productos():
    query = "SELECT * FROM Producto"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('productos.html', productos=productos)

@app.route('/agregar_productos', methods=['POST'])
def agregar_productos():
    tamaño = request.form.get('tamaño')
    material = request.form.get('material')
    precio = request.form.get('precio')
    query = 'INSERT INTO Producto (tamaño, material, precio) VALUES (%s, %s, %s)'
    cursor.execute(query, (tamaño, material, precio))
    conexion.commit()
    return redirect(url_for('productos'))

@app.route('/modificar_productos', methods=['POST'])
def modificar_productos():
    # Obtengo el ID que se puso en el formulario
    ID_producto = request.form.get('ID')

    # Obtengo los campos modificados
    tamaño = request.form.get('tamaño')
    material = request.form.get('material')
    precio = request.form.get('precio')

    # Ejecuto el SQL para modificar
    query = 'UPDATE Producto SET tamaño = %s, material = %s, precio = %s WHERE ID_Producto = %s'
    cursor.execute(query, (tamaño, material, precio, ID_producto))
    conexion.commit()
    return redirect(url_for('productos'))

@app.route('/eliminar_productos', methods=['POST'])
def eliminar_productos():
    # Obtengo el ID que se puso en el formulario
    ID_producto = request.form.get('ID')

    # Hago la query en la base de datos para eliminar el producto de ese ID
    query = 'DELETE FROM Producto WHERE ID_Producto = %s'
    cursor.execute(query, (ID_producto,))
    conexion.commit()
    return redirect(url_for('productos'))


# Página para cargar pedidos
@app.route('/pedidos')
def pedidos():
    # Obtener los clientes y productos existentes
    cursor.execute("SELECT * FROM Cliente")
    clientes = cursor.fetchall()

    cursor.execute("SELECT * FROM Producto")
    productos = cursor.fetchall()

    # Obtener los pedidos existentes y sus detalles
    query = """
    SELECT Pedido.ID_Pedido, Pedido.Fecha, Cliente.Nombre, Cliente.Apellido
    FROM Pedido
    INNER JOIN Cliente ON Pedido.ID_Cliente = Cliente.ID_Cliente
    """
    cursor.execute(query)
    pedidos = cursor.fetchall()

    # Incluir los productos en cada pedido
    pedidos_detalles = []
    for pedido in pedidos:
        cursor.execute("""
        SELECT Producto.Tamaño, Producto.Oro, Producto.Plata, Tiene.Cantidad, Producto.Precio
        FROM Tiene
        INNER JOIN Producto ON Tiene.ID_Producto = Producto.ID_Producto
        WHERE Tiene.ID_Pedido = %s
        """, (pedido[0],))
        productos_pedido = cursor.fetchall()
        pedidos_detalles.append((pedido[0], pedido[1], pedido[2], pedido[3], productos_pedido))

    return render_template('CargarPedidos.html', Clientes=clientes, Productos=productos, Pedidos=pedidos_detalles)

@app.route('/agregar_pedido', methods=['POST'])
def agregar_pedido():
    cliente_id = request.form['ClienteID']
    producto_ids = request.form.getlist('ProductoID[]')
    cantidades = request.form.getlist('Cantidad[]')
    fecha = request.form['Fecha']
    factura = request.form['Factura']

    total_precio = 0
    for producto_id, cantidad in zip(producto_ids, cantidades):
        cantidad = int(cantidad)
        cursor.execute("SELECT Precio FROM Producto WHERE ID_Producto = %s", (producto_id,))
        precio_producto = cursor.fetchone()[0]
        total_precio += cantidad * precio_producto

    # Insert the order into the database
    cursor.execute("INSERT INTO Pedido (ID_Cliente, Fecha, Factura) VALUES (%s, %s, %s)", 
                   (cliente_id, fecha, factura))
    pedido_id = cursor.lastrowid
    for producto_id, cantidad in zip(producto_ids, cantidades):
        cursor.execute("INSERT INTO Tiene (ID_Pedido, ID_Producto, Cantidad) VALUES (%s, %s, %s)",
                       (pedido_id, producto_id, cantidad))
    
    conexion.commit()

    return redirect(url_for('pedidos'))

@app.route('/eliminar_pedido', methods=['POST'])
def eliminar_pedido():
    pedido_id = request.form['ID_Pedido']
    try:
        pedido_id = int(pedido_id)  # Asegurarse de que es un entero
        cursor.execute("DELETE FROM Pedido WHERE ID_Pedido = %s", (pedido_id,))
        conexion.commit()
    except ValueError:
        return "ID de pedido inválido.", 400
    return redirect(url_for('pedidos'))

@app.route('/modificar_pedido/<int:pedido_id>')
def modificar_pedido(pedido_id):
    cursor.execute("SELECT * FROM Pedido WHERE ID_Pedido = %s", (pedido_id,))
    pedido = cursor.fetchone()
    return render_template('modificar_pedido.html', pedido=pedido)

@app.route('/guardar_modificacion_pedido', methods=['POST'])
def guardar_modificacion_pedido():
    pedido_id = request.form['pedido_id']
    fecha = request.form['Fecha']
    factura = request.form['Factura']
    try:
        pedido_id = int(pedido_id)  # Verificar que pedido_id sea entero
        cursor.execute("UPDATE Pedido SET Fecha = %s, Factura = %s WHERE ID_Pedido = %s", (fecha, factura, pedido_id))
        conexion.commit()
    except ValueError:
        return "ID de pedido inválido.", 400
    return redirect(url_for('pedidos'))

@app.route('/volver')
def volver():
    return render_template('index.html')