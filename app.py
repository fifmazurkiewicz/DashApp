"""
A simple application which presents
a dashboard written in dash and an example of its use in the form of several graphs.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

# Load data
df = pd.read_csv(r'D:\Odys#24\projekty\dash/top100richest_prepr.csv', sep='\t')
mapbox_access_token = 'your token'

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


def get_options(list_options):
    dict_list = []
    for i in list_options:
        dict_list.append({'label': i, 'value': i})
    return dict_list


app.layout = html.Div(
    children=[
        html.Div(className='row',
                 id='main_output',
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[
                                  html.P('Pick one type of chart from the dropdown below.'),
                                  # type chart selector
                                  html.Div(
                                      className='div-for-dropdown',
                                      id='div-for-chart-selector',
                                      children=[
                                          dcc.Dropdown(
                                              id='chart_dropdown',
                                              options=[
                                                  {'label': 'Top10 by Years', 'value': 'chartYears'},
                                                  {'label': 'Top10 by Country ', 'value': 'chartCountries'},
                                                  {'label': ' Search name', 'value': 'chartSearchName'},
                                                  {'label': 'Map ', 'value': 'chartMap'}
                                              ],
                                              value='chartYears'
                                          ),
                                          html.Div(id='dd-output-container'),
                                      ],
                                      style={'color': '#1E1E1E'}
                                  ),
                              ]
                              ),
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  dcc.Graph(id='chart', config={'displayModeBar': False}, animate=True)
                              ]),
                 ])
    ]

)


# select chart type
@app.callback(
    Output('dd-output-container', 'children'),
    [Input('chart_dropdown', 'value')],
    [State('div-for-chart-selector', 'children')])
def update_output(value, old_output):
    if value == "chartYears":
        return [html.Div(
            id="additional_div",
            className='additional_selector',
            children=[
                html.P('Pick Year.'),
                dcc.Dropdown(id='selector_chart_types',
                             options=get_options(df['Year'].unique()),
                             searchable=True,
                             # multi=True,
                             value=df['Year'].sort_values()[0],
                             style={'backgroundColor': '#1E1E1E'},
                             className='selector_chart_types'
                             ),
                ###### Button triggers calculations necessary for links#####
                html.Div([
                    html.Button('Show Top10 in given year', className="show-details-button", n_clicks=0,
                                id='show-details-button'),
                ], className="show-detail-button-div"),

                ##### DETAILED INFO MODAL ######
                html.Div([
                    html.Label(id="label_modal", children=[
                        "Order as shown in the legend"]),
                    html.Div([
                        html.Button('Close', className="close-button", n_clicks=0, id='close-button'),
                    ], className="close-button-div"),
                ], className="modal-container", id="modal-container", style={'display': 'none'}),
                ##### MODAL BACKDROP ######
                html.Div([
                ], className="modal-backdrop", id="modal-backdrop", style={'display': 'none'}),
                html.Div(id='modal-button-values', children="Get:0 Close:0 last:Close",
                         style={'display': 'none'}),
            ],
            style={'color': '#1E1E1E'}),
        ]

    if value == "chartCountries":
        return [html.Div(
            className='search_selector',
            children=[
                html.P('Pick or insert Country'),
                dcc.Dropdown(id='selector_chart_types', options=
                get_options(df['Country'].unique()),
                             searchable=True,
                             # multi=True,
                             value=df['Country'].sort_values()[0],
                             style={'backgroundColor': '#1E1E1E'},
                             className='selector_chart_types'
                             ),
                ###### Button trigger calculations necessary for links and thumbnails#####
                html.Div([
                    html.Button('Get info', className="show-details-button", n_clicks=0,
                                id='show-details-button'),
                ], className="show-detail-button-div"),

                ##### DETAILED INFO MODAL ######
                html.Div([
                    html.Label(id="label_modal", children=[
                        "Order as shown in the legend"]),
                    html.Div([
                        html.Button('Close', className="close-button", n_clicks=0, id='close-button'),
                    ], className="close-button-div"),
                ], className="modal-container", id="modal-container", style={'display': 'none'}),
                ##### MODAL BACKDROP ######
                html.Div([
                ], className="modal-backdrop", id="modal-backdrop", style={'display': 'none'}),
                html.Div(id='modal-button-values', children="Get:0 Close:0 last:Close",
                         style={'display': 'none'}),
            ],
            style={'color': '#1E1E1E'}),
        ]
        ######## IF  USER CHOSE country VIEW ##########
    if value == "chartSearchName":
        return [html.Div(
            className='search_selector',
            children=[
                html.H1(" "),
                dcc.Dropdown(id='selector_chart_types',
                             searchable=True,
                             options=get_options(df['Name'].unique()),
                             multi=True,
                             value=[df['Name'].sort_values()[0]],
                             style={'backgroundColor': '#1E1E1E'},
                             className='selector_chart_types',
                             ),
            ],
            style={'color': '#1E1E1E'})]

        ######## IF  USER CHOSE map VIEW ##########
    if value == "chartMap":
        return [html.Div(id='selector_chart_types',
                         className='selector_chart_types',
                         children=[
                             html.P('Pick Year.'),
                             dcc.Dropdown(id='selector_chart_types',
                                          options=get_options(df['Year'].unique()),
                                          searchable=True,
                                          # multi=True,
                                          value=df['Year'].sort_values()[0],
                                          style={'backgroundColor': '#1E1E1E'},
                                          className='selector_chart_types'
                                          ),
                         ],
                         style={'color': '#1E1E1E'})]


# Create links for modal bar
def create_links(df_sub):
    df_sub = df_sub.sort_values(by='NetWorthinBillionUSD', ascending=False)
    names_details = df_sub.Name.unique()
    try:
        links = {
            i: f"https://www.google.com/search?q={i}"
            for i in names_details}
        new_label = [html.Label(id="label_link", children=[
            f"Ranking of the richest people and their wealth "])]
        new_elem = [html.Label(children=[f"{i + 1} :", html.A(f' {df_sub.Name.unique()[i]}', id="link_name",
                                                              href=links[df_sub.Name.unique()[i]], target="_blank"),
                                         f"  {df_sub.NetWorthinBillionUSD.values[i]}"
                                         ]) for i in
                    range(len(df_sub.Name.unique()))]
        return new_label + new_elem
    except Exception as exp:
        print(exp)
        return None


# Fill modal bar with data  for each view
@app.callback(Output("label_modal", "children"),
              [Input("show-details-button", "n_clicks"), State('selector_chart_types', 'value'),
               State('chart_dropdown', 'value')])
def update_body_image(n_clicks, selected_dropdown_value, value_chart):
    new_layout = None
    if value_chart == "chartYears":
        df_sub = prep_years_data(selected_dropdown_value)
        if df_sub is not None:
            new_layout = create_links(df_sub)
            return new_layout
        else:
            return new_layout

    if value_chart == "chartCountries":
        df_sub = prep_country_data(selected_dropdown_value)
        if df_sub is not None:
            new_layout = create_links(df_sub)
            return new_layout
        else:
            return new_layout


# General behaviour for modal bar (openning, closing)
@app.callback(Output('modal-button-values', 'children'),
              [Input('show-details-button', 'n_clicks'), Input('close-button', 'n_clicks')],
              [State('modal-button-values', 'children')], [])
def modal_button_status(get_clicks, close_clicks, button_values):
    button_values = dict([i.split(':') for i in button_values.split(' ')])

    if get_clicks > int(button_values["Get"]):
        last_clicked = "Get"
    elif close_clicks > int(button_values["Close"]):
        last_clicked = "Close"
    else:
        last_clicked = "Close"

    return "Get:{0} Close:{1} last:{2}".format(get_clicks, close_clicks, last_clicked)


@app.callback(Output('modal-container', 'style'),
              [Input('modal-button-values', 'children')],
              [], [])
def modal_display_status(button_values):
    button_values = dict([i.split(':') for i in button_values.split(' ')])

    if button_values["last"] == 'Get':
        return {'display': 'inline'}
    else:
        return {'display': 'none'}


# Preapre data and draw chart for each view
@app.callback(Output('chart', 'figure'),
              Input('selector_chart_types', 'value'), State('chart_dropdown', 'value'))
def update_graph(selected_dropdown_value, value_chart):
    if value_chart == "chartYears":
        df_sub = prep_years_data(selected_dropdown_value)
        figure = draw_years_graph(df_sub)
        return figure
    if value_chart == "chartSearchName":
        df_sub = prep_searchName_data(selected_dropdown_value)
        figure = draw_linechart(df_sub)
        return figure

    if value_chart == "chartMap":
        df_sub = prep_map_data(selected_dropdown_value)
        figure = draw_map(df, df_sub[1])
        return figure

    if value_chart == "chartCountries":
        df_sub = prep_country_data(selected_dropdown_value)
        figure = draw_linechart(df_sub)
        return figure


# Simple preparing dataset for years view
def prep_years_data(i):
    if i:
        data = df[df.Year == i].head(10)
        return data
    else:
        return None


def prep_country_data(i):
    if i:
        data = df[(df.Country == i)]
        data_sub = data.groupby('Year').head(10)
        data = data[data.index.isin(data_sub.index)]
        return data
    else:
        return None


# Prepare dataset for searching by Name view
def prep_searchName_data(i):
    if i:
        data = df[df.Name.isin(i)]
        return data
    else:
        return None


# Prepare dataset for maps
def prep_map_data(i):
    if i:
        data = df[df.Year == i]
        data = data.groupby("Country").agg({'Name': 'nunique'})
        size = pd.merge(df, data, on="Country")
        return [data, size]
    else:
        return None


## Prepare monthly graph
def draw_years_graph(df_sub):
    trace1 = []
    if df_sub is not None:
        trace1.append(go.Bar(x=df_sub.Name.values, y=df_sub.NetWorthinBillionUSD.values,
                             opacity=0.9,
                             textposition='inside'))
        figure = go.Figure(data=trace1,
                           layout=go.Layout(
                               title=go.layout.Title(text="What was the wealth of the top10 in different years"),
                               template='plotly_dark',
                               autosize=True, ))
        figure.update_traces(hovertemplate='Name: %{x} <br>Value: %{y}')
        figure.update_layout(title_text=f'Top10',
                             xaxis_title="Years",
                             yaxis_title=f"NetWorthinBillionUSD",
                             )
        return figure
    else:
        try:
            figure = go.Figure()
            figure.update_layout(title="Default Blank Chart",
                                 template="plotly_dark")
            return figure
        except Exception as exp:
            print(exp)
            return None


## Prepare Top10 richest people in a chosen country
def draw_linechart(df_sub):
    trace1 = []
    if df_sub is not None:
        for i in df_sub.Name.unique():
            data = df_sub[df_sub.Name == i]
            country_sub = data.Country.unique()
            try:
                trace1.append(go.Scatter(x=df_sub.Year.unique(), y=data.NetWorthinBillionUSD.values,
                                         mode='lines',
                                         opacity=0.9,
                                         name=data.Name.unique()[0],
                                         textposition='bottom center'))
            except Exception as exp:
                print(exp)
        figure = go.Figure(data=trace1,
                           layout=go.Layout(
                               title=go.layout.Title(text="Top10 richest people in a chosen country "),
                               template='plotly_dark',
                               autosize=True))
        figure.update_traces(mode="markers+lines", hovertemplate='Year: %{x} <br>Value: %{y}')
        figure.update_layout(
            legend_title="Please, refresh legend",
            xaxis_title="Year",
            yaxis_title="NetWorthinBillionUSD",
        )
        return figure
    else:
        figure = go.Figure()
        figure.update_layout(title="Default Blank Chart",
                             template="plotly_dark")
        return figure


# Prepare map graph
def draw_map(df_sub, size):
    if df_sub is not None:
        try:
            figure = px.scatter_geo(size,
                                    lat=size.Latitude,
                                    lon=size.Longitude,
                                    color="Country",
                                    size=size.Name_y)
            figure.update_layout(
                title='Number of richest people per country',
                autosize=True,
                template="plotly_dark",
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=38,
                        lon=-94
                    ),
                    pitch=0,
                    zoom=3,
                    style='light'
                ),
            )
            return figure
        except Exception as exp:
            print(exp)
    else:
        figure = go.Figure()
        figure.update_layout(title="Default Blank Chart",
                             template="plotly_dark")
        return figure


if __name__ == '__main__':
    app.run_server(debug=True)
