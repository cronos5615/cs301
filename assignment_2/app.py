import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State



stock_df = pd.read_csv("StockData.csv").dropna()
app = Dash(__name__)
months=stock_df['Month'].unique()
filter_options=['Open','Close','High','Low']

color_palette= {
    'Google':'#00F000',
    'Apple':'#FF0000',
    'Amazon':'#800080',
    'Microsoft':'#0000FF',
    'Tesla':'#F0A500'
}

avg_open = stock_df[stock_df['Month']==months[0]].groupby('Company')[filter_options[0]].mean().reset_index()

fig_barchart = px.bar(avg_open,x='Company',y=filter_options[0],color='Company',color_discrete_map=color_palette,labels={filter_options[0]:f'Average {filter_options[0]} Prices of Each Company'},title=f'Average {filter_options[0]} Prices of Each Company',template='simple_white')
fig_barchart.update_xaxes(showgrid=True)
fig_barchart.update_yaxes(showgrid=True)
fig_boxplot = px.box(stock_df[stock_df['Month']==months[0]],x='Company',y=filter_options[0],title=f"Stock {filter_options[0]} Price Distribution",color='Company',color_discrete_map=color_palette,template='simple_white')
fig_boxplot.update_xaxes(showgrid=True)
fig_boxplot.update_yaxes(showgrid=True)
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(
            children="Stock Market Analysis Dashboard",
            style={
                'textAlign' : 'center'
            }
        )
    ]),
    html.Div(style={
        'display':'flex',
        'flexDirection':'row',
        'alignItems':'center',
        'justifyContent':'center',
        'gap':'20px'

    },
        children=[
            html.Div(
                style={
                    'display':'flex',
                    'alignItems':'center',
                    'gap':'10px'
                },
                children=[
                html.Label(html.B("Select Month:")),
                dcc.Dropdown(
                        id='month_dropdown_comp',
                        options=months,
                        value=months[0],
                        clearable=True,
                        style={
                            "width": "150px",
                        }
                )]),
            
            html.Div(
                style={
                    'display':'flex',
                    'alignItems':'center',
                    'gap':'10px'
                },
                children=[ 
                html.Label(html.B("Select Stock Price Metric:")),
                dcc.RadioItems(
                    id='metric_radio_comp',
                    options=filter_options,
                    value=filter_options[0],
                    inline=True
                )]),
            html.Button( "Update Charts",id='UpdateButton')
    ]),

    html.Div(style={
        'display':'flex',
        'flexDirection':'row',
        'justifyContent':'center',

    },children=[
        html.Div(style={'width':'25%'},children=[
        dcc.Graph(id='bargraph',
        figure=fig_barchart),
    ]),
        html.Div(style={'width':'25%'},children=[
        dcc.Graph(id='boxplot',
        figure=fig_boxplot),
    ]),


    ]) 




#this is the end of the children of div
]

#this is the end of div
)

@app.callback(
    [Output('bargraph','figure'),
    Output('boxplot','figure')],
    Input('UpdateButton','n_clicks'),
    State('month_dropdown_comp','value'),
    State('metric_radio_comp','value')
)
def update_graphs(clicks,month,metric):
    avg_metric = stock_df[stock_df['Month']==month].groupby('Company')[metric].mean().reset_index()
    fig_barchart = px.bar(avg_metric,x='Company',y=metric,color='Company',color_discrete_map=color_palette,labels={metric:f'Average {metric} Prices of Each Company'},title=f'Average {metric} Prices of Each Company',template='simple_white')
    fig_barchart.update_xaxes(showgrid=True)
    fig_barchart.update_yaxes(showgrid=True)

    fig_boxplot = px.box(stock_df[stock_df['Month']==month],x='Company',y=metric,title=f"Stock {metric} Price Distribution",color='Company',color_discrete_map=color_palette,template='simple_white')
    fig_boxplot.update_xaxes(showgrid=True)
    fig_boxplot.update_yaxes(showgrid=True)
    return fig_barchart,fig_boxplot

if(__name__ == "__main__"):
    app.run(debug=True)



