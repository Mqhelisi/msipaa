from dash import html, dash_table, Input, Output, State, callback
from dash import dcc
import dash_bootstrap_components as dbc
from datetime import date
import pandas as pd
from models import read_workers

# df = pd.DataFrame(read_workers())

labelDict = {   

    'margin':'0 10px 10px',
    'text-shadow':'1px 1px 1px blue',
    'font-size':'25px'
    }

def sideBySide(cmp1,cmp2):
    return(
        dbc.Row(
                            [
                                dbc.Col(
                                cmp1,
                                width={"offset":2}
                            ),
                            dbc.Col(
                                cmp2
                            ),
                              dbc.Col(
                                width={"size":1}
                            ),
                            ]
                        )
    )

modal2 = html.Div(
    [
        # dbc.Button("Open modal", id="open", n_clicks=0),
        dbc.Modal(
            
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody(
                    html.Div(
                        children=[

    sideBySide(
        html.Label("Job Details: "),
        html.Label(id="job-modal-deet",style=labelDict)
    ),
    sideBySide(
        html.Label("Job Date: "),
        html.Label(id="job-modal-date",style=labelDict)
    ),
    sideBySide(
        html.Label("Capacity: "),
        html.Label(id="job-modal-cap",style=labelDict)
    ),
    sideBySide(
        html.Label("Labour Requirement: "),
        html.Label(id="job-modal-labor",style=labelDict)
    ),
    html.Hr(),
    html.H1('Select Workers For the Job', style={'textAlign':'center'}),

   dash_table.DataTable(
       id='tbl2',
    page_current=0,
    page_size=8,
    page_action='native',
row_selectable="multi",
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
    ),
    html.Br(),
    html.Div(
        children=[
        dbc.Button("Accept Work Config",id='accpt'),        
        ],
style={"flex-direction":"row","display":"flex","justify-content":"center"}
    ),

    html.Label(id="job-resp")

                    ]
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close2", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            size="xl",
            id="modal2",
            is_open=False,
        ),
    ]
)


page2 = html.Div(
    style={"margin-left":"3%","margin-right":"2%"},
    children=[
    html.H1('add New Job', style={'textAlign':'center'}),
    html.Div(
        children=[
    sideBySide(html.Label("Job Details",style=labelDict),
               dbc.Input(id="job-input", placeholder="Description of Job", type="text")),
            html.Br(),
    sideBySide(html.Label("Start Date",style=labelDict),
               dcc.DatePickerSingle(month_format='MMM Do, YY',
                                    placeholder='MMM Do, YY',
                                    id="job-datepick",
            
                                    date=date.today())),
            html.Br(),
    sideBySide(html.Label("Capacity",style=labelDict),
               dbc.Input(id="cap-input", placeholder="Please Put Integer Value", type="number")),
            html.Br(),
    html.Div(
        children=[
    dbc.Button("Sort Workers", id="workerr"),
        ],
        style={"flex-direction":"row","display":"flex","justify-content":"center"}
    ),
    modal2
        ]
    )

    ]
)