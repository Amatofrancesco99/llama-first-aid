import dash
import ast
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np

import sys
sys.path.append('src')
from utils import country_translation


# Load dataset (must be switched to a BigQuery load)
df = pd.read_csv("data/sessions_history/sessions_history.csv")

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Set a custom app title
app_title = "Dashboard"  # Customize this title

# Set the custom title and favicon via the index_string
app.index_string = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>llama-first-aid</title>
        <!-- <link rel="icon" href="/assets/favicon.ico" type="image/x-icon"> Link to favicon -->
        {%metas%}
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''


# Get distinct values of 'app_version'
app_versions = [{'label': version, 'value': version} for version in df['app_version'].unique()]
# Add a 'No filter' option as well
app_versions.insert(0, {'label': 'No filter', 'value': 'All'})

# Get distinct values of 'severity'
severities = [{'label': severity, 'value': severity} for severity in df['severity'].unique()]
# Add a 'No filter' option as well
severities.insert(0, {'label': 'No filter', 'value': 'All'})

# Get distinct values of 'medical_classes'
medical_classes = [{'label': medical_class, 'value': medical_class} for medical_class in df['medical_class'].unique()]
# Add a 'No filter' option as well
medical_classes.insert(0, {'label': 'No filter', 'value': 'All'})

# Ensure 'timestamp' column is in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])


##########################################################        USERS PAGE       ##################################################################
# Layout for users Page
users_page = html.Div([
    # Navbar with title, logo, and users link
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Users", href="/")),
            dbc.NavItem(dbc.NavLink("Performance", href="/performance")),  # Performance link
        ],
        brand=app_title,  # This will display the custom title
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4",
    ),

    # Filters - Start and End Date Filters, app_version filter
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Date:', style={'margin-right': '10px', 'display': 'inline-block'}),
                    dcc.DatePickerRange(
                        id='date-picker-range-users',  # Unique ID for users page filter
                        start_date=(df['timestamp'].max() - pd.DateOffset(months=1)).strftime('%Y-%m-%d'),
                        end_date=df['timestamp'].max().strftime('%Y-%m-%d'),
                        display_format='YYYY-MM-DD',
                        style={'width': '100%'}
                    )
                ]),
            ], width=4),
            dbc.Col([  # app_version filter dropdown
                html.Div([
                    html.Label('App:', style={'margin-right': '10px', 'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='app-version-users',
                        options=app_versions,
                        value='All',
                        style={'width': '100%'}
                    )
                ]),
            ], width=4),
            dbc.Col([  # Empty column for alignment
            ], width=4),
        ])
    ], style={'padding': '20px'}),

    # First Row - 3 graphs without filters
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    html.H6("This month's sessions over last month's sessions", style={'textAlign': 'center'}),
                    html.Div(id='graph-1-1-users', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'})
                ]),
                dbc.Row([
                    html.H6("Sessions with location enabled over sessions with location disabled", style={'textAlign': 'center'}),
                    html.Div(id='graph-1-2-users', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'})
                ], style={'padding': '50px'}),
            ], width=4),
            dbc.Col([
                html.H6("Average daily sessions", style={'textAlign': 'center'}),
                html.Div(id='graph-2-users', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'})
            ], width=4),
            dbc.Col([
                html.H6("Daily sessions (trend)", style={'textAlign': 'center'}),
                dcc.Graph(id='graph-3-users'),
            ], width=4)
        ])
    ], style={'padding': '20px'}),

    # Second Row - 3 graphs with filters
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H6("Most frequent medical classes, by severity level", style={'textAlign': 'center'}),
                html.Div([
                    html.Label('Severity:', style={'margin-right': '10px', 'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='graph-4-users-filter',
                        options=severities,
                        value='All',  # Default value
                        style={'width': '50%', 'display': 'inline-block'}
                    )
                ]),
                dcc.Graph(id='graph-4-users'),
            ], width=4),
            dbc.Col([
                html.H6("Most frequent severity levels, by weekday and medical class", style={'textAlign': 'center'}),
                html.Div([
                    html.Label('Medical Class:', style={'margin-right': '10px', 'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='graph-5-users-filter',
                        options=medical_classes,
                        value='All',  # Default value
                        style={'width': '50%', 'display': 'inline-block'}
                    )
                ]),
                dcc.Graph(id='graph-5-users'),
            ], width=4),
            dbc.Col([
                html.H6("Most frequent severity levels, by time range and medical class", style={'textAlign': 'center'}),
                html.Div([
                    html.Label('Medical Class:', style={'margin-right': '10px', 'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='graph-6-users-filter',
                        options=medical_classes,
                        value='All',  # Default value
                        style={'width': '50%', 'display': 'inline-block'}
                    )
                ]),
                dcc.Graph(id='graph-6-users'),
            ], width=4),
        ])
    ], style={'padding': '20px'}),

    # Third Row
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H6("Choropleth map of sessions in time", style={'textAlign': 'center'}),
                dbc.Switch(
                    id='graph-7-users-toggle-button',
                    value=False,  # default state (False is off, True is on)
                    label="Timelapse",  # Optional, you can customize the label here
                    style={'width': '50%'}  # Optional: style for the label text
                ),
                dcc.Graph(id='graph-7-users'),
            ], width='100%'),
        ])
    ], style={'padding': '15px'}),

    # Fourth Row
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H6("Heatmap of worldwide sessions", style={'textAlign': 'center'}),
                dbc.Switch(
                    id='graph-8-users-toggle-button',
                    value=False,  # default state (False is off, True is on)
                    label="Timelapse",  # Optional, you can customize the label here
                    style={'width': '50%'}  # Optional: style for the label text
                ),                  
                html.Label('Severity:', style={'margin-right': '10px', 'display': 'inline-block'}),
                dcc.Dropdown(
                    id='graph-8-users-filter-severity',
                    options=severities,
                    value='All',  # Default value
                    style={'width': '50%'}
                ),
                html.Label('Medical Class:', style={'margin-right': '10px', 'display': 'inline-block'}),
                dcc.Dropdown(
                    id='graph-8-users-filter-medical-class',
                    options=medical_classes,
                    value='All',  # Default value
                    style={'width': '50%'}
                ),
                dcc.Graph(id='graph-8-users'),
            ], width='100%'),
        ])
    ], style={'padding': '15px'}),
])


##########################################################        PERFORMANCE PAGE       ##################################################################
# Layout for performance Page
performance_page = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Users", href="/")),
            dbc.NavItem(dbc.NavLink("Performance", href="/performance")),  # Added Performance link
        ],
        brand=app_title,
        brand_href="/performance",
        color="primary",
        dark=True,
        className="mb-4",
    ),
    
    # Filters Row - Start and End Date Filters, app_version filter
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Date:', style={'margin-right': '10px', 'display': 'inline-block'}),
                    dcc.DatePickerRange(
                        id='date-picker-range-users',  # Unique ID for users page filter
                        start_date=(df['timestamp'].max() - pd.DateOffset(months=1)).strftime('%Y-%m-%d'),
                        end_date=df['timestamp'].max().strftime('%Y-%m-%d'),
                        display_format='YYYY-MM-DD',
                        style={'width': '100%'}
                    )
                ]),
            ], width=4),
            dbc.Col([  # app_version filter dropdown
                html.Div([
                    html.Label('App:', style={'margin-right': '10px', 'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='app-version-users',
                        options=app_versions,
                        value='All',
                        style={'width': '100%'}
                    )
                ]),
            ], width=4),
            dbc.Col([  # Empty column for alignment
            ], width=4),
        ])
    ], style={'padding': '20px'}),

    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    html.H6("Average response time per single interaction", style={'textAlign': 'center'}),
                    html.Div(id='graph-1-1-performance', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'})
                ]),
                dbc.Row([
                    html.H6("Average daily response time", style={'textAlign': 'center'}),
                    html.Div(id='graph-1-2-performance', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'})
                ], style={'padding': '50px'}),
                dbc.Row([
                    html.H6("Average number of interactions per session", style={'textAlign': 'center'}),
                    html.Div(id='graph-1-3-performance', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'})
                ]),
            ], width=4),
            dbc.Col([
                dbc.Row([
                    html.H6("Average time to identify issue", style={'textAlign': 'center'}),
                    html.Div(id='graph-2-1-performance', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'})
                ]),
                dbc.Row([
                    html.H6("Average time to solve issue", style={'textAlign': 'center'}),
                    html.Div(id='graph-2-2-performance', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'})
                ], style={'padding': '50px'}),
                dbc.Row([
                    html.H6("Average time to identify and solve issue", style={'textAlign': 'center'}),
                    html.Div(id='graph-2-3-performance', style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'})
                ]),
            ], width=4),
            dbc.Col([
                html.H6("Average response time, per sessions, per day (trend)", style={'textAlign': 'center'}),
                dcc.Graph(id='graph-3-performance'),
            ], width=4)
        ])
    ], style={'padding': '20px'}),

])

# Set up routing for pages (users and performance)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Define page content based on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/performance':
        return performance_page
    else:  # users page or any other invalid URL will show users
        return users_page


##########################################################        USERS PAGE       ##################################################################
@app.callback(
    [
        Output('graph-1-1-users', 'children'),
        Output('graph-1-1-users', 'style'),
        Output('graph-1-2-users', 'children'),
        Output('graph-1-2-users', 'style'),
        Output('graph-2-users', 'children'),
        Output('graph-3-users', 'figure'),
        Output('graph-4-users', 'figure'),
        Output('graph-5-users', 'figure'),
        Output('graph-6-users', 'figure'),
        Output('graph-7-users', 'figure'),
        Output('graph-8-users', 'figure')
    ],
    [
        Input('date-picker-range-users', 'start_date'),
        Input('date-picker-range-users', 'end_date'),
        Input('app-version-users', 'value'), 
        Input('graph-4-users-filter', 'value'),
        Input('graph-5-users-filter', 'value'),
        Input('graph-6-users-filter', 'value'),
        Input('graph-7-users-toggle-button', 'value'),
        Input('graph-8-users-toggle-button', 'value'),
        Input('graph-8-users-filter-severity', 'value'),
        Input('graph-8-users-filter-medical-class', 'value')
    ]
)
def update_graphs(start_date, end_date, app_version, graph_4_severity_level, graph_5_medical_class, graph_6_medical_class, graph_7_toggle_button, graph_8_toggle_button,
                graph_8_severity_level, graph_8_medical_class):
    # Filter the data based on the selected date range and app_version filter
    start_date = pd.to_datetime(start_date).date()  # Convert to date
    end_date = pd.to_datetime(end_date).date()  # Convert to date

    # Filter the dataframe based on the date range
    filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]
    
    if app_version != 'All':  # Check if app_version is not the empty string
        filtered_df = filtered_df[filtered_df['app_version'] == app_version]  # Apply the app_version filter


    ## FIRST PLOT - 1
    # Calculate session count for current and last month
    current_month_sessions = filtered_df[filtered_df['timestamp'].dt.month == pd.to_datetime(end_date).month]['session_id'].nunique()
    last_month_sessions = filtered_df[filtered_df['timestamp'].dt.month == (pd.to_datetime(end_date).month - 1)]['session_id'].nunique()

    # Calculate the percentage change (if last_month_sessions > 0)
    if last_month_sessions > 0:
        percentage_change_1 = (current_month_sessions / last_month_sessions) * 100
    else:
        percentage_change_1 = '-'  # If no sessions last month, assume no change

    # Determine color based on percentage change
    color_1 = 'black'
    if percentage_change_1 != '-':
        if percentage_change_1 >= 100:
            color_1 = 'green'
        elif percentage_change_1 >= 0 and percentage_change_1 < 100:
            color_1 = 'red'
    
    # Style for the percentage text (color)
    text_style_1 = {
        'fontSize': 24,
        'fontWeight': 'bold',
        'textAlign': 'center',
        'color': color_1  # Apply dynamic color
    }

    ## FIRST PLOT - 2
    sessions_location_enabled = filtered_df[filtered_df['location'] != "[None, None]"]['session_id'].nunique()
    sessions_location_disabled = filtered_df[filtered_df['location'] == "[None, None]"]['session_id'].nunique()

    if sessions_location_disabled > 0:
        percentage_change_2 = (sessions_location_enabled / sessions_location_disabled) * 100
    else:
        percentage_change_2 = '-'

    color_2 = 'green'
    if percentage_change_2 != '-':
        if percentage_change_2 >= 100.0:
            color_2 = 'green'
        elif percentage_change_2 >= 0 and percentage_change_2 < 100:
            color_2 = 'red'

    # Style for the percentage text (color)
    text_style_2 = {
        'fontSize': 24,
        'fontWeight': 'bold',
        'textAlign': 'center',
        'color': color_2  # Apply dynamic color
    }

    ## SECOND PLOT
    average_sessions_per_day = '-' if len(filtered_df) == 0 else filtered_df['session_id'].nunique() / (((end_date - start_date).days) + 1)


    ## THIRD PLOT
    # Generate a list of all dates between start_date and end_date
    date_range = pd.date_range(start=start_date, end=end_date)

    # Group the sessions by date and count the number of sessions per day
    sessions_per_day = filtered_df.groupby(filtered_df['timestamp'].dt.date).size().reindex(date_range.date, fill_value=0)

    # Create a DataFrame for the sessions per day to plot with plotly.express
    sessions_df = pd.DataFrame({
        'date': sessions_per_day.index,
        'sessions': sessions_per_day.values
    })

    # Create the initial line graph using plotly express
    sessions_line_graph = px.line(
        sessions_df, 
        x='date', 
        y='sessions'
    )

    # Add scatter trace for bullet points where sessions > 0
    non_zero_sessions = sessions_df[sessions_df['sessions'] > 0]

    # Overlay bullet points on the line graph
    sessions_line_graph.add_traces(
        go.Scatter(
            x=non_zero_sessions['date'],
            y=non_zero_sessions['sessions'],
            mode='markers',
            marker=dict(size=6, symbol='circle', color='rgb(50, 50, 50)'),  # Small bullet points
            name=None
        )
    )

    # Customize the layout for transparent background
    sessions_line_graph.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the entire figure
        title_font=dict(size=14, family="Arial, sans-serif", color='rgb(50, 50, 50)', weight='bold'),
        xaxis=dict(
            title='Date',
            title_font=dict(size=12, family="Arial, sans-serif", color='rgb(50, 50, 50)'),
            tickfont=dict(size=10, family="Arial, sans-serif", color='rgb(100, 100, 100)'),
            showgrid=False,  # Hide gridlines
            gridcolor='rgb(200, 200, 200)',  # Light gridlines
            gridwidth=0.5,
            zeroline=True,  # Line at y=0
            zerolinecolor='rgb(200, 200, 200)',
            zerolinewidth=1
        ),
        yaxis=dict(
            title='Number of Sessions',
            title_font=dict(size=12, family="Arial, sans-serif", color='rgb(50, 50, 50)'),
            tickfont=dict(size=10, family="Arial, sans-serif", color='rgb(100, 100, 100)'),
            showgrid=True,
            gridcolor='rgb(200, 200, 200)',
            gridwidth=0.5,
            zeroline=True,
            zerolinecolor='rgb(200, 200, 200)',
            zerolinewidth=1
        ),
        margin=dict(l=10, r=10, t=10, b=30),
        showlegend=False
    )


    ## FOURTH PLOT
    # Group the data by 'medical_class' and count the sessions per class
    # Filter data based on severity level
    if graph_4_severity_level != 'All':
        medical_class_df = filtered_df[filtered_df['severity'] == graph_4_severity_level]
    else:
        medical_class_df = filtered_df  # No severity filter applied

    medical_class_sessions = medical_class_df.groupby('medical_class')['session_id'].nunique()

    total_sessions = medical_class_df['session_id'].nunique()

    medical_class_percentage = (medical_class_sessions / total_sessions) * 100

    medical_class_df = pd.DataFrame({
        'medical_class': medical_class_percentage.index,
        'percentage': medical_class_percentage.values
    }).reset_index(drop=True)

    medical_class_df.sort_values(by='percentage', ascending=False).head(5)

    medical_class_bar_chart = px.bar(
        medical_class_df,
        x='medical_class',
        y='percentage',
    )

    medical_class_bar_chart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the entire figure
        title_font=dict(size=24, family="Arial, sans-serif", color='rgb(50, 50, 50)', weight='bold'),
        xaxis=dict(
            title='Medical Class',
            title_font=dict(size=12, family="Arial, sans-serif", color='rgb(50, 50, 50)'),
            tickfont=dict(size=10, family="Arial, sans-serif", color='rgb(100, 100, 100)'),
            gridcolor='rgb(200, 200, 200)',
            gridwidth=0.5,
        ),
        yaxis=dict(
            title='% Sessions',
            title_font=dict(size=12, family="Arial, sans-serif", color='rgb(50, 50, 50)'),
            tickfont=dict(size=10, family="Arial, sans-serif", color='rgb(100, 100, 100)'),
            showgrid=True,
            gridcolor='rgb(200, 200, 200)',
            gridwidth=0.5,
        ),
        margin=dict(l=10, r=10, t=10, b=30),
        showlegend=False
    )


    ## FIFTH PLOT
    if graph_5_medical_class != 'All':
        composition_df = filtered_df[filtered_df['medical_class'] == graph_5_medical_class]
    else:
        composition_df = filtered_df  # No severity filter applied

    composition_df_not_na = composition_df[composition_df['severity'].notna()]  # Remove rows where severity is None

    # --- Calculate the percentage of sessions for each severity level per weekday ---
    composition_df_not_na['weekday'] = composition_df_not_na['timestamp'].dt.day_name()  # Get weekday names
    severity_weekday_counts = composition_df_not_na.groupby(['weekday', 'severity']).size().reset_index(name='session_count')

    # Calculate the total sessions per weekday
    total_sessions_per_weekday = composition_df_not_na.groupby('weekday').size().reset_index(name='total_sessions')

    # Merge the session counts with the total sessions per weekday
    severity_weekday_counts = severity_weekday_counts.merge(total_sessions_per_weekday, on='weekday')

    # Calculate the percentage of sessions for each severity level
    severity_weekday_counts['percentage'] = (severity_weekday_counts['session_count'] / severity_weekday_counts['total_sessions']) * 100

    # Sort the weekdays to maintain the order (Monday, Tuesday, etc.)
    weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    severity_weekday_counts['weekday'] = pd.Categorical(severity_weekday_counts['weekday'], categories=weekdays_order, ordered=True)
    severity_weekday_counts = severity_weekday_counts.sort_values('weekday')

    # --- Ensure that all weekdays are included, even those with no data ---
    all_weekdays = pd.DataFrame({'weekday': weekdays_order})
    all_severity_levels = composition_df_not_na['severity'].unique()

    # Create all combinations of weekdays and severity levels
    all_combinations = pd.MultiIndex.from_product([all_weekdays['weekday'], all_severity_levels], names=['weekday', 'severity']).to_frame(index=False)

    # Merge with the original data to include weekdays with no sessions
    severity_weekday_counts_full = all_combinations.merge(severity_weekday_counts, on=['weekday', 'severity'], how='left').fillna(0)

    # Calculate the percentage for the missing data (if any)
    total_sessions_per_weekday_full = severity_weekday_counts_full.groupby('weekday')['session_count'].transform('sum')
    severity_weekday_counts_full['percentage'] = (severity_weekday_counts_full['session_count'] / total_sessions_per_weekday_full) * 100

    # --- Define the custom color scale ---
    color_scale = {
        '1': 'white',
        '2': 'green',
        '3': 'orange',
        '4': 'darkorange',
        '5': 'red'
    }

    # Ensure the 'severity' column is treated as a string for correct mapping
    severity_weekday_counts_full['severity'] = severity_weekday_counts_full['severity'].astype(str)

    # --- Create the stacked bar chart ---
    composition_graph = px.bar(
        severity_weekday_counts_full,
        x='weekday',
        y='percentage',
        color='severity',
        color_discrete_map=color_scale,  # Custom color scale
        category_orders={'weekday': weekdays_order}  # Order weekdays properly
    )

    composition_graph.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the entire figure
        title_font=dict(size=24, family="Arial, sans-serif", color='rgb(50, 50, 50)', weight='bold'),
        xaxis=dict(
            title='Weekday',
            title_font=dict(size=12, family="Arial, sans-serif", color='rgb(50, 50, 50)'),
            tickfont=dict(size=10, family="Arial, sans-serif", color='rgb(100, 100, 100)'),
            gridcolor='rgb(200, 200, 200)',
            gridwidth=0.5,
        ),
        yaxis=dict(
            title='% Sessions',
            title_font=dict(size=12, family="Arial, sans-serif", color='rgb(50, 50, 50)'),
            tickfont=dict(size=10, family="Arial, sans-serif", color='rgb(100, 100, 100)'),
            showgrid=True,
            gridcolor='rgb(200, 200, 200)',
            gridwidth=0.5,
        ),
        margin=dict(l=10, r=10, t=10, b=30),
        showlegend=True
    )



    ## SIXTH PLOT
    if graph_6_medical_class != 'All':
        composition_df_2 = filtered_df[filtered_df['medical_class'] == graph_6_medical_class]
    else:
        composition_df_2 = filtered_df  # No medical class filter applied

    composition_df_2_not_na = composition_df_2[composition_df_2['severity'].notna()]  # Remove rows where severity is None

    # --- Create a new column for hour ranges ---
    def get_hour_range(hour):
        if 0 <= hour <= 4:
            return '0-4'
        elif 5 <= hour <= 9:
            return '5-9'
        elif 10 <= hour <= 14:
            return '10-14'
        elif 15 <= hour <= 19:
            return '15-19'
        elif 20 <= hour <= 23:
            return '20-23'
        return 'Unknown'

    # Apply the function to the 'timestamp' column to create the 'hour_range' column
    composition_df_2_not_na['hour_range'] = composition_df_2_not_na['timestamp'].dt.hour.apply(get_hour_range)

    # --- Calculate the percentage of sessions for each severity level per hour range ---
    severity_hour_range_counts = composition_df_2_not_na.groupby(['hour_range', 'severity']).size().reset_index(name='session_count')

    # Calculate the total sessions per hour range
    total_sessions_per_hour_range = composition_df_2_not_na.groupby('hour_range').size().reset_index(name='total_sessions')

    # Merge the session counts with the total sessions per hour range
    severity_hour_range_counts = severity_hour_range_counts.merge(total_sessions_per_hour_range, on='hour_range')

    # Calculate the percentage of sessions for each severity level
    severity_hour_range_counts['percentage'] = (severity_hour_range_counts['session_count'] / severity_hour_range_counts['total_sessions']) * 100

    # Sort the hour ranges to maintain the order (0-4, 5-9, etc.)
    hour_range_order = ['0-4', '5-9', '10-14', '15-19', '20-23']
    severity_hour_range_counts['hour_range'] = pd.Categorical(severity_hour_range_counts['hour_range'], categories=hour_range_order, ordered=True)

    # Ensure all hour ranges are present, even those with 0% sessions
    # Create a DataFrame with all possible hour ranges and severity levels
    all_hour_ranges = pd.DataFrame({'hour_range': hour_range_order})
    all_severity_levels = composition_df_2_not_na['severity'].unique()

    # Create a DataFrame for all combinations of hour_range and severity (even if no sessions)
    all_combinations = pd.MultiIndex.from_product([all_hour_ranges['hour_range'], all_severity_levels], names=['hour_range', 'severity']).to_frame(index=False)

    # Merge with the original data to ensure all combinations are represented
    severity_hour_range_counts_full = all_combinations.merge(severity_hour_range_counts, on=['hour_range', 'severity'], how='left').fillna(0)

    # Calculate percentage for missing data (if any)
    total_sessions_per_hour_range_full = severity_hour_range_counts_full.groupby('hour_range')['session_count'].transform('sum')
    severity_hour_range_counts_full['percentage'] = (severity_hour_range_counts_full['session_count'] / total_sessions_per_hour_range_full) * 100

    # Ensure the 'severity' column is treated as a string for correct mapping
    severity_hour_range_counts_full['severity'] = severity_hour_range_counts_full['severity'].astype(str)

    # --- Force the severity to follow a consistent order across all hour ranges ---
    severity_order = ['5', '4', '3', '2', '1']  # Severity 5 at the top, severity 1 at the bottom
    severity_hour_range_counts_full['severity'] = pd.Categorical(severity_hour_range_counts_full['severity'], categories=severity_order, ordered=True)

    # --- Create the stacked bar chart ---
    composition_graph_2 = px.bar(
        severity_hour_range_counts_full,
        x='hour_range',
        y='percentage',
        color='severity',
        color_discrete_map=color_scale,  # Apply the custom color scale
        category_orders={'hour_range': hour_range_order}  # Order hour ranges properly
    )

    composition_graph_2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the entire figure
        title_font=dict(size=24, family="Arial, sans-serif", color='rgb(50, 50, 50)', weight='bold'),
        xaxis=dict(
            title='Time Range',
            title_font=dict(size=12, family="Arial, sans-serif", color='rgb(50, 50, 50)'),
            tickfont=dict(size=10, family="Arial, sans-serif", color='rgb(100, 100, 100)'),
            gridcolor='rgb(200, 200, 200)',
            gridwidth=0.5,
        ),
        yaxis=dict(
            title='% Sessions',
            title_font=dict(size=12, family="Arial, sans-serif", color='rgb(50, 50, 50)'),
            tickfont=dict(size=10, family="Arial, sans-serif", color='rgb(100, 100, 100)'),
            showgrid=True,
            gridcolor='rgb(200, 200, 200)',
            gridwidth=0.5,
        ),
        margin=dict(l=10, r=10, t=10, b=30),
        showlegend=True
    )


    # SEVENTH PLOT
    # Prepare the data
    if graph_7_toggle_button == False:
        coordinates_df = filtered_df[['country', 'session_id']]  # Adjust as necessary
        coordinates_df = coordinates_df[coordinates_df['country'] != None]
        coordinates_df['country'] = coordinates_df['country'].replace(country_translation)

        # Group by country and sum the sessions
        country_sessions = coordinates_df.groupby('country')['session_id'].nunique().reset_index()

        # Create a choropleth map with a custom color scale
        choropleth_map = px.choropleth(country_sessions,
                                        locations='country',
                                        locationmode='country names',
                                        color='session_id',
                                        hover_name='country',
                                        color_continuous_scale=["#d1e9d3", "#4caf50"])

        # Update layout for a more beautiful map
        choropleth_map.update_layout(
            coloraxis_colorbar_title="Sessions",
            coloraxis_colorbar_x=0,  # Position the color bar to the left
            coloraxis_colorbar_xpad=10,  # Optional padding from the map
            coloraxis_colorbar_ypad=10,  # Optional padding from the map
            geo=dict(
                projection_type="natural earth",  # Using a more beautiful map projection (Natural Earth)
                showcoastlines=True,  # Display coastlines
                coastlinecolor="gray",  # Set coastline color to gray for subtlety
                showland=True,  # Show land areas
                landcolor="whitesmoke",  # Set land color to a soft grayish white
                subunitcolor="gray",  # Subunit color for borders
                showlakes=True,  # Display lakes
                lakecolor="lightblue",  # Color of lakes for better visual contrast
            ),
            title_x=0.5,  # Center the title horizontally
            title_font=dict(
                size=24,  # Title font size
                family="Arial, sans-serif",  # Title font family
                color="black"  # Title font color
            ),
            margin={"r": 0, "t": 50, "l": 0, "b": 0},  # Adjust margins for better padding
            font=dict(
                family="Arial, sans-serif",  # Font family for labels and hover info
                size=14,  # Font size
                color="black"  # Font color
            ),
        )
    else:
        # Assuming filtered_df already has 'timestamp' column
        coordinates_df = filtered_df[['country', 'session_id', 'timestamp']]  # Keep country, session_id, and timestamp
        coordinates_df = coordinates_df[coordinates_df['country'] != None]
        coordinates_df['country'] = coordinates_df['country'].replace(country_translation)

        # Remove minutes and downcast to the nearest hour
        coordinates_df['timestamp'] = coordinates_df['timestamp'].dt.floor('H')  # Floor to the nearest hour (remove minutes and seconds)

        # Create a 'date_hour' column by extracting the date and hour (without minutes and seconds)
        coordinates_df['date_hour'] = coordinates_df['timestamp'].dt.strftime('%Y-%m-%d %H')  # Format as 'YYYY-MM-DD HH'

        # Convert 'date_hour' back to a datetime object for proper sorting and aggregation
        coordinates_df['date_hour'] = pd.to_datetime(coordinates_df['date_hour'], format='%Y-%m-%d %H')

        # Sort the data by 'date_hour' to ensure correct chronological order
        coordinates_df = coordinates_df.sort_values('date_hour')

        # Group by country and date_hour, then count the unique sessions
        country_sessions = coordinates_df.groupby(['country', 'date_hour']).agg({'session_id': 'nunique'}).reset_index()

        # Ensure 'date_hour' is sorted chronologically
        country_sessions['date_hour'] = pd.to_datetime(country_sessions['date_hour'], format='%Y-%m-%d %H')

        # Sort the grouped data explicitly by 'date_hour' to ensure correct ordering
        country_sessions = country_sessions.sort_values('date_hour')

        # Create the animated choropleth map
        choropleth_map = px.choropleth(country_sessions,
                                        locations='country',
                                        locationmode='country names',
                                        color='session_id',
                                        hover_name='country',
                                        animation_frame='date_hour',  # Animate by the sorted 'date_hour'
                                        color_continuous_scale=["#d1e9d3", "#4caf50"])

        # Update layout for the map appearance
        choropleth_map.update_layout(
            coloraxis_colorbar_title="Sessions",
            coloraxis_colorbar_x=0,  # Position the color bar to the left
            coloraxis_colorbar_xpad=10,
            coloraxis_colorbar_ypad=10,
            geo=dict(
                projection_type="natural earth",
                showcoastlines=True,
                coastlinecolor="gray",
                showland=True,
                landcolor="whitesmoke",
                subunitcolor="gray",
                showlakes=True,
                lakecolor="lightblue",
            ),
            title_x=0.5,
            title_font=dict(
                size=24,
                family="Arial, sans-serif",
                color="black"
            ),
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            font=dict(
                family="Arial, sans-serif",
                size=14,
                color="black"
            ),
            # Add autoplay and pause buttons, positioned in the center
            updatemenus=[
                {
                    'buttons': [
                        {
                            'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                            'label': 'Play',
                            'method': 'animate',
                        },
                        {
                            'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                            'label': 'Pause',
                            'method': 'animate',
                        }
                    ],
                    'direction': 'left',
                    'pad': {'r': 10, 't': 87},
                    'showactive': False,
                    'type': 'buttons',
                    'x': 0.5,  # Center the play/pause buttons horizontally
                    'xanchor': 'center',  # Center the buttons horizontally
                    'y': -0.12,  # Position the buttons just above the slider (reduced space)
                    'yanchor': 'top',
                }
            ],
            sliders=[{
                'currentvalue': {
                    'visible': False,  # Hide the date_hour label on top of the slider
                },
                'pad': {"t": 0},  # Remove the gap between the map and the slider
                'len': 0.8,  # Reduce the size of the slider (make it 80% of the total width)
                'x': 0.5,  # Center the slider horizontally
                'xanchor': 'center',  # Center the slider horizontally
                'y': -0.2  # Position the slider just below the buttons (reduced space)
            }]
        )


    # EIGHTH PLOT
    # Replace native country names with their English equivalents
    if graph_8_toggle_button == False:
        if graph_8_severity_level != 'All':
            filtered_df = filtered_df[filtered_df['severity'] == graph_8_severity_level]
    
        if graph_8_medical_class != 'All':
            filtered_df = filtered_df[filtered_df['medical_class'] == graph_8_medical_class]

        hm_df = filtered_df[['location', 'session_id']]  # Ensure this contains lat, long, and session_id
        hm_df = filtered_df[filtered_df['location'] != "[None, None]"]
        hm_df['latitude'] = hm_df['location'].apply(lambda x: eval(x)[0])
        hm_df['longitude'] = hm_df['location'].apply(lambda x: eval(x)[1])

        # Group by latitude and longitude, summing the sessions
        coordinates_sessions = hm_df.groupby(['latitude', 'longitude'])['session_id'].nunique().reset_index()

        # Create a heatmap using scatter_mapbox
        heatmap_map = px.scatter_mapbox(
            coordinates_sessions,
            lat="latitude",
            lon="longitude",
            size="session_id",  # The size of the points is determined by the session count
            color="session_id",  # The color of the points is also based on the session count
            hover_name="session_id",  # Display session count on hover
            color_continuous_scale=["#ffcccc", "#990000"],  # Color scale from light red to dark red
            labels={'session_id': 'Sessions'},
            size_max=8,  # Reduced maximum bubble size
        )

        # Update layout to make the heatmap visually beautiful with reduced bubble sizes
        heatmap_map.update_layout(
            mapbox_style="carto-positron",  # Map style; you can use "stamen-terrain" or others
            mapbox_zoom=2,  # Set default zoom level for Europe (zoom level 4 works well)
            mapbox_center={"lat": 50, "lon": 10},  # Center the map on Europe (roughly lat=50, lon=10)
            title_x=0.5,  # Center the title horizontally
            title_font=dict(
                size=24,  # Title font size
                family="Arial, sans-serif",  # Title font family
                color="black"  # Title font color
            ),
            coloraxis_colorbar_title="Sessions",  # Title for the color scale
            font=dict(
                family="Arial, sans-serif",  # Font family for labels and hover info
                size=14,  # Font size
                color="black"  # Font color
            ),
            mapbox=dict(
                style="carto-positron",  # Style of the map background (clean white background)
            ),
            autosize=True,  # Automatically adjust size based on the data
        )
    else:
        if graph_8_severity_level != 'All':
            filtered_df = filtered_df[filtered_df['severity'] == graph_8_severity_level]
    
        if graph_8_medical_class != 'All':
            filtered_df = filtered_df[filtered_df['medical_class'] == graph_8_medical_class]
            
        # Assuming filtered_df already has 'timestamp' and 'location' columns
        hm_df = filtered_df[['location', 'session_id', 'timestamp']]  # Ensure this contains lat, long, session_id, and timestamp
        hm_df = filtered_df[filtered_df['location'] != "[None, None]"]

        # Convert location to latitude and longitude
        hm_df['latitude'] = hm_df['location'].apply(lambda x: eval(x)[0])
        hm_df['longitude'] = hm_df['location'].apply(lambda x: eval(x)[1])

        # Create a 'date_hour' column by extracting the date and hour from the timestamp
        hm_df['date_hour'] = hm_df['timestamp'].dt.strftime('%Y-%m-%d %H')  # Format as 'YYYY-MM-DD HH'

        # Convert 'date_hour' back to datetime for proper sorting and grouping
        hm_df['date_hour'] = pd.to_datetime(hm_df['date_hour'], format='%Y-%m-%d %H')

        # Sort the data by 'date_hour' to ensure correct chronological order
        hm_df = hm_df.sort_values('date_hour')

        # Group by latitude, longitude, and date_hour, then count the unique sessions
        coordinates_sessions = hm_df.groupby(['latitude', 'longitude', 'date_hour'])['session_id'].nunique().reset_index()

        # Ensure 'date_hour' is sorted chronologically
        coordinates_sessions['date_hour'] = pd.to_datetime(coordinates_sessions['date_hour'], format='%Y-%m-%d %H')

        # Sort the grouped data explicitly by 'date_hour' to ensure correct ordering
        coordinates_sessions = coordinates_sessions.sort_values('date_hour')

        # Create the animated heatmap using scatter_mapbox
        heatmap_map = px.scatter_mapbox(
            coordinates_sessions,
            lat="latitude",
            lon="longitude",
            size="session_id",  # The size of the points is determined by the session count
            color="session_id",  # The color of the points is also based on the session count
            hover_name="session_id",  # Display session count on hover
            color_continuous_scale=["#ffcccc", "#990000"],  # Color scale from light red to dark red
            labels={'session_id': 'Sessions'},
            size_max=8,  # Reduced maximum bubble size
            animation_frame="date_hour",  # Animate by 'date_hour'
        )

        # Update layout for the heatmap appearance
        heatmap_map.update_layout(
            mapbox_style="carto-positron",  # Map style; you can use "stamen-terrain" or others
            mapbox_zoom=2,  # Set default zoom level for Europe (zoom level 4 works well)
            mapbox_center={"lat": 50, "lon": 10},  # Center the map on Europe (roughly lat=50, lon=10)
            title_x=0.5,  # Center the title horizontally
            title_font=dict(
                size=24,  # Title font size
                family="Arial, sans-serif",  # Title font family
                color="black"  # Title font color
            ),
            coloraxis_colorbar_title="Sessions",  # Title for the color scale
            font=dict(
                family="Arial, sans-serif",  # Font family for labels and hover info
                size=14,  # Font size
                color="black"  # Font color
            ),
            mapbox=dict(
                style="carto-positron",  # Style of the map background (clean white background)
            ),
            autosize=True,  # Automatically adjust size based on the data
            updatemenus=[
                {
                    'buttons': [
                        {
                            'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                            'label': 'Play',
                            'method': 'animate',
                        },
                        {
                            'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                            'label': 'Pause',
                            'method': 'animate',
                        }
                    ],
                    'direction': 'left',
                    'pad': {'r': 10, 't': 87},
                    'showactive': False,
                    'type': 'buttons',
                    'x': 0.5,  # Center the play/pause buttons horizontally
                    'xanchor': 'center',  # Center the buttons horizontally
                    'y': -0.12,  # Position the buttons just above the slider (reduced space)
                    'yanchor': 'top',
                }
            ],
            sliders=[{
                'currentvalue': {
                    'visible': False,  # Hide the date_hour label on top of the slider
                },
                'pad': {"t": 0},  # Remove the gap between the map and the slider
                'len': 0.8,  # Reduce the size of the slider (make it 80% of the total width)
                'x': 0.5,  # Center the slider horizontally
                'xanchor': 'center',  # Center the slider horizontally
                'y': -0.2  # Position the slider just below the buttons (reduced space)
            }]
        )


    # --- Return the figures for all graphs ---
    return (
        ('No sessions in last month' if percentage_change_1 == '-' else [f"{percentage_change_1:.2f}%"]), 
        text_style_1, 
        ('No sessions with location disabled' if percentage_change_2 == '-' else [f"{percentage_change_2:.2f}%"]), 
        text_style_2, 
        ('Not enough days' if average_sessions_per_day == '-' else [f"{average_sessions_per_day:.2f}"]),
        sessions_line_graph,  # Line graph for sessions per day
        medical_class_bar_chart,  # Bar chart for medical class percentages
        composition_graph,  # Bar chart for weekday and severity composition
        composition_graph_2,  # Bar chart for hour range and severity composition
        choropleth_map,  # Choropleth map for sessions by country
        heatmap_map,  # Heatmap for sessions by country
    )




##########################################################        PERFORMANCE PAGE       ##################################################################
@app.callback(
    [
        Output('graph-1-1-performance', 'children'),
        Output('graph-1-2-performance', 'children'),
        Output('graph-1-3-performance', 'children'),
    ],
    [
        Input('date-picker-range-users', 'start_date'),
        Input('date-picker-range-users', 'end_date'),
        Input('app-version-users', 'value')
    ]
)
def update_performance_graphs(start_date, end_date, app_version):
    # Filter the data based on the selected date range and app_version filter
    start_date = pd.to_datetime(start_date).date()  # Convert to date
    end_date = pd.to_datetime(end_date).date()  # Convert to date

    # Filter the dataframe based on the date range
    filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]
    
    if app_version != 'All':  # Check if app_version is not the empty string
        filtered_df = filtered_df[filtered_df['app_version'] == app_version]  # Apply the app_version filter

    # Ensure response_times is a list of numbers
    filtered_df['response_times'] = filtered_df['response_times'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    
    ## FIRST PLOT - 1
    # 1.1
    # Flatten the 'response_times' column into a single list of all times
    all_response_times = [time for sublist in filtered_df['response_times'] for time in sublist]
    
    # Calculate the average response time from the flattened list
    average_response_time = np.mean(all_response_times)

    # 1.2
    # Group by the date part of the timestamp
    filtered_df['date'] = filtered_df['timestamp'].dt.date

    # List to hold daily average response times
    daily_avg_response_times = []

    # Loop through each group (day)
    for date, group in filtered_df.groupby('date'):
        # Flatten response times for each session in that day
        daily_response_times = [time for sublist in group['response_times'] for time in sublist]

        # Calculate the average response time for that day
        if daily_response_times:  # Check if there are any response times for that day
            daily_avg_response_times.append(np.mean(daily_response_times))

    # Calculate the overall average response time
    overall_daily_average_response_time = np.mean(daily_avg_response_times) if daily_avg_response_times else 0

    # 1.3
    # Calculate the length of 'response_times' for each session
    filtered_df['response_times_len'] = filtered_df['response_times'].apply(len)

    # Calculate the overall average response time length
    overall_avg_response_times_len = filtered_df['response_times_len'].mean()

    
    # --- Return the figures for all graphs ---
    return (
        [str(round(average_response_time, 2))+ "s"],
        [str(round(overall_daily_average_response_time, 2))+ "s"],
        [str(round(overall_avg_response_times_len, 2))]
    )



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
