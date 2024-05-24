from flask import Flask, render_template, request
import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
from folium.plugins import HeatMap
import warnings

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

csv_file_path = 'master_final.csv'

@app.route('/heat-map-view')
def heat_map():
    df = pd.read_csv(csv_file_path)

    # Check if DataFrame is empty
    if df.empty:
        return "No data available"

    # Create a folium map centered at an average location
    m = folium.Map(location=[df['decimalLatitude'].mean(), df['decimalLongitude'].mean()], zoom_start=5)

    # Prepare data for heat map
    heat_data = df[['decimalLatitude', 'decimalLongitude']].dropna().values.tolist()

    # Add heat map layer
    HeatMap(heat_data).add_to(m)

    return m._repr_html_()

@app.route('/map-view')
def index():
    try:
        # Filter out specific warnings if necessary
        warnings.filterwarnings("ignore", category=UserWarning, module='folium')

        df = pd.read_csv(csv_file_path)
        print(df.head())  # Debug: print the first few rows of the DataFrame

        # Check if DataFrame is empty
        if df.empty:
            return "No data available"

        # Ensure eventDate is parsed correctly and remove timezone information
        df['eventDate'] = pd.to_datetime(df['eventDate'], errors='coerce')
        df = df.dropna(subset=['eventDate'])  # Drop rows with invalid dates

        # Remove timezone information
        df['eventDate'] = df['eventDate'].dt.tz_localize(None)
        df.sort_values('eventDate', inplace=True)

        # Group data by date
        grouped = df.groupby(df['eventDate'].dt.date)

        heat_data = []
        time_index = []

        for date, group in grouped:
            heat_data.append(group[['decimalLatitude', 'decimalLongitude']].values.tolist())
            time_index.append(date.strftime('%Y-%m-%d'))

        # Create the map centered at an average location
        m = folium.Map(location=[df['decimalLatitude'].mean(), df['decimalLongitude'].mean()], zoom_start=5)

        # Add HeatMapWithTime to the map with the oldest date as the start date
        HeatMapWithTime(data=heat_data, index=time_index, auto_play=True, max_opacity=0.8).add_to(m)

        # Save map to an HTML string
        map_html = m._repr_html_()

        return render_template('map.html', map_html=map_html)
    
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

if __name__ == '__main__':
   app.run(debug=True)
