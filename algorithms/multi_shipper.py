import pandas as pd
import numpy as np
from algorithms.distance_matrix import DistanceMatrixBuilder
from algorithms.genetic import GeneticRoutingSolver

class MultiShipperCoordinator:
  def __init__(self,cities_path,traffic_path,shipper_path):
    self.matrix_builder = DistanceMatrixBuilder(cities_path, traffic_path, shipper_path)
    self.df_shipper = pd.read_csv(shipper_path)
    self.df_cities = pd.read_csv(cities_path)
  def _assign_cities_to_shippers(self,active_shippers):
    shipper_tasks={s['shipper_id']: [] for _, s in active_shippers .iterrows()}
    home_cities=set(active_shippers['city_id'])
    delivery_points=self.df_cities[~self.df_cities['city_id'].isin(home_cities)].to_dict('records')
    for point in delivery_points:
      best_shipper_id=None
      min_dist=float('inf')
      for _,shipper in active_shippers.iterrows():
        shipper_home=self.df_cities[self.df_cities['city_id']==shipper['city_id']].iloc[0]
        dist=self.matrix_builder.haversine_distance(point['longitude' ],point['latitude'],shipper_home['longitude'],shipper_home['latitude'])
        if dist< min_dist:
          min_dist=dist
          best_shipper_id=shipper['shipper_id']
      if best_shipper_id:
        shipper_tasks[best_shipper_id].append(point)
    return shipper_tasks
  def run_multi_routing(self,hour,day_type):
    active_shippers=self.df_shipper[self.df_shipper['status'].isin(['active','available'])]
    shipper_tasks=self._assign_cities_to_shippers(active_shippers)
    final_routes={}
    for _,shipper in active_shippers.iterrows():
      s_id=shipper['shipper_id']
      assigned_points=shipper_tasks[s_id]
      if not assigned_points:
        continue
      shipper_home=self.df_cities[self.df_cities['city_id']==shipper['city_id']].iloc[0].to_dict()
      local_cities=[shipper_home]+assigned_points
      df_local_cities=pd.DataFrame(local_cities)
      self.matrix_builder.cities = df_local_cities
      distance_matrix = self.matrix_builder.build_distance_matrix()
      time_matrix = self.matrix_builder.build_time_matrix(hour, day_type, s_id)
      zone_cost_matrix = self.matrix_builder.build_zone_cost_matrix()
      demands = df_local_cities['demand'].values
      solver = GeneticRoutingSolver(
        time_matrix=time_matrix,
        distance_matrix=distance_matrix,
        demands=demands,
        capacity=shipper['capacity'],
        time_cost_per_minute=1.0,
        distance_cost_per_km=0.6,
        zone_cost_matrix=zone_cost_matrix
      )
      best_chrom, total_time, total_distance, total_cost = solver.evolve()
      route_names = [df_local_cities.iloc[0]['city_name']] + [df_local_cities.iloc[i]['city_name'] for i in best_chrom]
      final_routes[s_id] = {
        "shipper_name": shipper['name_city'],
        "shipper_id": s_id,
        "route": route_names,
        "total_time_minutes": round(total_time, 2),
        "total_distance_km": round(total_distance, 2),
        "total_cost": round(total_cost, 2)
      }
    return final_routes

if __name__ == '__main__':
  coordinator = MultiShipperCoordinator(
    cities_path='data/vietnam_cities.csv',
    traffic_path='data/traffic_schedule.csv',
    shipper_path='data/shipper.csv'
  )
  routes = coordinator.run_multi_routing(hour=6, day_type='normal')
  print('Multi-shipper routing results:')
  for shipper_id, route_info in routes.items():
    print(f"- shipper {shipper_id}: {route_info['route']} (time={route_info['total_time_minutes']} min)")

