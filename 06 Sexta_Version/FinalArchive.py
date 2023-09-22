import pandas as pd
import gzip
from functions.columns import *


####################################################
#             Algunas funciones utiles             #
####################################################

def new_df(dff,columns_1,columns_2):
    """
    Crea un nuevo DataFrame combinando columnas de `dff` según reglas específicas.

    Parámetros:
    - dff: DataFrame. El DataFrame original.
    - columns_1: Lista. Lista de nombres de columnas para el primer subconjunto de columnas.
    - columns_2: Lista. Lista de nombres de columnas para el segundo subconjunto de columnas.

    Retorna:
    - DataFrame. Un nuevo DataFrame combinado según las reglas especificadas.

    Descripción:
    Esta función toma un DataFrame `dff` y dos listas de nombres de columnas `columns_1` y `columns_2`.
    A partir de estas listas, se crean dos DataFrames `dff1` y `dff2` que contienen las columnas
    correspondientes de `dff`. Luego, se asignan nuevos índices a cada DataFrame y se renombran las columnas
    con números enteros en ambos DataFrames.

    Posteriormente, se realiza una concatenación vertical de los DataFrames `dff1` y `dff2` en el orden
    especificado por los índices. Finalmente, se ordena el DataFrame resultante según los índices y se retorna.
    """
    
    dff1=dff[columns_1]
    dff2=dff[columns_2]

    index1=[x for x in np.arange(0,len(dff1)*2,2)]
    index2=[x for x in np.arange(1,len(dff2)*2,2)]

    dff1 = dff1.set_index(pd.Index(index1))
    dff2 = dff2.set_index(pd.Index(index2))

    dff1.columns=[x for x in range(0,len(dff1.columns))]
    dff2.columns=[x for x in range(0,len(dff2.columns))]
    dff3 = pd.concat([dff1, dff2], ignore_index=False, axis=0)
    dff3 = dff3.sort_index()
    return dff3


#Funcion para comprimir archivo
def CompressFile(name_file, name_file_compress):
    print("Comprimiendo archivo")
    with open(name_file, 'rb') as file:
        with gzip.open(name_file_compress, 'wb') as file_compress:
            file_compress.writelines(file)
    
    print("Archivo comprimido exitosamente: ", name_file_compress)

#Funcion para corregir los espacios
def correct_spaces(string,condition,column,df):
    if len(string)<=condition:
        miss_spaces=abs(len(string)-condition)
        string = " "*miss_spaces+string
    
    if len(string)>condition:
        if column in rounds["round_float1"]:
            print("\nError en columna ", column)
            print("Valor original: ", string)
            print("Valor reemplazdo: ", "-99.9\n")

            string="-99.9"
        elif column in rounds["round_float2"]:
            print("\nError en columna ", column)
            print("Valor original: ", string)
            print("Valor reemplazdo: ", "-99.99\n")

            string="-99.99"
        elif column in rounds["round_int"]:
            print("\nError en columna ", column)
            print("Valor original: ", string)
            print("Valor reemplazdo: ", "-999\n")

            string="-999"

    return string


def create_string(dff,option):
    
    dff=dff.astype(str)

    #Cuando se redondea y pasamos a Strgin Python pasa de 19.10 a 19.1, para evitar eso ocupamos:
    for k in dff.columns:
        if k in rounds["round_float2"]:
            dff[k]=dff[k].astype(float).map("{:.2f}".format)

    #Renombramos columnas 
    original_columns=list(dff.columns)
    dff.columns=list(range(0,len(dff.columns)))

    #Corregimos espacios
    for j in dff.columns:
        dff[j]=dff[j].apply(lambda x: correct_spaces(x, spaces[option][j],original_columns[j],dff))

    #Creamos la cadena
    cadena = dff.to_string(col_space=0,header=False,index=False) + "\n"
    return cadena

def round_df(df,rounds):
    #Se redondean segun opciones y se reemplazan los datos null
    for i in rounds["round_int"]:
        df[i]=df[i].fillna(-999)
        df[i]=df[i].round(0)
        df[i]=df[i].astype(int)

    for i in rounds["round_float1"]:
        df[i]=df[i].fillna(-99.9)
        df[i]=df[i].round(1)

    for i in rounds["round_float2"]:
        df[i]=df[i].fillna(-99.99)
        df[i]=df[i].round(2)

    return df


####################################################
#  Opciones para redondear segun especificaciones  #
####################################################

rounds=dict(round_int=["GLOBAL_Avg","GLOBAL_Min","GLOBAL_Max","DIRECT_Avg","DIRECT_Min","DIRECT_Max","DIFFUSE_Avg",
                       "DIFFUSE_Min","DIFFUSE_Max","DOWNWARD_Avg","DOWNWARD_Min","DOWNWARD_Max","UPWARD_SW_Avg",
                       "UPWARD_SW_Min","UPWARD_SW_Max","UPWARD_LW_Avg","UPWARD_LW_Min","UPWARD_LW_Max","PRESSURE_Avg",
                       "UPWARD_SW_Avg","UPWARD_SW_Min","UPWARD_SW_Max","UPWARD_LW_Avg","UPWARD_LW_Min","UPWARD_LW_Max",],
           round_float1=["GLOBAL_Std","DIRECT_Std","DIFFUSE_Std","DOWNWARD_Std","AIR_TEMPERATURE_Avg",
                         "RELATIVE_HUMIDITY_Avg","UPWARD_SW_Std","UPWARD_LW_Std","UVB_Avg","UVB_Std","UVB_Min","UVB_Max",
                        "DWTERMO_Avg","UWTERMO_Avg"],
           round_float2=["DWIRTEMPC_Avg","UWIRTEMPC_Avg"])


#########################################
#  Opciones para categorias de archivo  #
#########################################

options=dict(C0100=["day","minute","GLOBAL_Avg","GLOBAL_Std","GLOBAL_Min","GLOBAL_Max","DIRECT_Avg","DIRECT_Std",
                    "DIRECT_Min","DIRECT_Max","DIFFUSE_Avg","DIFFUSE_Std","DIFFUSE_Min","DIFFUSE_Max","DOWNWARD_Avg",
                    "DOWNWARD_Std","DOWNWARD_Min","DOWNWARD_Max","AIR_TEMPERATURE_Avg","RELATIVE_HUMIDITY_Avg",
                    "PRESSURE_Avg","empy"],
             #C0200=["day","minute","GLOBAL_Avg","GLOBAL_Std","GLOBAL_Min","GLOBAL_Max"],
             C0300=["day","minute","UPWARD_SW_Avg","UPWARD_SW_Std","UPWARD_SW_Min","UPWARD_SW_Max","UPWARD_LW_Avg",
                    "UPWARD_LW_Std","UPWARD_LW_Min","UPWARD_LW_Max","null_int","null_float1","null_int", "null_int"],
             C0500=["day","minute","null_float1", "UVB_Avg","UVB_Std","UVB_Min","UVB_Max","empy"], 
             C4000=["day","minute","null_float2","null_float2","null_float2","DWIRTEMPC_Avg","DWTERMO_Avg"
                    ,"null_float2","null_float2","null_float2","UWIRTEMPC_Avg","UWTERMO_Avg"])

#########################################
#  Opciones para Espacios entre datos   #
#########################################

spaces=dict(C0100=[3,4,6,5,4,4,6,5,4,4,8,5,4],
            C0300=[3,4,6,5,4,4,6,5,4,4,6,5,4,4],
            C0500=[3,4,5,5,5,5,5,5,5,5,5,5,5,5],
            C4000=[3,4,6,6,6,6,6,7,6,6,6,6])

###########################################
#  Se agregan columnas de minutos y dias  #
###########################################

day = [x.day for x in df["TIMESTAMP"]]
minute = [x.hour*60+x.minute for x in df["TIMESTAMP"]]
month = [x.month for x in df["TIMESTAMP"]]


df_aux=df.copy()
df_aux.insert(0,"minute",minute)
df_aux.insert(0,"day",day)

df_aux["day"] = df_aux["day"].astype(str)
df_aux['day'] = df_aux['day'].apply(lambda x: ' ' + x)

df_aux['UVB_Avg'] = df_aux['UVB_Avg'].replace(-999, -99.9)
df_aux['UVB_Min'] = df_aux['UVB_Min'].replace(-999, -99.9)
df_aux['UVB_Max'] = df_aux['UVB_Max'].replace(-999, -99.9)

def CreateFinalArchive(df,path_origin=r"..\00 bsrn\fijo.dat",path_destination="Final_Example.dat"):

    with open(path_origin) as archive:
        lines = archive.readlines()   
    
    if len(str(mounth_))==1:
        lines[1]=" 83" + "  " + mounth_ + " 20" + base_sql[-2:] + "  1" + "\n"
    elif len(str(mounth_))==2:
        lines[1]=" 83" + " " + mounth_ + " 20" + base_sql[-2:] + "  1" +"\n"

    lines.append("\n")

    print("Comenzando proceso")

    df=round_df(df,rounds)

    for i in options.keys():
        
        lines.append("*"+i+"\n")
        
        dff=df[list(options[i])]
        
        if i=="C0100":
        
            columns_1=["day","minute","GLOBAL_Avg","GLOBAL_Std","GLOBAL_Min","GLOBAL_Max","DIRECT_Avg","DIRECT_Std","DIRECT_Min",
                        "DIRECT_Max","empy","empy","empy"]

            columns_2=["empy","empy","DIFFUSE_Avg","DIFFUSE_Std","DIFFUSE_Min","DIFFUSE_Max","DOWNWARD_Avg","DOWNWARD_Std",
                       "DOWNWARD_Min","DOWNWARD_Max","AIR_TEMPERATURE_Avg","RELATIVE_HUMIDITY_Avg","PRESSURE_Avg"]
            
            dff = new_df(dff,columns_1,columns_2)

            cadena=create_string(dff,i)
            cadena=cadena.replace("                    ","")

        elif i=="C0300":
            cadena=create_string(dff,i)
        
        elif i=="C0500":
            
            columns_1=["day","minute","null_float1","null_float1","null_float1","null_float1","null_float1","null_float1","null_float1",
                "null_float1","empy","empy","empy","empy"]

            columns_2=["empy","empy","UVB_Avg","UVB_Std","UVB_Min","UVB_Max","null_float1","null_float1","null_float1","null_float1",
            "null_float1","null_float1","null_float1","null_float1"]
            
            dff = new_df(dff,columns_1,columns_2)

            cadena=create_string(dff,i)
            cadena=cadena.replace("                        ","")

        elif i=="C4000":
            cadena=create_string(dff,i)
            
        lines.append(cadena)

        print(i + " Terminado")

    with open(path_destination, 'w',newline='') as archive:
        archive.writelines(lines)  

    print("Archivo final terminado: ", path_destination)

if len(mounth_)==1:
    mes_ = "0" + str(mounth_)

else:
    mes_=str(mounth_)

path_dest = "sel" + str(mes_) + base_sql[-2:] + ".dat"

CreateFinalArchive(df_aux,path_destination=path_dest)

CompressFile(path_dest,path_dest+".gz")
