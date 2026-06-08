import math
import csv
import heapq

class Node:
  def __init__(self, lat, lon, g=0, h=0, parent=None):
    self.lat = lat
    self.lon = lon
    self.g, self.h = g, h
    self.f = g + h
    self.parent = parent
  def __lt__(self, other):
    return self.f < other.f

class AStarPlanner:
  def __init__(self, traffic_graph):
    self.traffic_graph = traffic_graph
  def heuristic(self, n1, n2):
    return math.hypot(n1.lat - n2.lat, n1.lon - n2.lon) * 111
  def search(self, start_coords, goal_coord):
    start_node = Node(start_coords[0], start_coords[1])
    goal_node = Node(goal_coord[0], goal_coord[1])
    start_node.h = self.heuristic(start_node, goal_node)
    start_node.f = start_node.g + start_node.h
    open_set = [start_node]
    visited_g = {(start_node.lat, start_node.lon): 0.0}
    while open_set:
      current = heapq.heappop(open_set)
      if (current.lat, current.lon) == (goal_node.lat, goal_node.lon):
        path = []
        while current:
          path.append((current.lat, current.lon))
          current = current.parent
        return path[::-1]
      current_coords = (current.lat, current.lon)
      for next_coords, travel_cost in self.traffic_graph.get(current_coords, []):
        new_g = current.g + travel_cost
        if next_coords not in visited_g or new_g < visited_g[next_coords]:
          visited_g[next_coords] = new_g
          neighbor = Node(next_coords[0], next_coords[1], g=new_g, parent=current)
          neighbor.h = self.heuristic(neighbor, goal_node)
          neighbor.f = neighbor.g + neighbor.h
          heapq.heappush(open_set, neighbor)
    return []

def load_graph_from_csv(file_path):
  points = []
  with open(file_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
      lat = float(row['latitude'])
      lon = float(row['longitude'])
      points.append((lat, lon))
  graph = {}
  for p1 in points:
    graph[p1] = []
    for p2 in points:
      if p1 != p2:
        dist = math.hypot(p1[0] - p2[0], p1[1] - p2[1]) * 111
        graph[p1].append((p2, dist))
  return graph

if __name__ == '__main__':
  traffic_graph = load_graph_from_csv('vietnam_cities.csv')
  planner = AStarPlanner(traffic_graph)
  start = (21.0285, 105.8542)
  goal = (10.7769, 106.7009)
  route = planner.search(start, goal)
  print(f"Lộ trình tối ưu qua các thành phố: {route}")
  
    
        
          
    
    
    
