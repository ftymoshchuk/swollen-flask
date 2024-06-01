from flask import Flask, render_template, request
import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
from folium.plugins import HeatMap
import constants
import data_connector

app = Flask(__name__)

state_mapping = constants.state_mapping
master_data = data_connector.get_data()

# Reverse the state mapping for dropdown display
reverse_state_mapping = {v: k for k, v in state_mapping.items()}

@app.route('/')
def main():
    return render_template('main.html', states=reverse_state_mapping)

@app.route('/bee-chance', methods=['POST'])
def bee_chance():
    try:
        # Load data
        local_df = master_data

        # Convert eventDate to datetime
        master_data['eventDate'] = pd.to_datetime(master_data['eventDate'])

        # Calculate Sightings Frequency
        local_df['month'] = local_df['eventDate'].dt.month
        local_df['year'] = local_df['eventDate'].dt.year
        state_monthly_sightings = local_df.groupby(['stateNumeric', 'year', 'month']).size().reset_index(name='sightings')

        # Calculate average sightings per month for each state
        avg_sightings = state_monthly_sightings.groupby('stateNumeric')['sightings'].mean().reset_index()

        # Normalize and Categorize
        avg_sightings['normalized'] = (avg_sightings['sightings'] - avg_sightings['sightings'].min()) / (avg_sightings['sightings'].max() - avg_sightings['sightings'].min())

        # Determine thresholds
        low_threshold = avg_sightings['normalized'].quantile(0.33)
        high_threshold = avg_sightings['normalized'].quantile(0.67)

        # Categorize
        def categorize(probability):
            if probability <= low_threshold:
                return 'Low'
            elif probability <= high_threshold:
                return 'Medium'
            else:
                return 'High'

        avg_sightings['category'] = avg_sightings['normalized'].apply(categorize)

        # Summary table
        summary_table = avg_sightings[['stateNumeric', 'category']]

        # Get selected state from the form
        state_numeric = int(request.form['state'])
        state_category = summary_table[summary_table['stateNumeric'] == state_numeric]['category'].values[0]

        # Fetch state name (for display purposes)
        state_name = reverse_state_mapping[state_numeric]

        return render_template('main.html', state_name=state_name, category=state_category, states=reverse_state_mapping)
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/bee-count', methods=['POST'])
def bee_count():
    try:
        state_numeric = int(request.form['state'])

        # Filter the DataFrame for the selected state
        count = master_data[master_data['stateNumeric'] == state_numeric].shape[0]

        state_name = reverse_state_mapping[state_numeric]
        return render_template('main.html', states=reverse_state_mapping, state=state_name, count=count)

    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/heat-map-view')
def heat_map():
    try:
        # Create a folium map centered at an average location
        m = folium.Map(location=[master_data['decimalLatitude'].mean(), master_data['decimalLongitude'].mean()], zoom_start=5)

        # Prepare data for heat map
        heat_data = master_data[['decimalLatitude', 'decimalLongitude']].values.tolist()

        # Add heat map layer
        HeatMap(heat_data).add_to(m)

        # Generate HTML representation of the map
        map_html = m._repr_html_()

        return render_template('heatmap.html', map_html=map_html)

    except Exception as e:
        print(f"Error: {e}")
    return None

@app.route('/map-view')
def index():
    try:
        # Filter out specific warnings if necessary
        local_df = master_data
        #  warnings.filterwarnings("ignore", category=UserWarning, module='folium')

        # Ensure eventDate is parsed correctly and remove timezone information
        #local_df['eventDate'] = pd.to_datetime(local_df['eventDate'], errors='coerce')
        #local_df = local_df.dropna(subset=['eventDate'])  # Drop rows with invalid dates

        # Remove timezone information
        local_df['eventDate'] = local_df['eventDate'].dt.tz_localize(None)
        local_df.sort_values('eventDate', inplace=True)

        # Group data by date
        grouped = local_df.groupby(local_df['eventDate'].dt.date)

        heat_data = []
        time_index = []

        for date, group in grouped:
            heat_data.append(group[['decimalLatitude', 'decimalLongitude']].values.tolist())
            time_index.append(date.strftime('%Y-%m-%d'))

        # Create the map centered at an average location
        m = folium.Map(location=[local_df['decimalLatitude'].mean(), local_df['decimalLongitude'].mean()], zoom_start=5)

        # Add HeatMapWithTime to the map with the oldest date as the start date
        HeatMapWithTime(data=heat_data, index=time_index, auto_play=True, max_opacity=0.8).add_to(m)

        # Save map to an HTML string
        map_html = m._repr_html_()

        return render_template('map.html', map_html=map_html)

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
   app.run(debug=True)
