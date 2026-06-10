import pandas as pd
import numpy as np
from math import radians,cos, sin,asin,sqrt
class DistanceMatrixBuilder:
  def __init__(self,cities_path,traffic_path,shipper_path):
    self.df_cities=pd.read_csv(cities_path)
    self.df_traffic=pd.read_csv(traffic_path)
    self.df_shipper=pd.read_csv(shipper_path)
    self.cities = self.df_cities

  def haversine_distance(self, lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    return 2 * 6371 * np.arcsin(np.sqrt(a))

  def build_distance_matrix(self):
    cities_df = self.cities
    lat = np.radians(cities_df['latitude'].values)
    lon = np.radians(cities_df['longitude'].values)
    dlat = lat[:, None] - lat
    dlon = lon[:, None] - lon
    a = np.sin(dlat / 2)**2 + np.cos(lat[:, None]) * np.cos(lat) * np.sin(dlon / 2)**2
    distance_matrix = 2 * 6371 * np.arcsin(np.sqrt(a)) * 1.3
    return distance_matrix

  def build_time_matrix(self,hour,day_type,shipper_id):
    t_row = self.df_traffic[(self.df_traffic['hour'] == hour) & (self.df_traffic['day_type'] == day_type)]
    traffic_f = t_row['traffic_factor'].values[0]
    s_row = self.df_shipper[self.df_shipper['shipper_id'] == shipper_id]
    shipper_f = s_row['speed_factor'].values[0]
    v_effective = (40 / 60) * shipper_f / traffic_f
    distance_matrix = self.build_distance_matrix()
    time_matrix = distance_matrix / v_effective
    return time_matrix
