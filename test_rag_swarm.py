import os
import json
import openai
import faiss
import numpy as np
import asyncio

class CourseBot:
    # Global semaphore and embedding cache shared across all CourseBot instances.
    embedding_semaphore = asyncio.Semaphore(1)
    embedding_cache = {}

    def __init__(self, course, chunk_size=500, overlap=50, embedding_model="text-embedding-ada-002", chat_model="gpt-4-turbo", top_k=2):
        self.course = course
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.embedding_model = embedding_model
        self.chat_model = chat_model
        self.top_k = top_k

    def chunk_text(self, text):
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i+self.chunk_size])
            chunks.append(chunk)
            i += self.chunk_size - self.overlap
        return chunks

    async def get_embedding(self, text, retry_count=5):
        # Check global cache first.
        if text in CourseBot.embedding_cache:
            return CourseBot.embedding_cache[text]
        for attempt in range(retry_count):
            async with CourseBot.embedding_semaphore:
                try:
                    response = await openai.Embedding.acreate(input=[text], model=self.embedding_model)
                    embedding = np.array(response['data'][0]['embedding'], dtype=np.float32)
                    CourseBot.embedding_cache[text] = embedding
                    return embedding
                except openai.error.RateLimitError:
                    wait_time = 2 ** attempt
                    print(f"Rate limit encountered for text '{text[:30]}...', waiting {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
        raise Exception("Exceeded maximum retries for get_embedding.")

    async def create_faiss_index(self, chunks):
        tasks = [self.get_embedding(chunk) for chunk in chunks]
        embeddings = await asyncio.gather(*tasks)
        embeddings = np.vstack(embeddings)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        return index, embeddings, chunks

    async def retrieve_chunks(self, query, index, chunks):
        query_embedding = await self.get_embedding(query)
        query_embedding = np.expand_dims(query_embedding, axis=0)
        distances, indices = index.search(query_embedding, self.top_k)
        return [chunks[i] for i in indices[0]]

    def build_prompt(self, user_query, retrieved_context, course_description):
        context = "\n\n".join(retrieved_context)
        course_details = json.dumps(self.course)
        prompt = (
            f"Course Details: {course_details}\n\n"
            f"Course Description: {course_description}\n\n"
            f"Relevant Context:\n{context}\n\n"
            f"User Query: {user_query}\n\n"
            "In 5 to 10 words, provide a course-specific response:"
        )
        return prompt

    async def generate_response(self, prompt, temperature=0.7, max_tokens=500):
        messages = [
            {"role": "system", "content": "You are a helpful assistant specialized in course-related information."},
            {"role": "user", "content": prompt}
        ]
        response = await openai.ChatCompletion.acreate(
            model=self.chat_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message["content"].strip()

    async def answer_query(self, user_query):
        # Load the syllabus text if available.
        syllabus_path = self.course.get("syllabus")
        if syllabus_path and os.path.exists(syllabus_path):
            with open(syllabus_path, "r") as f:
                syllabus_text = f.read()
        else:
            syllabus_text = "No syllabus available."
        
        # Use the course description from the course record.
        course_description = self.course.get("description", "No description available.")
        
        # RAG steps: chunk the syllabus, create FAISS index, and retrieve relevant context.
        chunks = self.chunk_text(syllabus_text)
        if chunks:
            index, _, chunks = await self.create_faiss_index(chunks)
            retrieved_context = await self.retrieve_chunks(user_query, index, chunks)
        else:
            retrieved_context = []
        
        prompt = self.build_prompt(user_query, retrieved_context, course_description)
        answer = await self.generate_response(prompt)
        return answer

class AgenticSwarm:
    def __init__(self, courses_file, **kwargs):
        self.courses_file = courses_file
        with open(courses_file, "r") as f:
            self.courses = json.load(f)
        self.kwargs = kwargs

    async def run_swarm(self, user_query, filtered_courses=None):
        if (len(filtered_courses) > 10):
            return
        courses_to_process = filtered_courses if filtered_courses is not None else self.courses
        results = {}
        # Process each course sequentially.
        for course in courses_to_process:
            bot = CourseBot(course, **self.kwargs)
            answer = await bot.answer_query(user_query)
            results[course.get("id")] = answer
        return results

# Example usage:
async def main():
    #openai.api_key = os.environ.get("API_TOKEN")
    openai.api_key = "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"
    swarm = AgenticSwarm("courses/courses.json", embedding_model="text-embedding-ada-002", chat_model="gpt-4-turbo", top_k=2)
    user_query = "do you think this class will add a lot to my work schedule?"
    results = await swarm.run_swarm(user_query)
    for course_id, answer in results.items():
        print(f"Course {course_id}:\n{answer}\n")

if __name__ == "__main__":
    asyncio.run(main())
