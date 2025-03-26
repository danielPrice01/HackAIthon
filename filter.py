import json

class Filter:
    def __init__(self, filter_file):
        """
        Initialize the Filter by reading courses from a JSON file.
        
        Parameters:
            filter_file (str): Path to the JSON file containing course data.
        """
        with open(filter_file, 'r') as f:
            self.all_courses = json.load(f)
        # Default columns always shown:
        self.default_columns = ["id", "name"]
        # Additional filters: attribute -> value.
        self.filters = {}
        # Update state based on all courses and current filters.
        self.update_state()

    def update_state(self):
        """
        Recompute the current courses and columns based on the applied filters.
        Starting with all courses, for each filter with a non-empty value, only courses
        with that attribute containing the value are retained.
        The current columns are the default columns plus the attributes of the filters.
        """
        courses = self.all_courses
        for attr, val in self.filters.items():
            if val:  # Only filter if a non-empty value was provided.
                courses = [course for course in courses if attr in course and val in course[attr]]
        self.current_courses = courses
        # Current columns: default columns plus the keys in filters (order is the order of insertion).
        self.current_columns = self.default_columns + list(self.filters.keys())

    def add_filter(self, attribute, value):
        """
        Add (or update) a filter on an attribute.
        
        Parameters:
            attribute (str): The attribute to filter on (e.g., "prereq").
            value (str): The substring to look for in that attribute.
                         If empty, the column is added without filtering courses.
        
        This method adds the attribute (as a new column) and then updates the current courses.
        """
        self.filters[attribute] = value
        self.update_state()

    def delete_filter(self, attribute):
        """
        Remove a filter (and its column) from the current state.
        
        Parameters:
            attribute (str): The attribute to remove.
        """
        if attribute in self.filters:
            del self.filters[attribute]
        self.update_state()

    def get_current_state(self):
        """
        Returns the current state as a dictionary with two keys:
          - "columns": a list of column names currently being displayed.
          - "courses": a list of dictionaries where each dictionary represents a row
                       (i.e. a course) with keys corresponding to the current columns.
        """
        displayed_courses = []
        for course in self.current_courses:
            row = {}
            for col in self.current_columns:
                row[col] = course.get(col, "")
            displayed_courses.append(row)
        return {
            "columns": self.current_columns,
            "courses": displayed_courses
        }

    def get_current_filters(self):
        """
        Returns a copy of the currently applied filters.
        
        The returned dictionary maps filter attributes to their filter values.
        """
        return self.filters.copy()

    def get_num_classes(self):
        """
        Returns the number of courses currently displayed.
        """
        return len(self.current_courses)
    
    def get_classes(self):
        """
        Returns the courses currently displayed.
        """
        return self.current_courses

    def add_column(self, class_ids, attribute, values):
        """
        Add a column to the courses with the given attribute and corresponding values.
        
        Parameters:
            class_ids (list): A list of course IDs for which the attribute should be set.
            attribute (str): The attribute name to be added as a column.
            values (list): A list of values corresponding to each course ID in class_ids.
            
        For each course in all_courses, if the course's 'id' is in class_ids, the course is updated 
        with the given attribute set to the corresponding value. For courses whose 'id' is not in 
        class_ids, the attribute is set to an empty string.
        """
        # Create a mapping from course ID to its new value.
        mapping = dict(zip(class_ids, values))
        for course in self.all_courses:
            course_id = course.get("id")
            if course_id in mapping:
                course[attribute] = mapping[course_id]
            else:
                course[attribute] = ""
        # Ensure the new attribute is always displayed by adding it to additional_columns.
        if attribute not in self.additional_columns:
            self.additional_columns.append(attribute)
        self.update_state()
