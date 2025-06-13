from datetime import datetime

# Date
START_DATE = datetime(1936, 1, 1)
CURRENT_DATE = datetime(1936, 1, 1)
END_DATE = datetime(1942, 1, 1)
SWITCH_DATE = datetime(1938, 1, 1)
TRANSFORM_DATE = datetime(1938, 1, 1)
TARGET_TECH_DATE = datetime(1938, 7, 1)

# Trade
TRADE_CIV_EACH_MIL = 0.5

# Construction
CIVILIAN = 200
MILITARY = 100
CONSUMER_GOODS = 0.2
CIVILIAN_COST = 10800
MILITARY_COST = 7200
CIVILIAN_TO_MILITARY_COST = 2800
BASE_CONSTRUCTION_SPEED = 5
ADDITIONAL_CONSTRUCTION_SPEED = 1.2
INFRASTRUCTURE = 1.8
CONSTRUCTION_TECH_EFFECT = 0.1
CONSTRUCTION_FINISH_DATE = [
	datetime(1936, 7, 1),
	datetime(1937, 1, 1),
	datetime(1939, 1, 1),
	datetime(1941, 1, 1),
	datetime(1943, 1, 1),
]

def get_construction_speed():
    tech_level = sum(1 for d in CONSTRUCTION_FINISH_DATE if CURRENT_DATE > d)
    speed_bonus = ADDITIONAL_CONSTRUCTION_SPEED + CONSTRUCTION_TECH_EFFECT * tech_level
    return BASE_CONSTRUCTION_SPEED * speed_bonus * INFRASTRUCTURE

# Production
BASE_FACTORY_OUTPUT = 4.5
ADDITIONAL_FACTORY_OUTPUT = 1.3
INDUSTRY_TECH_EFFECT = 0.15
INDUSTRY_FINISH_DATE = [
	datetime(1937, 1, 1),
	datetime(1937, 7, 1),
	datetime(1939, 1, 1),
	datetime(1941, 1, 1),
	datetime(1943, 1, 1),
]

def get_factory_output():
    tech_level = sum(1 for d in INDUSTRY_FINISH_DATE if CURRENT_DATE > d)
    output_bonus = ADDITIONAL_FACTORY_OUTPUT + INDUSTRY_TECH_EFFECT * tech_level
    return BASE_FACTORY_OUTPUT * output_bonus

# Efficiency
BASE_PRODUCTION_EFFICIENCY_CAP = 0.5
ADDITIONAL_PRODUCTION_EFFICIENCY_CAP = 0.1
MACHINETOOL_TECH_EFFECT = 0.1
MACHINETOOL_FINISH_DATE = [
	datetime(1936, 7, 1),
	datetime(1938, 1, 1),
	datetime(1939, 1, 1),
	datetime(1941, 1, 1),
	datetime(1943, 1, 1),
]

def get_production_efficiency_cap():
    tech_level = sum(1 for d in MACHINETOOL_FINISH_DATE if CURRENT_DATE > d)
    efficiency_cap = BASE_PRODUCTION_EFFICIENCY_CAP + MACHINETOOL_TECH_EFFECT * tech_level
    return efficiency_cap
