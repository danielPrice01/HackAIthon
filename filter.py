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
        # Additional columns added via add_column.
        self.additional_columns = []
        # Update state based on all courses and current filters.
        self.update_state()

    def update_state(self):
        """
        Recompute the current courses and columns based on the applied filters.
        Starting with all courses, for each filter with a non-empty value, only courses
        with that attribute containing the value are retained.
        The current columns are the default columns plus the keys in filters and any additional columns.
        """
        courses = self.all_courses
        for attr, val in self.filters.items():
            if val:  # Only filter if a non-empty value was provided.
                courses = [course for course in courses if attr in course and val in course[attr]]
        self.current_courses = courses
        # Current columns: default columns + filter keys.
        self.current_columns = self.default_columns + list(self.filters.keys())
        # Append additional columns that are not already included.
        for col in self.additional_columns:
            if col not in self.current_columns:
                self.current_columns.append(col)

    def add_filter(self, attribute, value):
        """
        Add (or update) a filter on an attribute.
        """
        self.filters[attribute] = value
        self.update_state()

    def delete_filter(self, attribute):
        """
        Remove a filter (and its column) from the current state.
        """
        if attribute in self.filters:
            del self.filters[attribute]
        self.update_state()

    def get_current_state(self):
        """
        Returns the current state as a dictionary with keys:
          - "columns": a list of column names currently being displayed.
          - "courses": a list of dictionaries representing rows.
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
        """
        mapping = dict(zip(class_ids, values))
        for course in self.all_courses:
            course_id = course.get("id")
            if course_id in mapping:
                course[attribute] = mapping[course_id]
            else:
                course[attribute] = ""
        if attribute not in self.additional_columns:
            self.additional_columns.append(attribute)
        self.update_state()
        
    def delete_column(self, attribute):
        """
        Remove an additional column from the filter.
        This method removes the column from additional_columns and updates the state.
        """
        if attribute in self.additional_columns:
            self.additional_columns.remove(attribute)
        # Optionally, remove the column from each course in all_courses:
        for course in self.all_courses:
            if attribute in course:
                del course[attribute]
        self.update_state()
