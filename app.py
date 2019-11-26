import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import altair as alt
import vega_datasets

alt.data_transformers.enable('default')
alt.data_transformers.disable_max_rows()

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'
df = pd.read_csv("Police_Department_Incidents_-_Previous_Year__2016_.csv")

df['datetime'] = pd.to_datetime(df[["Date","Time"]].apply(lambda x: x[0].split()[0] +" "+x[1], axis=1), format="%m/%d/%Y %H:%M")
df['hour'] = df['datetime'].dt.hour
df.dropna(inplace=True)

top_4_crimes = df['Category'].value_counts()[:6].index.to_list()
top_4_crimes

top_4_crimes.remove("NON-CRIMINAL")
top_4_crimes.remove("OTHER OFFENSES")

# top 4 crimes df subset
df_t4 = df[df["Category"].isin(top_4_crimes)].copy()
def make_plot():

    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default
    # Create a plot of the Displacement and the Horsepower of the cars dataset
    
    # making the slider
    slider = alt.binding_range(min = 0, max = 23, step = 1)
    select_hour = alt.selection_single(name='hour', fields = ['hour'],
                                    bind = slider, init={'hour': 0})
    chart = alt.Chart(df_t4).mark_bar().encode(
        x=alt.X('Category:N', title = "Crime category", axis = alt.Axis(labelAngle = 0)),
        y=alt.Y('count()', title = "Count" , scale = alt.Scale(domain = (0,3300))),
        tooltip='count()'
    ).properties(
        title = "Per hour crime occurrences for the top 4 crimes",
        width=600,
        height = 400
    ).add_selection(
        select_hour
    ).transform_filter(
        select_hour
    )
    return chart

app.layout = html.Div([

    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1("First dashboard !"),
    html.H2("subtitle"),
    html.H5("The plot"),
    html.Iframe(
        sandbox = "allow-scripts",
        id = "plot",
        height = "500",
        width = "700",
        style = {"border-width": "5px"},

        srcDoc = make_plot().to_html()
        ),
        dcc.Markdown("""
        ### Here is a markdown cell

        !>---[here](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png)
        """),
])
if __name__ == '__main__':
    app.run_server(debug=True)