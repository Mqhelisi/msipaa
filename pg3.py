from dash import html, dash_table, Input, Output, State, callback
from dash import dcc
import dash_bootstrap_components as dbc
from datetime import date, timedelta
import pandas as pd
from models import read_workers, read_leaves

df = pd.DataFrame(read_workers())
df2 = pd.DataFrame(read_leaves())

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
modal3 = html.Div(
    [
        # dbc.Button("Open modal", id="open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody(
                    html.Div(
                        children=[

       sideBySide(
        html.Label("Leave Type: "),
        html.Label(id="leave-modal-type")
    ),
    sideBySide(
        html.Label("Leave Start Date: "),
        html.Label(id="leave-modal-strt")
    ),
    sideBySide(
        html.Label("Leave End Date: "),
        html.Label(id="leave-modal-end")
    ),
    sideBySide(
        html.Label("Worker Applying: "),
        html.Label(id="leave-modal-wrkr")
    ),
    sideBySide(
        html.Label("Leave Days Deducted: "),
        html.Label(id="leave-modal-deduct")
    ),
html.Div(
        children=[
    dbc.Button("Confirm Leave Add", id="leav-upd",color='secondary'),
        ],
        style={"flex-direction":"row","display":"flex","justify-content":"center"}
    ),
                    ]
                    )
                ),
                dbc.ModalFooter([
                    dbc.Button(
                        "Close", id="close3", className="ms-auto", n_clicks=0
                    ),
                    html.Label(id='leave-resp',style=labelDict)
                    ]
                ),
            ],
            id="modal3",
            is_open=False,
            backdrop='static',
            # style={'background-color':'#9E829C'}

        ),
    ]
)


page3 = html.Div(
    style={"margin-left":"3%","margin-right":"2%"},
    children=[
        html.Hr(),
    html.H1('Add Leave Day', style={'textAlign':'center'}),
    html.Div(
        children=[
    sideBySide(html.Label("Select Leave Type"),
               dcc.Dropdown(['Occasaional', 'Sympathetic', 'Sick'], 'Occasaional', id='leave-dropdown'),
            ),
            html.Br(),
    sideBySide(html.Label("Dates"),
               dcc.DatePickerRange(
        id='leave-date-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2050, 9, 19),
        start_date=date.today()+timedelta(1),
        initial_visible_month=date.today()+timedelta(1),
        style={'margin':'0 10px 20px',}
    )
               ),
               html.Br(),
               sideBySide(html.Label("Select Worker applying"),
               dcc.Dropdown(df[['id','name']].rename(columns={"id": "value", "name": "label"}).to_dict('records'), 1, id='worker-dropdown'),
            ),
            html.Br(),
html.Div(
        children=[
    dbc.Button("Add Leave", id="leav-add",color='danger'),
        ],
        style={"flex-direction":"row","display":"flex","justify-content":"center"}
    ),
               html.Hr(),
    html.H1('View Workers list', style={'textAlign':'center'}),

        dash_table.DataTable(df2.sort_values(by=['startDate']).to_dict('records'),id='tbl3',
                                  page_current=0,
    # page_size=8,
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
    
    ),
    
    modal3
        ]
    )

    ]
)