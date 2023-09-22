from functions.columns import *
from dash import dash_table

def create_table(selections,start_date,end_date,highlight_date=None):

    """
    Crea una tabla Dash DataTable a partir de un DataFrame de Pandas.

    Args:
        selections (list o str):        
            Lista de columnas a mostrar en la tabla. 
            Tamzbién se puede proporcionar una sola columna como string.
        start_date (str):               
            Fecha de inicio del intervalo de tiempo a considerar en formato "YYYY-MM-DD".
        end_date (str):                 
            Fecha de fin del intervalo de tiempo a considerar en formato "YYYY-MM-DD".
        highlight_date (str, opcional): 
            Fecha en formato "YYYY-MM-DD" que se desea resaltar en la tabla. 
            Por defecto, no se resalta ninguna fecha.

    Returns:
        dash_table.DataTable: 
            Una tabla Dash DataTable con los datos correspondientes al intervalo de tiempo y las columnas seleccionadas.
    """

    columns=["TIMESTAMP"]

    initial_index = df[df['TIMESTAMP'] == start_date].index
    final_index = df[df['TIMESTAMP'] == end_date].index
    dff=df[initial_index[0]:final_index[0]]

    #Filtros para angulo cenital menor a 90 y mayor a cero
    hour_filter = (dff["ZenDeg"]>=0) & (dff["ZenDeg"]<=90)
    filtered_dff = dff.loc[hour_filter]

    if type(selections) != list:
            selections=[selections]

    for selection in selections:
        if selection in common_list:
            for i in ["_Avg","_Std","_Min","_Max"]:
                columns.append(selection + i)
        elif selection in unique_columns:
            columns.append(selection)


    table = dash_table.DataTable(
        id='table_dates',
        columns=[{"name": i, "id": i} for i in columns],
        data=filtered_dff.to_dict("rows"),
        page_size=60,
        fixed_rows={'headers': True},
        style_data={'whiteSpace': 'normal','height': 'auto','lineHeight': '20px'},
        style_table={'minWidth': '100%','height': '500px', 'overflowY': 'auto'},
        style_cell={'minWidth': '50px', 'width': '50px', 'maxWidth': '50px','textAlign': 'center'},
        export_format='xlsx',
        export_headers='display',
        editable=True,
        style_data_conditional=[],        
        )
    
    if highlight_date!=None:
        highlight_date = filtered_dff[filtered_dff['TIMESTAMP'] == highlight_date].index
        highlight_date=str(filtered_dff['TIMESTAMP'][highlight_date[0]])
        highlight_date = highlight_date.replace(" ","T")
        table .style_data_conditional.append({'if': {'filter_query': '{{TIMESTAMP}} = {}'.format(highlight_date)},
                                'backgroundColor': '#FF4136',
                                'color': 'white'})

    return table 
