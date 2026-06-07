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
    self.tráffic.graph=traffic_graph
  def heuristic(self,n1,n2):
    return math.hypot(n1.latitude-n2.latitude,n1.longitude-n2.longitude)*111
  def search(self,start_coords,goal_coord):
    start_node=Node(start_coords[0],start_coord[1])
    goal_node=Node(goal_coord[0],goal_coords[1])
    start_node.h=self.heuristic(start_node,goal_node)
    start_node.f=start_node.g+start_node.h
    open_set=[start_node]
    visited_g=[(start_node.latitude,start_node.longitude):0.0}
    while open_set:
      current=heapq.heappop(open_set)
      if(current.latitude, current.longitude)==(goal_node.latitude,goal_node.longitude):
        path=[]
        while current:
          path.append((current.latitude,current.longitude))
          current=current.parent
        return path[::-1]
      current_coords=(current.latitude, current.longitude)
      for next 
          
    
    
    
