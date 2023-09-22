import pandas as pd
import numpy as np
import mysql.connector


import tkinter as tk
from tkinter import messagebox

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

# Conversion de columna 'TIMESTAMP' al formato de fecha de pandas (datatime64)
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='%Y-%m-%d %H:%M:%S')
df["TIMESTAMP"]=df["TIMESTAMP"] + pd.Timedelta(hours=6)
df=df[df["TIMESTAMP"].dt.month==int(mounth_)]

start_date = df['TIMESTAMP'].iloc[0]
end_date = df['TIMESTAMP'].iloc[-1]


#Conversion de tempartura a Grados Kelvin
df['CRPTemp_Avg']=df['CRPTemp_Avg']+273.15
df['UVTEMP_Avg']=df['UVTEMP_Avg']+273.15
df["DEW_POINT_Avg"] = df["DEW_POINT_Avg"]+273.15

#Agregamos columnas al DataFrame
dif_GH_CALC_GLOBAL=df["GH_CALC_Avg"] - df["GLOBAL_Avg"]
porcent_GH_CALC_GLOBAL=(abs(df["GLOBAL_Avg"]-df["GH_CALC_Avg"])/df["GH_CALC_Avg"])
sum_SW = df["DIFFUSE_Avg"] + df["DIRECT_Avg"]*np.cos(np.radians(df["ZenDeg"]))

df["dif_GH_CALC_GLOBAL"]=dif_GH_CALC_GLOBAL
df["porcent_GH_CALC_GLOBAL"]=porcent_GH_CALC_GLOBAL
df["sum_SW"]=sum_SW
df["porcent_2"] = 0.01*sum_SW

df["empy"]=""
df["null_int"]=-999
df["null_float1"]=-99.9
df["null_float2"]=-99.99

# Guardamos todas las culumnas del DataFrame
columns = list(df.columns)

# Columnas provicionales para trabajar
avg_list = [x.replace("_Avg","") for x in columns if x.endswith("Avg")]
std_list = [x.replace("_Std","") for x in columns if x.endswith("Std")]
min_list = [x.replace("_Min","") for x in columns if x.endswith("Min")]
max_list = [x.replace("_Max","") for x in columns if x.endswith("Max")]

common_list = list(set(avg_list) & set(std_list) & set(min_list) & set(max_list))

aux = [elemento + "_" + str(i) for elemento in common_list for i in ["Avg","Std","Min","Max"]]
unique_columns=columns.copy()

for i in aux:
    unique_columns.remove(i)

unique_columns.remove("TIMESTAMP")
unique_columns.remove("RECORD")




#Columnas del DataFrame que pertenecen a cada categoría.
basic_parameters = ["GLOBAL","DIRECT","DIFFUSE","GH_CALC_Avg"]
stadistic = ["dif_GH_CALC_GLOBAL","porcent_GH_CALC_GLOBAL","sum_SW"]
shortwave_balance = ["GLOBAL","UPWARD_SW"]
longwave_balance = ["DOWNWARD","UPWARD_LW","DWIRTEMP","UWIRTEMP","CRPTemp_Avg"]
meteorology = ["CRPTemp_Avg","RELATIVE_HUMIDITY_Avg","PRESSURE_Avg","DEW_POINT_Avg"]
ultraviolet = ["UVB","UVTEMP_Avg","UVSIGNAL_Avg"]


categories = [basic_parameters,shortwave_balance,longwave_balance,meteorology,ultraviolet,stadistic]

#others = merged_columns.copy()
others = columns 

for j in list(df.columns[-8:]):
    others.remove(j)

categories.append(others)


names_categories=["Parametros Basicos","Balance de onda corta","Balance de onda larga","Meteorologia","Ultravioleta","Dispersion","Otros"]

climatic_categories = dict(zip(names_categories,categories))