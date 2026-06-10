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
    optimal_time = float('inf')
    optimal_cost = float('inf')
    optimal_shipper_time = None
    optimal_shipper_cost = None
    
    for shipper_id, info in routes.items():
        coordinates = [city_map.get(name, {'latitude': 0.0, 'longitude': 0.0}) for name in info['route']]
        response[shipper_id] = {
            'shipper_name': info.get('shipper_name', 'N/A'),
            'shipper_id': info.get('shipper_id', shipper_id),
            'route': info['route'],
            'total_time_minutes': info['total_time_minutes'],
            'total_distance_km': info.get('total_distance_km', 0.0),
            'total_cost': info.get('total_cost', 0.0),
            'coordinates': coordinates
        }
        
        if info['total_time_minutes'] < optimal_time:
            optimal_time = info['total_time_minutes']
            optimal_shipper_time = info.get('shipper_name', 'N/A')
        
        if info.get('total_cost', float('inf')) < optimal_cost:
            optimal_cost = info.get('total_cost', float('inf'))
            optimal_shipper_cost = info.get('shipper_name', 'N/A')
    
    return jsonify({
        'routes': response,
        'summary': {
            'optimal_time': {
                'shipper': optimal_shipper_time,
                'minutes': round(optimal_time, 2)
            },
            'optimal_cost': {
                'shipper': optimal_shipper_cost,
                'amount': round(optimal_cost, 2)
            }
        }
    })

@app.route('/api/stats')
def stats():
    routes = coordinator.run_multi_routing(hour=6, day_type='normal')
    total_time = sum(info['total_time_minutes'] for info in routes.values())
    total_distance = sum(info.get('total_distance_km', 0.0) for info in routes.values())
    total_cost = sum(info.get('total_cost', 0.0) for info in routes.values())
    num_shippers = len(routes)
    
    return jsonify({
        'total_shippers': num_shippers,
        'total_time_minutes': round(total_time, 2),
        'total_distance_km': round(total_distance, 2),
        'total_cost': round(total_cost, 2),
        'avg_time_per_shipper': round(total_time / num_shippers if num_shippers > 0 else 0, 2),
        'avg_distance_per_shipper': round(total_distance / num_shippers if num_shippers > 0 else 0, 2),
        'avg_cost_per_shipper': round(total_cost / num_shippers if num_shippers > 0 else 0, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
