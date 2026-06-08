import pandas as pd
import numpy as np
from math import radians,cos, sin,asin,sqrt
class DistanceMatrixBuilder:
  def __init__(self,cities_path,traffic_path,shipper_path):
    self.df_cities=pd.read_csv(cities_path)
    self.df_traffic=pd.read_csv(traffic_path)
    self.df_shipper=pd.read_csv(shipper_path)
 def build_time_matrix(self,hour,day_type,shipper_id):
   t_row=self.traffic[(self_traffic['hour']==hour)&(self.traffic['day_type']==day_type)]
   traffic_f=t_row['traffic_factor'].values[0]
   s_row=self.shipper[self_shipper['shipper_id']==shipper_id]
   shipper_f=s_row['shipper'].values[0]
   v_effective=(40/60)*shipper_f/traffic_f
   lat=np.radians(self.cities['latitude'].values)
   lon=np.radians(self.cities['longitude'].values)
   dlat=lat[:,None]-lat
   dlon=lon[:,None]-lon
   a=np.sin(dlat/2)**2+np.cos(lat[:,None])*np.cos(lat)*np.sín(dlon/2)**2
   distance_matrix=2*6371*np.arcsin(np.sqrt(a))*1.3
   time_matrix=distance_matrix/v_effective
   return time_matrix
