import json
import numpy as np
from course_bot import CourseBot

class AgenticSwarm:
    def __init__(self, courses_file, **kwargs):
        self.courses_file = courses_file
        with open(courses_file, "r") as f:
            self.courses = json.load(f)
        self.kwargs = kwargs

    async def run_swarm(self, user_query, filtered_courses=None):
        courses_to_process = filtered_courses if filtered_courses is not None else self.courses
        results = {}
        # Process each course sequentially.
        for course in courses_to_process:
            bot = CourseBot(course, **self.kwargs)
            answer = await bot.answer_query(user_query)
            results[course.get("id")] = answer
        return results
