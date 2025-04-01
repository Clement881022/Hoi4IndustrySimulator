import globals
from event_system import EventManager

class MilitaryFactory:
    def __init__(self, is_initial_factory=False):
        if is_initial_factory:
            self.production_efficiency = 0.5
        else:
            self.production_efficiency = 0.1

    def produce_one_day(self):
        if globals.CURRENT_DATE < globals.TARGET_TECH_DATE:
            return 0
        
        cap = globals.get_production_efficiency_cap()
        if self.production_efficiency < cap:
            self.production_efficiency += 0.001 * cap * cap / self.production_efficiency
        return globals.get_factory_output() * self.production_efficiency

class MilitaryFactoryLine:
    def __init__(self, event_manager):
        self.ic = 0
        self.factories = []
        self.event_manager = event_manager
        self.event_manager.add_listener("military_factory_built", self.add_factory)
        for _ in range(globals.MILITARY):
            self.add_initial_factory()

    def add_initial_factory(self):
        self.factories.append(MilitaryFactory(is_initial_factory=True))

    def add_factory(self):
        self.factories.append(MilitaryFactory())

    def produce_one_day(self):
        for factory in self.factories:
            self.ic += factory.produce_one_day()
