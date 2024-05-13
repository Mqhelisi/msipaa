import dash
from dash import html, dash_table, Input, Output, State, callback, callback_context
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
import time
import numpy as np
import math
from pg2 import page2, modal2
from pg1 import page1
from pg3 import page3, modal3
from models import Work,Worker,Leave,add_leave,check_worker_leave,read_workers,add_work,read_works


# load data
# df = pd.DataFrame(read_workers())

# make plot
# initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

labelDict = {   

    'margin':'0 10px 10px',
    'text-shadow':'1px 1px 1px blue',
    'font-size':'25px'
    }


tabs = dbc.Tabs(
    [
        dbc.Tab(page1, label="Job Viewer",tab_id='tab-1'),
        dbc.Tab(page2, label="Job Adder",tab_id='tab-2'),
        dbc.Tab(page3, label="Leave Manager",tab_id='tab-3'),
    ],id='tabs'
)
app.layout = tabs
# set app layout
@app.callback(Output("tbl", "data"), [Input("tabs", "active_tab")]
              )
def switch_tab(at):
    if at == "tab-1":
        return pd.DataFrame(read_works()).to_dict('records')
    elif at == "tab-3":
        return pd.DataFrame(read_workers()).to_dict('records')
    # return html.P("This shouldn't ever be displayed...")
# Callback for getting table details
@app.callback(
    # Output('tbl_out', 'children'),
        [Output("modal", "is_open"),
         Output("name-label","children"),
         Output("sex-label","children"),
         Output("age-label","children"),
         Output("ticket-label","children")
         
         ],
               
              [Input('tbl', 'active_cell'),
            #    Input("open", "n_clicks"), 
               Input("close", "n_clicks")
               ],
              [State('tbl', 'selected_rows'),State("modal", "is_open")],
          prevent_initial_call=True)
def update_graphs(active_cell,n2,rows,is_open):
    dff = pd.DataFrame(read_works())

    if bool(active_cell) or n2:
        rowdeet = dff.iloc[active_cell['row']].to_dict()
        print(rowdeet)

        return not is_open,rowdeet['descr'],rowdeet['capacity'],rowdeet['status'],rowdeet['workers']
    return is_open,None,None,None,None

    # return str(active_cell) if active_cell else "Click the table"

@app.callback(
    # Output('tbl_out', 'children'),
[Output("modal2", "is_open"),
Output("job-modal-deet", "children"),
Output("job-modal-date", "children"),
Output("tbl2", "data"),
Output("job-modal-labor", "children"),
Output("job-modal-cap", "children")
],[
    Input("workerr", "n_clicks"), 
    Input("close2", "n_clicks")],
        [
        State('job-datepick', 'date'),
        State('cap-input', 'value'),
        State('job-input', 'value'),
        State("modal2", "is_open")],
        prevent_initial_call=True)
def showJobs(srchBtn,clseBtn,jobDate,capDate,jobDet,modState):
    df=pd.DataFrame(read_workers())
    if srchBtn:
        capWork = math.ceil(capDate * 0.65)
        return not modState,jobDet,jobDate,df.sort_values(by=['leaveDays']).to_dict('records'),capWork,capDate
    if clseBtn:
        return not modState,None,None,None,None,None
    

@app.callback(
    # Output('tbl_out', 'children'),
        [
            Output("modal3", "is_open"),
            Output("leave-modal-type", "children"),
            Output("leave-modal-strt", "children"),
            Output("leave-modal-end", "children"),
            Output("leave-modal-wrkr", "children"),
            Output("leave-resp", "children", allow_duplicate=True),

            Output("leave-modal-deduct", "children")
            ],
              [
               Input("leav-add", "n_clicks"), 
               Input("close3", "n_clicks")],
              [State('leave-date-picker-range', 'start_date'),
              State('leave-date-picker-range', 'end_date'),
              State('leave-dropdown', 'value'),
              State('worker-dropdown', 'value'),
          State("modal3", "is_open")],
          prevent_initial_call=True)
def leaveModal(srchBtn,clseBtn,leaveStrt,leaveEnd,leaveTyp,wrkrNm,modState):
    if srchBtn:
        if leaveTyp != 'Sympathetic':
            ddction = np.busday_count(leaveStrt,leaveEnd)
            return not modState,leaveTyp,leaveStrt,leaveEnd,wrkrNm,None,ddction
        else:
            return not modState,leaveTyp,leaveStrt,leaveEnd,wrkrNm,None,0

    if clseBtn:
        return not modState,None,None,None,None,None,None



@app.callback(
    # Output('tbl_out', 'children'),
        
            Output("leave-resp", "children"),

              [
               Input("leav-upd", "n_clicks"), 
               Input("close3", "n_clicks")],
              [State('leave-modal-strt', 'children'),
              State('leave-modal-end', 'children'),
              State('leave-modal-type', 'children'),
              State('leave-modal-wrkr', 'children'),
              State('leave-modal-deduct', 'children'),
              
              
          State("modal3", "is_open")
          ],
          prevent_initial_call=True)

def makeLeave(leaveBtn,closeBtn,leaveStrt,leaveEnd,leaveTyp,wrkrid,dedction,modState):
    # ctx = callback_context
    # print(leaveBtn)
    # print(ctx.triggered[0]['prop_id'])
    # print('running mklv')
    # return "woww"
    chck,dysLft = check_worker_leave(wrkrid,dedction)
    if chck == None:
        return "Leave Check Failed"
    elif(chck):
        return add_leave(dysLft, wrkrid,leaveStrt,leaveEnd,date.today(),leaveTyp)
    else:
        print(chck)
        return "Not Enough days, only have " + str(dysLft)  
@callback(
    Output('job-resp', "children"),
    Input('accpt', "n_clicks"),
    [
    State('tbl2', "derived_virtual_data"),
    State('tbl2', "derived_virtual_selected_rows"),
    State("job-modal-deet", "children"),
    State("job-modal-date", "children"),
    State("job-modal-labor", "children"),
    State("job-modal-cap", "children")
    ])
def update_graphs(accp,rows, derived_virtual_selected_rows,
                  job_detail,job_date,job_labor,job_cap
                  ):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    df = pd.DataFrame(read_workers())
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
        return None
    # print(derived_virtual_selected_rows)
    dff = df if rows is None else pd.DataFrame(rows)
    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]
    df2 = dff.iloc[derived_virtual_selected_rows]
    df2 = df2[['name','id','position']]
    # df2 = df2[['PassengerId','Name','Ticket']]

    donta = add_work(job_detail,job_date,job_cap,'open',df2.to_dict('records'))

    return donta




@app.callback(Output('tbl', 'page_size'), 
              Input('searcher', 'n_clicks'),
          prevent_initial_call=True)
def stump(actv):
    time.sleep(1)
    return 5


if __name__ == "__main__":
    app.run_server(debug=True)
