import pandas as pd
import numpy as np
from math import radians,cos, sin,asin,sqrt
class DistanceMatrixBuilder:
  def __init__(self,cities_name,traffic_path,shipper_path):
    self.df_cities=pd.read_csv(cities_name)
    self.df_traffic=pd.read_csv(traffic_path)
    self.df_shipper=pd.read_csv(shipper_path)
  def haversine_distance(self,lon1,lat1,lon2,lat2):
    lon1, lat1,lon2,lat2=map(radians,[lon1, lat1, lon2,lat2])
    dlon=lon2-lon1
    dlat=lat2-lat1
    a=sin(dlat/2)**2+cos(lat1)*cos(lat2)* sin(dlon/2)**2
    c=2*asin(sqrt(a))
    r=6731
    return c*r
  def get_traffic_factor(self,time_slot):
    traffic_row=self.df_trafic[self.df_traffic['time_slot']==time_slot]
    if not traffic_row.empty:
      return traffic_row['congestion_factor'].values[0]
