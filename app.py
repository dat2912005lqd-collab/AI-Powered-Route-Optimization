from flask import Flask, render_template, jsonify
from algorithms.multi_shipper import MultiShipperCoordinator

app = Flask(__name__, template_folder='templates', static_folder='static')

coordinator = MultiShipperCoordinator(
    cities_path='data/vietnam_cities.csv',
    traffic_path='data/traffic_schedule.csv',
    shipper_path='data/shipper.csv'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/optimize')
def optimize():
    routes = coordinator.run_multi_routing(hour=6, day_type='normal')
    city_map = {
        row['city_name']: {
            'latitude': float(row['latitude']),
            'longitude': float(row['longitude'])
        }
        for _, row in coordinator.df_cities.iterrows()
    }
    response = {}
    for shipper_id, info in routes.items():
        coordinates = [city_map.get(name, {'latitude': 0.0, 'longitude': 0.0}) for name in info['route']]
        response[shipper_id] = {
            'route': info['route'],
            'total_time_minutes': info['total_time_minutes'],
            'coordinates': coordinates
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
