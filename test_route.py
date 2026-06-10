#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from algorithms.multi_shipper import MultiShipperCoordinator

coordinator = MultiShipperCoordinator('data/vietnam_cities.csv','data/traffic_schedule.csv','data/shipper.csv')
routes = coordinator.run_multi_routing(hour=6, day_type='normal')

optimal_time = float('inf')
optimal_cost = float('inf')
optimal_shipper_time = None
optimal_shipper_cost = None

for shipper_id, info in routes.items():
    if info['total_time_minutes'] < optimal_time:
        optimal_time = info['total_time_minutes']
        optimal_shipper_time = info.get('shipper_name', 'N/A')
    if info.get('total_cost', float('inf')) < optimal_cost:
        optimal_cost = info.get('total_cost', float('inf'))
        optimal_shipper_cost = info.get('shipper_name', 'N/A')

summary = {
    'optimal_time': {'shipper': optimal_shipper_time, 'minutes': round(optimal_time, 2)},
    'optimal_cost': {'shipper': optimal_shipper_cost, 'amount': round(optimal_cost, 2)},
    'sample_routes': {k: {'shipper': v['shipper_name'], 'time': v['total_time_minutes'], 'cost': v['total_cost']} for k, v in list(routes.items())[:2]}
}
print(json.dumps(summary, ensure_ascii=True, indent=2))
