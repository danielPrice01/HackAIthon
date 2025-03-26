import os
import json
import openai
import asyncio

class CourseBot:
    def __init__(self, course, chat_model="gpt-4", prompt_template=None):
        self.course = course
        self.chat_model = chat_model
        # A template for building the prompt. You can adjust this as needed.
        self.prompt_template = prompt_template or (
            "Course Details:\n{course_details}\n\n"
            "Course Description:\n{description}\n\n"
            "User Query: {query}\n\n"
            "Provide a detailed, course-specific response:"
        )

    async def generate_response(self, user_query):
        # Use the course description (or a fallback message)
        description = self.course.get("description", "No description available.")
        # Convert full course details into a JSON string (or customize as desired)
        course_details = json.dumps(self.course)
        prompt = self.prompt_template.format(
            course_details=course_details,
            description=description,
            query=user_query
        )
        messages = [
            {"role": "system", "content": "You are a helpful assistant specialized in course-related information."},
            {"role": "user", "content": prompt}
        ]
        response = await openai.ChatCompletion.acreate(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message["content"].strip()

class AgenticSwarm:
    def __init__(self, courses_file, **kwargs):
        self.courses_file = courses_file
        with open(courses_file, "r") as f:
            self.courses = json.load(f)
        self.kwargs = kwargs

    async def run_swarm(self, user_query, filtered_courses=None):
        # Use the filtered courses if provided; otherwise, process all courses.
        courses_to_process = filtered_courses if filtered_courses is not None else self.courses
        results = {}
        # Process each course sequentially.
        for course in courses_to_process:
            bot = CourseBot(course, **self.kwargs)
            answer = await bot.generate_response(user_query)
            results[course.get("id")] = answer
        return results

# Example usage:
async def main():
    swarm = AgenticSwarm("courses/courses.json", chat_model="gpt-4")
    user_query = "In 5 words, does this course involve machine learning?"
    results = await swarm.run_swarm(user_query)
    for course_id, answer in results.items():
        print(f"Course {course_id}:\n{answer}\n")

if __name__ == "__main__":
    asyncio.run(main())
