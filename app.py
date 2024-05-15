from flask import Flask, render_template, request
import pandas as pd
import folium

app = Flask(__name__)

def summ(user_input):
    try:
        return int(user_input) + 2
    except ValueError:
        return None

@app.route('/', methods=['GET', 'POST'])
def main():
    result = None
    error = None
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        result = summ(user_input)
        if result is None:
            error = "Please provide only numbers."

    return render_template('main.html', result=result, error=error)

csv_file_path = 'master_data_us_no_duplicates_cleaned.csv'

@app.route('/map_view')
def index():
    try:
        df = pd.read_csv(csv_file_path, sep='\t')
        print(df.head())  # Debug: print the first few rows of the DataFrame
        
        # Check if DataFrame is empty
        if df.empty:
            return "No data available"

        # Create a map centered at an average location
        m = folium.Map(location=[df['decimalLatitude'].mean(), df['decimalLongitude'].mean()], zoom_start=5)
        
        # Add points to the map
        for _, row in df.iterrows():
            folium.Marker(
                location=[row['decimalLatitude'], row['decimalLongitude']],
                popup=f"Date: {row['eventDate']}, Location: ({row['decimalLatitude']}, {row['decimalLongitude']})",
            ).add_to(m)
        
        # Save map to an HTML string
        map_html = m._repr_html_()
        
        return render_template('map.html', map_html=map_html)
    
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

if __name__ == '__main__':
   app.run()
