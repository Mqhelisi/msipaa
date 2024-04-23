from dash import html, dash_table, Input, Output, State, callback
from dash import dcc
import dash_bootstrap_components as dbc
from datetime import date
import pandas as pd
from models import Work,Worker,Leave,read_workers,read_works

# df = pd.DataFrame(read_works())

labelDict = {   

    'margin':'0 10px 10px',
    'text-shadow':'1px 1px 1px blue',
    'font-size':'25px'
    }

modal = html.Div(
    [
        # dbc.Button("Open modal", id="open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody(
                    html.Div(
                        children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                html.Label("Description: ",style=labelDict)
                            ),
                            dbc.Col(
                                html.Label(id="name-label")
                            ),
                            ]
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                html.Label("Capacity: ",style=labelDict)
                            ),
                            dbc.Col(
                                html.Label(id="sex-label")
                            ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                html.Label("Status: ",style=labelDict)
                            ),
                            dbc.Col(
                                html.Label(id="age-label")
                            ),
                            ]
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                html.Label("Workers: ",style=labelDict)
                            ),
                            dbc.Col(
                                html.Label(id="ticket-label")
                            ),
                            ]
                        ),

                        
                    ]
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)


page1 = html.Div(children=[
    html.H1('Check All Jobs', style={'textAlign':'center'}),
    modal,
    # search bar
    html.Div(
        children=[
            html.Label("Search in Date Range",style=labelDict),
dcc.DatePickerRange(
        id='works-date-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2017, 9, 19),
        start_date=date.today(),
        end_date=date.today(),
        initial_visible_month=date(2017, 8, 5),
        style={'margin':'0 10px 20px',}
    ),
    dbc.Button("Search Everything", id="searcher"),
        ],
        style={"flex-direction":"row","display":"flex","justify-content":"center"}
    ),

    html.Br(),
    
    dcc.Loading(
            id="loading-1",
            type="default",
            children=[

            
    html.Div(

        children=[


    dash_table.DataTable(
        
        id='tbl',
                                  page_current=0,
    page_size=8,
    page_action='custom',

    sort_action='custom',
    sort_mode='single',
    sort_by=[],
    style_cell={"whiteSpace": "pre-line"},
    
    style_data={
        'color': 'black',
        'backgroundColor': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],
    
    )
        ],
        style={"margin-left":"3%","margin-right":"2%"}
    ),
  ]
    ),
    # dbc.Alert(id="tbl_out")
])
