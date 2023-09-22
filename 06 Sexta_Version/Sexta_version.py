from dash import dcc, html

from functions.callbacks import *

################################################
#  Creacion de objetos Iniciales para mostrar  #
################################################

# Grafica a Mostrar
dropdown_categorias = dcc.Dropdown(names_categories,
                    'Dispersion',
                    id="possible_categories",
                    style={'width': '400px'},
                    multi=False,
                    searchable=True
                    )

# Rango de Fechas
rang_date = dcc.DatePickerRange(id='my_date_picker_range',
                                min_date_allowed=df['TIMESTAMP'].iloc[0],
                                max_date_allowed=df['TIMESTAMP'].iloc[-1],
                                initial_visible_month=df['TIMESTAMP'].iloc[0],
                                start_date=df['TIMESTAMP'].iloc[0],
                                end_date=df['TIMESTAMP'].iloc[1440]) 

horas = [str(i).zfill(2) for i in range(24)]
minutos = [str(i).zfill(2) for i in range(60)]

range_hours_initial=dcc.Dropdown(
        id='hour-initial-dropdown',
        options=[{'label': h, 'value': h} for h in horas],
        value=horas[0]
    )
range_minutes_initial=dcc.Dropdown(
        id='minute-initial-dropdown',
        options=[{'label': m, 'value': m} for m in minutos],
        value=minutos[0]
    )

range_hours_final=dcc.Dropdown(
        id='hour-final-dropdown',
        options=[{'label': h, 'value': h} for h in horas],
        value=horas[23]
    )
range_minutes_final=dcc.Dropdown(
        id='minute-final-dropdown',
        options=[{'label': m, 'value': m} for m in minutos],
        value=minutos[59]
    )

button_errors = html.Button('Generar Report_Errors', id='button_errors', n_clicks=0)

dropdown_graph_values = dcc.Dropdown(id='graph_values')


##################################################
#               Pantalla principal               #
##################################################
      
app.layout = html.Div([
    html.H1("BSRN IGEF"),

    html.Hr(),

    html.Div([
        html.H3("Seleccione la categoría"),
        dropdown_categorias],
        style={'display': 'flex', 
               'flex-direction': 'column',
               'height': '100px',
               'text-align': 'center',
               'align-items': 'center'}
        ),

    html.Hr(),
    html.H3("Seleccione las gráficas a mostrar"),
    html.Div(
        dropdown_graph_values,
        id="possible_plots"),

    html.Hr(),

    html.Div(
        [
            html.H3("Seleccione el período de fechas deseado"),
            rang_date
        ],
        style={'display': 'flex', 
               'flex-direction': 'column',
               'height': '100px',
               'text-align': 'center',
               'align-items': 'center'}),

    html.Br(),
    html.H3("Seleccione el período de tiempo deseado"),
    html.Div([
                html.Div([html.H4("Seleccione la hora inicial"),
                          range_hours_initial,
                          range_minutes_initial], style={'margin': '20px'}),
                html.Div([html.H4("Seleccione la hora final"),
                          range_hours_final,
                          range_minutes_final], style={'margin': '20px'})
            ],
            style={'display': 'flex', 
                   'flex-direction': 'row',
                   'text-align': 'center',
                   'align-items': 'center',
                   'justify-content': 'center'}),

    html.Hr(),
    dcc.Graph(id='indicator_graphic'),

    html.Hr(),

    html.Div(button_errors),

    html.H3("Datos totales"),
    html.Div(id='table_container'),

    html.Hr(),
    html.H2("Generar archivo final"),
    html.Button('Generar archivo', id='my-button', n_clicks=0),
    html.Div(id='generate_final_archive')

], style={"text-align": 'center',
          'align-items': 'center'})


#####################################################################
#                             Llamadas                              #
#####################################################################

    
if __name__ == '__main__':
    app.run_server(debug=True)
    