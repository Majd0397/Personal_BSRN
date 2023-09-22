import json
from dash import Dash, dcc, ctx
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime

from functions.grafics import make_graphic
from functions.table import create_table
from functions.columns import climatic_categories,mounth_,base_sql,names_categories,df
from functions.finalarchive import CreateFinalArchive,CompressFile,df_aux

app = Dash(__name__,suppress_callback_exceptions=True)
app.title = "BSRN"

#Funcion auxiliar para manipular fechas
def conver_dates(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return datetime.strptime(date_str, "%Y-%m-%d")

#LLamada para obtener las posibles graficas de acuerdo a la categoria seleccionada
@app.callback(
    [Output("possible_plots", "children"),
    Output("possible_plots", "style")],
    Input("possible_categories", "value")
)
def select_graphs(value):
    """
    Actualiza el contenido del componente de Dash "possible_plots" con un elemento 
    dcc.Dropdown que contiene las opciones de gráficos correspondientes a la categoría 
    seleccionada en el componente "possible_categories".

    Args:
        value (str): 
            La categoría seleccionada en el componente "possible_categories".

    Returns:
        values_dropdown (dcc.Dropdown): 
            Componente de Dash que contiene las opciones de gráficos correspondientes a la categoría seleccionada.

    """
    opt_values = climatic_categories[value]
    #Se seleccionan los valores iniciales seleccionados
    if value=="Otros":
        initial = [opt_values[0]]
    elif value=="Dispersion":
        initial = [opt_values[-2]]
    else:
        initial = opt_values

    len_options = len(opt_values)
    #Creamos el estilo del DIV
    update_style = {'display': 'flex', 'flex-direction': 'column',"height":'50px',"text-align": "center","align-items": "center"}

    if len_options>=5:
        len_options=7
        #Modificamos el largo del DIV
        update_style = {'display': 'flex', 'flex-direction': 'column',"height":'300px',"text-align": "center","align-items": "center"}

    values_dropdown = dcc.Checklist(id="graph_values",
                                    options=opt_values,
                                    value=initial,
                                    labelStyle={"display": "flex", "align-items": "center"},
                                    style={"maxWidth": "1300px", "columnCount":len_options}
                                    )
    
    return values_dropdown,update_style

    

#Indicador para grafica
@app.callback([Output('indicator_graphic', 'figure'),
               Output('hour-initial-dropdown', 'disabled'),
               Output('minute-initial-dropdown', 'disabled'),
               Output('hour-final-dropdown', 'disabled'),
               Output('minute-final-dropdown', 'disabled')],
              Input("possible_categories", "value"),
              Input('graph_values', 'value'),
              Input('my_date_picker_range', 'start_date'),
              Input('my_date_picker_range', 'end_date'),
              Input("hour-initial-dropdown","value"),
              Input("minute-initial-dropdown","value"),
              Input("hour-final-dropdown","value"),
              Input("minute-final-dropdown","value"),
              Input("button_errors","n_clicks"))
def update_time_range_slider(categorie,
                             selected_values,
                             start_date,
                             end_date,
                             hour_initial,minute_initial,
                             hour_final,minute_final,
                             state_button):
    """
    Actualiza el gráfico del indicador en la aplicación Dash.

    Args:
        categorie (str):
            Categoria seleccionada.
        selected_values (list): 
            Valores seleccionados en el componente 'graph_values'.
        start_date (str): 
            Fecha de inicio seleccionada en el componente 'my_date_picker_range' en formato 'YYYY-MM-DD'.
        end_date (str): 
            Fecha de fin seleccionada en el componente 'my_date_picker_range' en formato 'YYYY-MM-DD'.

    Returns:
        fig (go.Figure):
            Objeto que contiene el gráfico del indicador actualizado.
    """

    figure_width = 650

    #Verificamos la diferencia de dias entre las fechas seleccionadas
    start_=conver_dates(start_date)
    end_=conver_dates(end_date)
    dif_days = end_-start_
    dif_days=dif_days.days
    
    if dif_days>=2:
        hour_initial = 0
        minute_initial = 0
        hour_final = 23
        minute_final=59
    start_date = start_ + pd.Timedelta(hours=int(hour_initial))+pd.Timedelta(minutes=int(minute_initial))
    end_date = end_ - pd.Timedelta(hours=(23-int(hour_final)))-pd.Timedelta(minutes=(59-int(minute_final)))
    print(start_date.date())
    fig,dff_errors = make_graphic(categorie,selected_values,start_date,end_date)

    if state_button != 0:
        dff_errors=dff_errors[["TIMESTAMP",
                               "porcent_GH_CALC_GLOBAL",
                               "GLOBAL_Avg",
                               "GLOBAL_Std",
                               "GLOBAL_Min",
                               "GLOBAL_Max",
                               "DIRECT_Avg",
                               "DIRECT_Std",
                               "DIRECT_Min",
                               "DIRECT_Max",
                               'DIFFUSE_Avg',
                               'DIFFUSE_Std',
                               'DIFFUSE_Min',
                               'DIFFUSE_Max',
                               'AIR_TEMPERATURE_Avg',
                               'RELATIVE_HUMIDITY_Avg',
                               'PRESSURE_Avg',
                               'UPWARD_SW_Avg',
                               'UPWARD_SW_Std',
                               'UPWARD_SW_Min',
                               'UPWARD_SW_Max',
                               'DOWNWARD_Avg',
                               'DOWNWARD_Std',
                               'DOWNWARD_Min',
                               'DOWNWARD_Max',
                               'DWIRTEMP_Avg',
                               'DWIRTEMP_Std',
                               'DWIRTEMP_Min',
                               'DWIRTEMP_Max',
                               'DWSIGNAL_Avg',
                               'DWIRTEMPC_Avg',
                               'DWTERMO_Avg',
                               'UPWARD_LW_Avg',
                               'UPWARD_LW_Std',
                               'UPWARD_LW_Min',
                               'UPWARD_LW_Max',
                               'UWIRTEMP_Avg',
                               'UWIRTEMP_Std',
                               'UWIRTEMP_Min',
                               'UWIRTEMP_Max',
                               'UWSIGNAL_Avg',
                               'UWIRTEMPC_Avg',
                               'UWTERMO_Avg',
                               'UVB_Avg',
                               'UVB_Std',
                               'UVB_Min',
                               'UVB_Max']]
        dff_errors.to_csv(f"E_{start_date.date()}_{hour_initial}{minute_initial}_{hour_final}{minute_final}.csv", index=False)
    
    fig.update_layout(margin={'l': 50, 'b': 50, 't': 50, 'r': 50}, 
                        hovermode='x',
                        clickmode='event+select',
                        autosize=False,
                        width=int(figure_width *(16/9)),
                        height=figure_width )
    if dif_days>=2:
        return fig,True,True,True,True
    else:
        return fig,False,False,False,False


#LLamada para mostrar tabla
@app.callback(Output('table_container', 'children'),
              Input('graph_values', 'value'),
              Input('my_date_picker_range', 'start_date'),
              Input('my_date_picker_range', 'end_date'),
              Input('indicator_graphic', 'clickData'))
def update_table(y_axis_column_name, start_date, end_date, click_data):

    """
    Actualiza la tabla de datos en la aplicación Dash.

    Args:
        y_axis_column_name (str): 
            Nombre de la columna del eje Y seleccionado en el componente 'graph_values'.
        start_date (str): 
            Fecha de inicio seleccionada en el componente 'my_date_picker_range' en formato 'YYYY-MM-DD'.
        end_date (str): 
            Fecha de fin seleccionada en el componente 'my_date_picker_range' en formato 'YYYY-MM-DD'.
        time_range (List[int]): 
            Rango de tiempo seleccionado en el componente 'time_range_slider'.
        click_data (dict): 
            Datos seleccionados en el gráfico 'indicator_graphic'.

    Returns:
        dbc.Table:
            Tabla de datos actualizada.
    """
        
    days = pd.to_datetime(end_date) - pd.to_datetime(start_date)
    days = days.days

    if click_data != None:
        a = json.dumps(click_data, indent=2)
        diccionario = json.loads(a)
        click_data = diccionario["points"][0]["x"]

    if days == 1:
        return create_table(y_axis_column_name, start_date, end_date, highlight_date=click_data)
    else:
        return create_table(y_axis_column_name, start_date, end_date, highlight_date=click_data)
    

#Llamada para generar archivo Final
@app.callback(Output("generate_final_archive","children"),
        Input('my-button', 'n_clicks'))
def update_output(n_clicks):
    if n_clicks!=0:
        if len(mounth_)==1:
            mes_ = "0" + str(mounth_)

        else:
            mes_=str(mounth_)

        path_dest = "sel" + str(mes_) + base_sql[-2:] + ".dat"

        CreateFinalArchive(df_aux,path_destination=path_dest)

        CompressFile(path_dest,path_dest+".gz")