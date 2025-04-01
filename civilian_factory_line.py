import globals
from event_system import EventManager

class CivilianFactoryLine:
    def __init__(self, event_manager):
        self.active_civilian_num = globals.CIVILIAN - (globals.CIVILIAN + globals.MILITARY) * globals.CONSUMER_GOODS - globals.MILITARY * globals.TRADE_CIV_EACH_MIL
        self.civilian_line = [0] * 20
        self.military_line = [0] * 20
        self.event_manager = event_manager

    def build_one_day(self):
        if globals.CURRENT_DATE >= globals.SWITCH_DATE:
            self.build_military()
        else:
            self.build_civilian()
        self.update()

    def build_civilian(self):
        remaining_factories = self.active_civilian_num
        for i in range(len(self.civilian_line)):
            if remaining_factories <= 0:
                break
            if remaining_factories >= 15:
                self.civilian_line[i] += 15 * globals.get_construction_speed()
                remaining_factories -= 15
            else:
                self.civilian_line[i] += remaining_factories * globals.get_construction_speed()
                remaining_factories = 0

    def build_military(self):
        remaining_factories = self.active_civilian_num
        for i in range(len(self.military_line)):
            if remaining_factories <= 0:
                break
            if remaining_factories >= 15:
                self.military_line[i] += 15 * globals.get_construction_speed()
                remaining_factories -= 15
            else:
                self.military_line[i] += remaining_factories * globals.get_construction_speed()
                remaining_factories = 0

    def update(self):
        for i in range(len(self.civilian_line)):
            if self.civilian_line[i] >= globals.CIVILIAN_COST:
                self.civilian_line[i] -= globals.CIVILIAN_COST
                globals.CIVILIAN += 1

        for i in range(len(self.military_line)):
            if self.military_line[i] >= globals.MILITARY_COST:
                self.military_line[i] -= globals.MILITARY_COST
                globals.MILITARY += 1
                self.event_manager.trigger_event("military_factory_built")
        
        self.civilian_line.sort(reverse=True)
        self.military_line.sort(reverse=True)
        self.active_civilian_num = globals.CIVILIAN - (globals.CIVILIAN + globals.MILITARY) * globals.CONSUMER_GOODS - globals.MILITARY * globals.TRADE_CIV_EACH_MIL
