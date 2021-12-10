class UVASchedule:
    """
    A model representing a collection of classes that meet the following hard
    constraints:

    * The same course (identified by a unique combination of mnemonic and
      course_num) cannot be added to a schedule twice.
    * No two classes can occur at the same time.
    * The total credit units of the schedule must be between 15 and 18 (inclusive)
    """
    def __init__(self, init_classes=None):
        # A list of UVAClass objects
        if init_classes is None:
            init_classes = []
        self.classes = init_classes
        if init_classes is not None:
            self.num_credits = sum([int(c.units) for c in self.classes if c.units.isnumeric()])


    def push_class(self, c):
        """
        Add a class to self.classes.

        :param c: a UVAClass object
        :return: true if constraints satisfied and class added, false otherwise
        """
        # Class will not be added in the case of duplicate classes or conflicting time slots
        if c in self.classes or does_conflict(self, c):
            return False
        self.classes.append(c)
        if c.units.isnumeric():
            self.num_credits += int(c.units)
        return True

    def pop_class(self):
        c = self.classes.pop()
        if c.units.isnumeric():
            self.num_credits -= int(c.units)

    def get_max_class_num(self):
        if len(self.classes) > 0:
            return self.classes[-1].class_num
        return 0

    def __copy__(self):
        return UVASchedule([c for c in self.classes])


def does_conflict(s, c):
    for o in s.classes:
        c_days, c_start, _, c_end = tuple(c.days.split(' '))
        o_days, o_start, _, o_end = tuple(o.days.split(' '))

        for day in ['Mo', 'Tu', 'We', 'Th', 'Fr']:
            if day in c_days and day in o_days:
                if do_times_conflict(c_start, c_end, o_start, o_end):
                    return True
    return False


def do_times_conflict(s1, e1, s2, e2):
    return (get_hf8(s1) == get_hf8(s2)) or (get_hf8(s1) < get_hf8(s2) < get_hf8(e1)) or \
           (get_hf8(s2) < get_hf8(s1) < get_hf8(e2))


def get_hf8(t):
    hrs, mins = tuple(t[0:-2].split(':'))
    if t[-2:].upper() == 'AM' or hrs == '12':
        result = (int(hrs) - 8) * 60 + int(mins)
    else:
        result = ((4 + int(hrs)) * 60) + int(mins)
    return result
