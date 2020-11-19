#Its just a web app for analysing cars, i focus more on few features, which are:
#Price,engine_size,cylinder,horsepower,horsepower_squared and fuel_type.
#Constructed two plots, scatter and sunburst,
#-----------------------------------------------------------------------
#Import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

#-----------------------------------------
#Read the data

df = pd.read_excel('Cars.xlsx')

print(df[:6])

#---------------------------------------------------
#app layout. This is reponsible for the tree i mean structure of the app i.e how the app should look like
app.layout = html.Div([
    #This is displays the web apps header
    html.H1("Car Analysis dashboard with dash", style={'text-align':'center','color':'brown'}),
    #This displays the input which in this case is a drop down where you select the car type
    dcc.Dropdown(id="selected-body-type",
                options=[
                     {'label':'convertible','value':'convertible'},
                     {'label':'sedan','value':'sedan'},
                     {'label':'hatchback','value':'hatchback'},
                     {'label':'wagon','value':'wagon'},
                     {'label':'hardtop','value':'hardtop'}],
                multi=False,
                value='sedan',
                style={'width':'30%','color':'rgb(80,80,80)'}),
    #Now structure for the output plots
    html.Div(id="Output_container",style={'text-align':'center','color':'blue'}),
    html.Br(),

    dcc.Graph(id='first_car_map'),
    html.Br(),

    html.Div(id="2nd_output",style={'text-align':'center','color':'blue'}),
    html.Br(),

    dcc.Graph(id='3rd_car_map')
    ])
    #---------------------------------------------------------------------------------
#add callbacks
#Callbacks are responsible for the interractiveness of the web app.
@app.callback(
    #Here goes what actually links the layout and the callback components
    [Output(component_id="Output_container",component_property="children"),
    Output(component_id="first_car_map",component_property="figure"),
    Output(component_id="2nd_output",component_property="children"),
    Output(component_id="3rd_car_map",component_property="figure")],
    [Input(component_id="selected-body-type",component_property="value")]
)
#Here is the functions that updates the web app immediately any change happens to the input.
def plot_the_graph(style_selected):
    print(style_selected)
    print(type(style_selected))
    #first Output
    chosenStyle = "The car style chosen by user is : {}".format(style_selected)
    #Third Output
    sun = "sunburst plot for {} is".format(style_selected)
    #Made a copy of my data, heard its a good practice.
    cdf = df.copy()
    #Input callback
    cdf = cdf[cdf["body_style"] ==style_selected]

    #---------------------------------------------------------------------------
    #plotlyexpess for the plots
    #Second Output using plotly.express for scatter plot.And i tell you, Its work wonders.
    fig = px.scatter(data_frame=cdf,
                    x='engine_size',
                    y="price",
                    color='fuel_type',
                    hover_name='cylinders',
                    size='horsepower_squared',
                    template='plotly_dark'
                    )
    

    fig.update_layout(transition_duration=500)
    #fourth output , using plotly again to plot Sunburst, and i tell you, this bursts brains.
    fig1 = px.sunburst(cdf,
                      path=['fuel_type','cylinders'],
                      values='price',
                      color='horsepower',
                      template='plotly_dark'
                      )
    #Here i return all my four outputs
    return [chosenStyle, fig,sun,fig1]

#------------------------------------------------------------------------------
#Just use this to run it on the serverrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr.
if __name__ == "__main__":
    app.run_server(debug=True)
#App works fine, TO GOD BE THE GLORY.