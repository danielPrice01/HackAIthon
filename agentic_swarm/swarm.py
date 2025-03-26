import json
from agentic_swarm.course_bot import CourseBot
from filter import Filter

class AgenticSwarm:
    def __init__(self, courses_file, filter_instance, **kwargs):
        self.courses_file = courses_file
        self.filter = filter_instance
        with open(courses_file, "r") as f:
            self.courses = json.load(f)
        self.kwargs = kwargs

    async def run_swarm(self, user_query, filtered_courses=None):
        if filtered_courses is None:
            courses_to_process = self.filter.get_classes()
        else:
            courses_to_process = filtered_courses
        results = {}
        # Process each course sequentially.
        for course in courses_to_process:
            bot = CourseBot(course, **self.kwargs)
            answer = await bot.answer_query(user_query)
            results[course.get("id")] = answer
        return results
