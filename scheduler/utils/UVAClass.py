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

    def __eq__(self, o):
        this_course = self.name.split('-')[0]
        other_course = o.name.split('-')[0]
        return this_course == other_course and self.units == o.units
