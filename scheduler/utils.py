class UVAClass:
    """
    A model representing a specific section of a UVA course.
    """
    def __init__(self, class_num, name, days, units):
        # Class number from Lou's list. A unique identifier for each class
        self.class_num = class_num

        # Name for a given course. Defined as {mnemonic} {course_num}-{section_num}.
        # This value will be unique and may be used for hashing.
        self.name = name

        # 'Days' value from searchData.csv. A string representing the days
        # of the week and time of a class.
        self.days = days

        # Number of credit units for this class
        self.units = units

    def __str__(self):
        return self.name + " (" + str(self.class_num) + "): " + self.days + ", Credits: " + self.units


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

    def add_class(self, class_num):
        """
        Add a class to self.classes if all hard constraints are met.

        :param class_num: unique identifier for a class
        :return: true if class added, false otherwise
        """
        pass

    def remove_class(self, class_num):
        pass