import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load CSV data into a DataFrame
df = pd.read_csv('speedtest_results.csv', parse_dates=['Timestamp'], on_bad_lines='skip')

# Styling
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Function to update charts and table
def update_data():
    # Reload CSV data into a DataFrame
    global df
    df = pd.read_csv('speedtest_results.csv', parse_dates=['Timestamp'], on_bad_lines='skip')

    # Get unique interface names from the DataFrame
    interface_names = df['Interface'].unique()

    # Custom colors for each interface
    custom_colors = ['blue', 'orange', 'red', 'purple']

    # Filter data for all available interfaces
    subset_df = df[df['Interface'].isin(interface_names)]

    # Create line charts with a custom color map
    download_chart = px.line(subset_df, x='Timestamp', y='Download', color='Interface', title='Download Speed',
                             labels={'Interface': 'Interface - ISP'}, line_group='ISP',
                             color_discrete_map=dict(zip(interface_names, custom_colors)))
    upload_chart = px.line(subset_df, x='Timestamp', y='Upload', color='Interface', title='Upload Speed',
                           labels={'Interface': 'Interface - ISP'}, line_group='ISP',
                           color_discrete_map=dict(zip(interface_names, custom_colors)))
    latency_chart = px.line(subset_df, x='Timestamp', y='Latency', color='Interface', title='Latency',
                            labels={'Interface': 'Interface - ISP'}, line_group='ISP',
                            color_discrete_map=dict(zip(interface_names, custom_colors)))

    # Update legend names
    for chart in [download_chart, upload_chart, latency_chart]:
        for i in range(len(chart.data)):
            interface = chart.data[i]['name']
            isp = subset_df[subset_df['Interface'] == interface]['ISP'].iloc[0]
            chart.data[i]['name'] = f"{interface} - {isp}"

    # Create average table
    average_data = {'Metric': ['Average Download', 'Average Upload', 'Average Latency']}
    isp_labels = {}

    for interface in interface_names:
        average_data[interface] = [
            subset_df[subset_df['Interface'] == interface]['Download'].mean(),
            subset_df[subset_df['Interface'] == interface]['Upload'].mean(),
            subset_df[subset_df['Interface'] == interface]['Latency'].mean()
        ]
        isp_labels[interface] = df[df['Interface'] == interface]['ISP'].iloc[0]

    average_table = [html.Tr([html.Th('Metric')] + [html.Th(f'{interface} - {isp_labels[interface]}') for interface in interface_names])]
    for i in range(len(average_data['Metric'])):
        row = [html.Td(average_data['Metric'][i])]
        row += [html.Td(average_data[interface][i]) for interface in interface_names]
        average_table.append(html.Tr(row))

    return download_chart, upload_chart, latency_chart, average_table

# Define the layout of the dashboard
app.layout = html.Div(style={'backgroundColor': '#f2f2f2', 'padding': '20px'}, children=[
    html.H1("Talketna Network Speed Dashboard", style={'color': '#333'}),

    # Line chart for download speed
    dcc.Graph(id='download-chart', style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '10px'}),

    # Line chart for upload speed
    dcc.Graph(id='upload-chart', style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '10px'}),

    # Line chart for latency
    dcc.Graph(id='latency-chart', style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '10px'}),

    # Table for average values
    html.Table(id='average-table', style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '10px'}),

    # Interval component to trigger updates
    dcc.Interval(
        id='interval-component',
        interval=1 * 60 * 1000,  # Update every 1 minute
        n_intervals=0
    ),
])

# Callback to update charts and table when data is appended
@app.callback(
    [Output('download-chart', 'figure'),
     Output('upload-chart', 'figure'),
     Output('latency-chart', 'figure'),
     Output('average-table', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_charts_and_table(n_intervals):
    return update_data()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)