import json

class Filter:
    def __init__(self, filter_file):
        """
        Initialize the Filter by reading courses from a JSON file.
        
        Parameters:
            filter_file (str): Path to the JSON file containing course data.
        """
        with open(filter_file, 'r') as file:
            self.courses = json.load(file)
    
    def filter_courses(self, attribute, input_parameter):
        """
        Filters the courses based on whether the specified attribute contains the input_parameter.
        
        Parameters:
            attribute (str): The key in the course dictionary (e.g., "prereq" or "available").
            input_parameter (str): The substring to search for within that attribute.
        
        Returns:
            list: A list of course dictionaries that match the criteria.
        """
        filtered_courses = []
        for course in self.courses:
            if attribute in course and input_parameter in course[attribute]:
                filtered_courses.append(course)
        return filtered_courses

    def get_filter_descriptor(self, class_name, attributes, values):
        """
        Returns a JSON descriptor for a class with filters.
        
        Parameters:
            class_name (str): The name of the class (e.g., "CIS 1200").
            attributes (list): A list of attribute names (e.g., ["prereq", "available"]).
            values (list): A list of values corresponding to each attribute.
        
        Returns:
            str: A JSON formatted string representing the class and its filters.
        
        Raises:
            ValueError: If the lengths of attributes and values do not match.
        """
        if len(attributes) != len(values):
            raise ValueError("The length of attributes and values must be the same.")
       
        descriptor = {"class": class_name}
        for attr, val in zip(attributes, values):
            descriptor[attr] = val
           
        return json.dumps(descriptor, indent=2)
