import json
from chat_bots.agentic_swarm.course_bot import CourseBot

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
        
        if len(courses_to_process) > 15:
            raise ValueError("More than fifteen courses, this is too many to process. Please filter the courses first.")

        results = {}
        # Process each course sequentially.
        for course in courses_to_process:
            bot = CourseBot(course, **self.kwargs)
            answer = await bot.answer_query(user_query)
            results[course.get("id")] = answer
        
        # Build lists for the new column.
        class_ids = []
        answer_values = []
        for course in courses_to_process:
            course_id = course.get("id")
            class_ids.append(course_id)
            # If no answer, use empty string.
            answer_values.append(results.get(course_id, ""))
        
        # Add the new column "swarm_answer" to the filter.
        self.filter.add_column(class_ids, "swarm_answer", answer_values)
        
        return results
