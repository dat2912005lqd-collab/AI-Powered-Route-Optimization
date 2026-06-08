import pandas as pd
import numpy as np
from distance_matrix import DistanceMatrixBuilder
from genetic import GeneticRoutingSolver
class MultiShipperCoordinator:
  def __init__(self,cities_path,traffic_path,shipper_path):
    self.matrix_builder=DistanceMatrixBuilder(cities_path,traffic_path,shipper_path)
    self.df_shipper=pd.read_csv(shipper_path)
    self.df_cities=pd.read_csv(cities_path)
  def 
