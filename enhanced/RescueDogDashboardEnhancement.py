# RescueDogDashboardEnhancement.py

#********************************
# Sarah Hayduk
# SNHU CS-499 Capstone
# Enhancement Category 2
# Algorithms & Data Structures
#********************************

#----------------------------------------------------------------------------------
# Dashboard Imports
#
# This section loads all modules for the Dashboard. Dash provides the UI framework,
# Plotly handles visualizations, and dash_leaflet renders the geolocation map.
# The CRUD module supplies database access to the Austin Animal Ceneter dataset.
#----------------------------------------------------------------------------------
from dash import Dash, dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import plotly.express as px
import base64
import os
import numpy as np
import pandas as pd
from PythonModule_Hayduk import CRUD

#----------------------------------------------------------------------------------
# Database Initialization
#
# Connect to MonogDB through CRUD module and load the full databset on startup.
# MongoDB automatically includes an internal "_id" field, which must be removed
# because the DataTable cannot serialize ObjectID types.
#----------------------------------------------------------------------------------
db = CRUD()
df = pd.DataFrame.from_records(db.read({}))
df.drop(columns=['_id'],inplace=True)

#########################
# Dashboard Layout / View
#########################
app = Dash(__name__)

#----------------------------------------------------------------------------------
# Logo Loading
#
# Check that the file exists and load logo from the project folder. If it doesn't
# exist, the dashboard continues without rendering the logo to prevent crashes.
#----------------------------------------------------------------------------------
image_filename = 'Grazioso Salvare Logo.png'

if os.path.exists(image_filename):
    with open(image_filename, 'rb') as f:
        encoded_image = base64.b64encode(f.read())
else:
    print(f"Warning: Logo file '{image_filename}' not found.")
    encoded_image = None

#----------------------------------------------------------------------------------
# Dashboard Header
# 
# The header displays two clickable logos and a centered title/subtitle. Flex
# conatiner used to align elements horizontally while keeping title vertically
# stacked. Both logos link to the SNHU homepage.
#----------------------------------------------------------------------------------
app.layout = html.Div([

    # Store last rescue button type so dropdown behaves correctly
    dcc.Store(id='last-rescue-type', data='none'),

    html.Div(id='hidden-div', style={'display':'none'}),
    html.Div([
        # ---------- Left logo (clickable) ----------
        html.A(
            href = 'https://www.snhu.edu',
            target = 'blank',
            title = 'SNHU Home Page',
            children = html.Img(
                src = 'data:image/png;base64,{}'.format(encoded_image.decode()),
                id = 'logo-left',
                #scale image, prevent from stretching within flex container
                style = {
                    'height': '150px',
                    'margin-right': '20px',
                    'flex': '0 0 auto'
            })
        ),
        # ---------- Title & subtitle (stacked vertically) ----------
        html.Div([
            html.H1("Grazioso Salvare Rescue Dog Dashboard",
                    style={
                        'color': 'rgb(145, 0, 115)', 
                        'margin': '0'}),
            html.P("Powered by Austin Animal Center Data",
                  style={
                      'fontSize': '16px',
                      'color': 'black',
                      'marginTop': '4px',
                      'fontStyle': 'italic'
                  })
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center'
            } 
        ),
        # ---------- Right logo (clickable) -----------
        html.A(
            href = 'https://snhu.edu',
            target = 'blank',
            title = 'SNHU Home Page',
            children = html.Img(
                src = 'data:image/png;base64,{}'.format(encoded_image.decode()),
                id = 'logo-right',
                #scale image, prevent from stretching within flex container
                style={
                    'height': '150px',
                    'margin-right': '20px',
                    'flex': '0 0 auto'
            })
        )
    # ---------- Flex container ----------
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '12px',
        'margin-top': '10px',
        'paddingLeft': '20px',
        'paddingRight': '20px'
    }),
    html.Hr(),
    
    #----------------------------------------------------------------------------------
    # Rescue Filter Options
    #
    # This section contains the Water, Mountain, Disaster and Reset buttons used to
    # filter the database. A dynamic header displays the active rescue category. The
    # breed-match dropdown appears only when a rescue type is selected and supports
    # strict (preferred breeds only) and expanded (include mixed breeds) matching.
    #----------------------------------------------------------------------------------
    html.Div(
        style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'flex-start',
            'gap': '20px',
            'marginBottom': '10px'
        },
        # --------- Rescue type & Reset buttons ----------
        children=[
            html.Div(className='buttonRow',
            style={
                'display' : 'flex', 
                'gap': '10px'
            },
            children=[
                html.Button(id='submit-button-one', n_clicks=0, children='Water Rescue'),
                html.Button(id='submit-button-two', n_clicks=0, children='Mountain Rescue'),
                html.Button(id='submit-button-three', n_clicks=0, children='Disaster Rescue'),
                html.Button(id='submit-button-four', n_clicks=0, children='Reset')
                ]
            ),
            # --------- Status header that updates to show type displayed ----------
            html.Div(id='rescue-type-header', style={
                'fontWeight': 'bold',
                'color': 'black',
                'fontSize': '14px'
            }),
            # ---------- Breed-match dropdown (hidden until a rescue type is selected) ----------
            html.Div(
                id='breed-match-container', 
                style={'display': 'none'},
                children=[
                    dcc.Dropdown(
                        id='breed-match-dropdown',
                        options=[
                            {'label': 'Preferred Breeds Only', 'value': 'strict'},
                            {'label': 'Include Mixed Breeds', 'value': 'expanded'}
                        ],
                        value='strict',
                        clearable=False,
                        style={'width': '250px', 'fontSize': '12px'}
                    )
                ]
            )
        ]),
        
    html.Hr(),

    #----------------------------------------------------------------------------------
    # DataTable Configuration
    #
    # The DataTable provides interactive sorting, filtering, pagination, and row
    # selection. Row selection is used to sync the map and highlight the selected row.
    # Custom styling improves readability and aligns with Dashboard color theme.
    #----------------------------------------------------------------------------------
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                         data=df.to_dict('records'),
                         
                         # ---------- Features for interactive data table ----------
                         editable=False,
                         filter_action="native",
                         sort_action="native",
                         column_selectable=False,
                         row_selectable="single", #enable single row selection for mapping callback
                         row_deletable=False,
                         selected_columns=[],
                         selected_rows=[0], #default to first row on load
                         page_action="native",
                         page_current=0,
                         page_size=10, #10 results per page
                         
                         # ---------- Customizations to header and cells ----------
                         style_header={
                             'backgroundColor': 'rgb(145, 0, 115)', #purple
                             'color': 'white', 
                             'fontWeight': 'bold',
                             'fontSize': '14px'
                         },
                         style_data={
                             'color': 'black',
                             'backgroundColor': 'white'
                         },
                         style_cell={
                             'textAlign': 'left',
                             'padding': '5px'
                         }),
    html.Br(),
    html.Hr(),

    #----------------------------------------------------------------------------------
    # Visualization Row
    #
    # This sets up the dashboard so the chart and geolocation chart are side-by-side
    # Keeps componenets centered and responsive as the browser window resizes.
    #----------------------------------------------------------------------------------
    html.Div(className='row',
         style={'display' : 'flex',
               'justifyContent': 'center',
               'alignItems': 'center'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ]),

    #----------------------------------------------------------------------------------
    # Dashboard Footer
    #
    # Displays project identifiers and clickable logo in a horiztonal layout.
    #----------------------------------------------------------------------------------
    html.Div(
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'marginTop': '20px',
            'paddingLeft': '40px',
            'paddingRight': '40px',
            'gap': '20px'
        },
        # ---------- Text (centered & stacked) ----------
        children = [
            html.Div([
                html.Div(
                    "© 2026 CS-499 Computer Science Capstone",
                    style={
                        'color': '#910073',
                        'fontSize': '24px',
                        'fontWeight': 'bold',
                    }
                ),
                html.Div(
                    "Refactor by: Sarah Hayduk",
                    style={
                        'color': '#910073',
                        'fontSize': '18px',
                        'fontWeight': 'normal',
                        'marginTop': '4px'
                    }
                )
            ],
            style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center'
            }),
            # ---------- Logo (clickable link) ----------
            html.A(
                href = 'https://snhu.edu',
                target = 'blank',
                title = 'SNHU Home Page',
                children = html.Img(
                    src = 'data:image/png;base64,{}'.format(encoded_image.decode()),
                    id = 'foot_logo',
                    style={'height': '100px'}
                )
            )
        ]
    )
])

#############################################
# Interaction Between Components / Controller
#############################################

#----------------------------------------------------------------------------------
# Rescue Filter Callback
# 
# This callback handles all rescue-type filtering logic. It determines which button
# triggered the update, applies the correct MonogDB query, and manages the state of
# the breed-match dropdown. A dcc.Store component in app.layout preserves the last
# rescue type so the dropdown behaves consistently when changed independently.
#----------------------------------------------------------------------------------
@app.callback(
    Output('datatable-id', 'data'),
    Output('rescue-type-header', 'children'),
    Output('datatable-id', 'filter_query'),
    Output('datatable-id', 'sort_by'),
    Output('datatable-id', 'selected_rows'),
    Output('breed-match-container', 'style'),
    Output('last-rescue-type', 'data'),
    Output('breed-match-dropdown', 'value'), # Reset dropdown
    [
        Input('submit-button-one', 'n_clicks'), # Water button
        Input('submit-button-two', 'n_clicks'), # Mountain button
        Input('submit-button-three', 'n_clicks'), # Disaster button
        Input('submit-button-four', 'n_clicks'), # Reset button
        Input('breed-match-dropdown', 'value')
    ],
    State('last-rescue-type', 'data')
)

#----------------------------------------------------------------------------------
# on_click
#
# Primary controller for all rescue-type filtering logic. This callback determines
# which UI element triggered the update, applies the appropriate MongoDb query,
# and syncs the breed-match dropdown with the selected rescue type. When a rescue
# button is pressed, the dropdown resets to strict mode to ensure predictable
# filtering behavior.
#----------------------------------------------------------------------------------
def on_click(water, mountain, disaster, reset, match_type, last_rescue_type):
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    # ---------- Breed-match dropdown ------------
    if triggered_id == 'breed-match-dropdown':
        rescue_type = last_rescue_type
        reset_dropdown = match_type # Keep current dropdown value
    else:
        rescue_type = triggered_id
        reset_dropdown = 'strict' # Reset dropdown when button clicked

    # ---------- Breed-match algorithm ---------------------------------------------
    # Anchored regex supports strict filtering while unanchored regex enables more
    # inclusive matching. This balances strictness vs. inclusiveness and reflects
    # the performance tradeoffs between reduced search space and broader scan cost.
    # -------------------------------------------------------------------------------
    def regex(breed, anchored=True):
        return {'breed': {'$regex': f'^{breed}$' if anchored else breed, '$options': 'i'}}

    anchored = (reset_dropdown == 'strict')

    header_text = "Displaying All Animals"
    query = {}
    dropdown_style = {'display': 'none'}

    # ---------- WATER RESCUE FILTER LOGIC ----------
    if rescue_type == 'submit-button-one':
        header_text = "Displaying Water Rescue Dogs"
        dropdown_style = {'display': 'block'}
        query = {
            'animal_type': 'Dog',
            'sex_upon_outcome': 'Intact Female',
            'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156},
            '$or': [
                regex('Labrador Retriever Mix', anchored),
                regex('Chesa Bay Retr', anchored),
                regex('Newfoundland', anchored),

                # ---- Always include slash-based Labrador mixes -----
                regex('Labrador Retriever/', False),
                regex('/Labrador Retriever', False),
            ]
        }

    # ---------- MOUNTAIN RESCUE FILTER LOGIC ----------
    elif rescue_type == 'submit-button-two':
        header_text = "Displaying Mountain Rescue Dogs"
        dropdown_style = {'display': 'block'}
        query = {
            'animal_type': 'Dog',
            'sex_upon_outcome': 'Intact Male',
            'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156},
            '$or': [
                regex('German Shepherd', anchored),
                regex('Alaskan Malamute', anchored),
                regex('Old English Sheepdog', anchored),
                regex('Siberian Husky', anchored),
                regex('Rottweiler', anchored)
            ]
        }

    # ---------- DISASTER RESCUE FILTER LOGIC ----------
    elif rescue_type == 'submit-button-three':
        header_text = "Displaying Disaster Rescue Dogs"
        dropdown_style = {'display': 'block'}
        query = {
            'animal_type': 'Dog',
            'sex_upon_outcome': 'Intact Male',
            'age_upon_outcome_in_weeks': {'$gte': 20, '$lte': 300},
            '$or': [
                regex('Doberman Pinsch', anchored),
                regex('German Shepherd', anchored),
                regex('Golden Retriever', anchored),
                regex('Bloodhound', anchored),
                regex('Rottweiler', anchored)
            ]
        }

    # ---------- RESET VIEW TO ALL ANIMALS ----------
    elif rescue_type == 'submit-button-four':
        header_text = "Displaying All Animals"
        dropdown_style = {'display': 'none'}
        query = {}

    # ---------- Query DB and return updated table & UI state -----------
    df = pd.DataFrame.from_records(db.read(query))
    df.drop(columns=['_id'], inplace=True)

    return (
        df.to_dict('records'), header_text, '', [], [0],
        dropdown_style, rescue_type, reset_dropdown
    )

#----------------------------------------------------------------------------------
# Breed Distribution Chart
#
# Generates pie chart and displays breeds of dogs based on quantity represented
# in the data table. Chart updates automatically when the DataTable view changes.
# Custom colors and limiting the display to top 8 keeps pie chart readable.
#----------------------------------------------------------------------------------
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])

def update_graphs(viewData):
    
    # ---------- Prevent errors on initial load or empty table ----------
    if viewData is None or len(viewData) == 0:
        return html.Div("No map data available.")
    
    df = pd.DataFrame(viewData)
    
    # ----------- Count occurance of each breed ----------
    breed_counts = df['breed'].value_counts().reset_index()
    breed_counts.columns = ['breed', 'count']
    
    fig = px.pie(
        breed_counts.head(8), # Limit 8
        names = 'breed', # Slices by breed
        values = 'count', # Slice proportion by count
        color_discrete_sequence=[
            '#003F5C', #deep blue
            '#58508D', #muted purple
            '#8A508F', #plum
            '#Bc5090', #magenta
            '#DE5A79', #rose
            '#FF6361', #coral
            '#FF8531', #orange
            '#FFA600', #gold
        ]
    )
    # ---------- Display percentage on chart -----------
    fig.update_traces(textinfo='percent')
    
    # ---------- Return graph ----------
    return [dcc.Graph(figure=fig, style={
        'height': '500px',
        'width': '100%',
        'margin': 'auto'
    })]
    
    
#----------------------------------------------------------------------------------
# Row Highlighting
# 
# Highlights selected row in the DataTable to improve visibility. Only single
# row selection is supported for this dashboard.
#----------------------------------------------------------------------------------
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_rows')] 
)

def update_styles(selected_rows):
    return [{
        'if': {'row_index': i},
        'backgroundColor': '#FFEBDC' #peachish
    }    for i in selected_rows]


#----------------------------------------------------------------------------------
# Geolocation Map
#
# Updates map marker based on the selected row in the DataTable. If no row is
# selected, the first row is used by default. The map centers in Austin TX, and
# displays a tooltip and popup for the selected animal.
#----------------------------------------------------------------------------------
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])

def update_map(viewData, index):  
    
    # ---------- Prevent errors on initial load or empty table ----------
    if viewData is None or len(viewData) == 0:
        return html.Div("No map data available.")
    
    dff = pd.DataFrame.from_dict(viewData)
    
    # ---------- Convert selected row to usable index ----------
    if index is None or len(index) == 0:
        row = 0
    else: 
        row = index[0]
        
    # ---------- Austin TX coordinates -----------
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            # Column 4 defines the breed for the animal
            # Column 9 defines the name of the animal
            dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]], children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,9])
                ])
            ])
        ])
    ]

# Launch as a standalone Flask server so it runs outside of Jupyter
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8050, debug=True)