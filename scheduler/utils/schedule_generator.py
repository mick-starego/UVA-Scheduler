from copy import copy
from typing import List

from scheduler.utils.UVAClass import UVAClass
from scheduler.utils.UVASchedule import UVASchedule


def generate_schedules(uva_classes: List[UVAClass]):
    uva_classes.sort(key=lambda x: x.class_num)
    viable_schedules = []
    generate_schedules_helper(uva_classes, viable_schedules, UVASchedule())
    viable_schedules.sort(key=lambda x: len(x.classes), reverse=True)
    return viable_schedules


def generate_schedules_helper(class_list, collector, current):
    for c in class_list:
        if c.class_num > current.get_max_class_num() and c.days != 'TBA':
            if not current.push_class(c):
                continue
            num_credits = sum([int(c.units) for c in current.classes if c.units.isnumeric()])
            if 15 <= num_credits <= 18:
                collector.append(copy(current))
            generate_schedules_helper(class_list, collector, current)
            current.pop_class()
