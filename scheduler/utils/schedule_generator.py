from copy import copy
from typing import List

from scheduler.utils.UVAClass import UVAClass
from scheduler.utils.UVASchedule import UVASchedule


def generate_schedules(input_classes: List[UVAClass]):
    input_classes.sort(key=lambda x: x.class_num)
    output = []
    generate_schedules_helper(input_classes, UVASchedule(), output)
    output.sort(key=lambda x: len(x.classes), reverse=True)
    return output


def generate_schedules_helper(input_classes, schedule, output):
    for c in input_classes:
        if c.class_num > schedule.get_max_class_num() and c.days != 'TBA':
            if not schedule.push_class(c):
                continue
            if 15 <= schedule.num_credits <= 18:
                output.append(copy(schedule))
            generate_schedules_helper(input_classes, schedule, output)
            schedule.pop_class()
