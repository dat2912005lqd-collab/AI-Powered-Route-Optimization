import random
import numpy as np
class GeneticRouting Solver:
def __init__(self,time_matrix,demands,capacity, pop_size=100,generations=200,mutate_rates=0,1):
  self.time_matrix=time_matrix
  self.demands=demands
  self.capacity=capacity
  self.pop_size=pop_size
  self.generations=generations
  self.mutate_rates=mutate_rates
  self.num_cities=len(demands)
def _generate_cchromosome(self):
  cities=list(range(1,self.num_cities))
  random.shuffle(cities)
  return cities
def calculate_fitness(self,chromosome):
  total_time=0
  current_load=0
  prev_node=0
  for node in chromosome:
    if current_load+self.demands[node]>self.capacity:
      total_time+=self.time_matrix[prev_node][0]+self.time_matrix[0][node] 
      current_load=self.demamds[node]
    else:
      total_time+=self.time_matrix[prev_node][node]
      current_load+=self.demands[node]
    prev_node=node
  total_time+= self.time_matrix[prev_node][0]
  return 1/total_time
def evolve(self):
  popurt random
import numpy as np
class GeneticRouting Solver:
def __init__(self,time_matrix,demands,capacity, pop_size=100,generations=200,mutate_rates=0,1):
  self.time_matrix=time_matrix
  self.demands=demands
  self.capacity=capacity
  self.pop_size=pop_size
  self.generations=generations
  self.mutate_rates=mutate_rates
  self.num_cities=len(demands)
def _generate_cchromosome(self):
  cities=list(range(1,self.num_cities))
  random.shuffle(cities)
  return cities
def calculate_fitness(self,chromosome):
  total_time=0
  current_load=0
  prev_node=0
  for node in chromosome:
    if current_load+self.demands[node]>self.capacity:
      total_time+=self.time_matrix[prev_node][0]+self.time_matrix[0][node] 
      current_load=self.demamds[node]
    else:
      total_time+=self.time_matrix[prev_node][node]
      current_load+=self.demands[node]
    prev_node=node
  total_time+= self.time_matrix[prev_node][0]
  return 1/total_time
def evolve(self):
  popu
  
      
