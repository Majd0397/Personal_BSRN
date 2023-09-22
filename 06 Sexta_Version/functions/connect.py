import mysql.connector
import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Crear una nueva ventana
window_ = tk.Tk()
window_.title("Ingresar datos")

# Crear etiquetas y campos de entrada
label_user = tk.Label(window_, text="Usuario:")
label_user.pack()
field_user = tk.Entry(window_)
field_user.pack()

label_password = tk.Label(window_, text="Contraseña:")
label_password.pack()
field_password = tk.Entry(window_, show="*")
field_password.pack()

label_base = tk.Label(window_, text="Ingresa la base de datos deseada:")
label_base.pack()
field_base = tk.Entry(window_)
field_base.pack()

label_table = tk.Label(window_, text="Ingresa la tabla deseada:")
label_table.pack()
field_table = tk.Entry(window_)
field_table.pack()

label_month = tk.Label(window_, text="Ingresa el mes:")
label_month.pack()
fiedl_month = tk.Entry(window_)
fiedl_month.pack()

# Función para manejar el botón "Aceptar"
def aceptar():
    global user
    global password
    global mounth_
    global base_sql
    global tabla_sql
        
    user = field_user.get()
    password = field_password.get()
    mounth_ = fiedl_month.get()
    base_sql = field_base.get()
    tabla_sql = field_table.get()


    window_.destroy()
# Crear el botón "Aceptar"
button_accept = tk.Button(window_, text="Aceptar", command=aceptar)
button_accept.pack()

window_.mainloop()

# Importamos el DataFrame
# Configuración de la conexión
config = {
    'user': user,
    'password': password,
    'host': '132.248.182.174',
    'database': base_sql,
    'port':3306
}


# Conexión al servidor MySQL

try:
    conn = mysql.connector.connect(**config)
    if mounth_!="1":
        query = "SELECT * FROM " + tabla_sql + " where (month(timestamp)=" + mounth_ + " or (month(timestamp)=" + str(int(mounth_)-1) + " and hour(timestamp)>17)" + ")" +" and year(timestamp)=" + str(int(base_sql[-4:]))
    elif mounth_=="1":
        query = "select * from " + tabla_sql + " where (month(timestamp)=12 and year(timestamp)="  + str(int(base_sql[-4:])-1) + " and day(timestamp)=31 and hour(timestamp)>17) or (month(timestamp)=1 and year(timestamp)=" +  str(int(base_sql[-4:])) + ")"
    df = pd.read_sql(query, conn)
    conn.close()
    print('Conexión exitosa')
    
except mysql.connector.Error as err:
    print('Error de conexión a la base de datos:', err)