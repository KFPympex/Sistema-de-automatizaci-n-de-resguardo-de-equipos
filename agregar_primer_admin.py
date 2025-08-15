import mysql.connector
import bcrypt

# Conexión a la base de datos
mydb = mysql.connector.connect(
    host='localhost',
    port='tu_puerto',
    user='tu_usuario',
    password='tu_contraseña',
    database='db_resguardos'
)

mycursor = mydb.cursor()

# Datos del nuevo administrador
nombre = 'tus_nombres'
primer_apellido = 'tu_primer_apellido'
segundo_apellido = 'tu_segundo_apellido'
nombre_admin = 'tu_nombe_de_admin'
contrasena = 'tu_contraseña'

# Hashear la contraseña
contrasena_hasheada = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

# Query SQL para insertar el nuevo admin
sql = """
INSERT INTO admin (
    nombre,
    primer_apellido_admin,
    segundo_apellido_admin,
    nombre_admin,
    contrasena
) VALUES (%s, %s, %s, %s, %s)
"""

# Ejecutar la consulta
valores = (nombre, primer_apellido, segundo_apellido, nombre_admin, contrasena_hasheada)
mycursor.execute(sql, valores)

# Confirmar cambios
mydb.commit()

print("Nuevo administrador agregado exitosamente.")
