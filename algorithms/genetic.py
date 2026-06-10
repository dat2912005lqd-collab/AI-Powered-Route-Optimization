import random
import numpy as np

class GeneticRoutingSolver:
  def __init__(self, time_matrix, distance_matrix, demands, capacity, time_cost_per_minute=1.0, distance_cost_per_km=0.5, pop_size=100, generations=200, mutate_rates=0.1):
    self.time_matrix = time_matrix
    self.distance_matrix = distance_matrix
    self.demands = demands
    self.capacity = capacity
    self.time_cost_per_minute = time_cost_per_minute
    self.distance_cost_per_km = distance_cost_per_km
    self.pop_size = pop_size
    self.generations = generations
    self.mutate_rates = mutate_rates
    self.num_cities = len(demands)

  def _generate_chromosome(self):
    cities = list(range(1, self.num_cities))
    random.shuffle(cities)
    return cities

  def evaluate_chromosome(self, chromosome):
    total_time = 0.0
    total_distance = 0.0
    current_load = 0
    prev_node = 0
    for node in chromosome:
      if current_load + self.demands[node] > self.capacity:
        total_time += self.time_matrix[prev_node][0] + self.time_matrix[0][node]
        total_distance += self.distance_matrix[prev_node][0] + self.distance_matrix[0][node]
        current_load = self.demands[node]
      else:
        total_time += self.time_matrix[prev_node][node]
        total_distance += self.distance_matrix[prev_node][node]
        current_load += self.demands[node]
      prev_node = node
    total_time += self.time_matrix[prev_node][0]
    total_distance += self.distance_matrix[prev_node][0]
    total_cost = total_time * self.time_cost_per_minute + total_distance * self.distance_cost_per_km
    return total_time, total_distance, total_cost

  def calculate_fitness(self, chromosome):
    _, _, total_cost = self.evaluate_chromosome(chromosome)
    return 1.0 / (total_cost + 1e-9)

  def evolve(self):
    population = [self._generate_chromosome() for _ in range(self.pop_size)]
    for gen in range(self.generations):
      fitness_scores = [self.calculate_fitness(chrom) for chrom in population]
      for chrom in population:
        if len(chrom) > 1 and random.random() < self.mutate_rates:
          idx1, idx2 = random.sample(range(len(chrom)), 2)
          chrom[idx1], chrom[idx2] = chrom[idx2], chrom[idx1]
      best_idx = np.argmax(fitness_scores)
      best_chrom = population[best_idx]
    total_time, total_distance, total_cost = self.evaluate_chromosome(best_chrom)
    return best_chrom, total_time, total_distance, total_cost
