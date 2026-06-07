import math
import heapq
class Node:
  def __init__(latitude, longitude,g,h,parent=Node):
    self.latitude=latitude
    self.longitude=longitude
    self.g, self.h=g,h
    self.f=g+h
    self.parent=parent
  def __lt__(self,other):
    return self.f<other.f
class AStarPlanner:
  def __init__(self,traffic_graph):
    slelf
    
    
