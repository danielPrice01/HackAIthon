---
sdk: gradio
app_file: app.py
---

# Ask @ Penn

Ask @ Penn is a modular application designed to make finding courses as easy as it should be. The project integrates several functionalities such as user input filtering, course query handling, multi-agent (swarm) management, and an interactive chat interface.

## Features

- **Filter Courses:**  
  Use natural language to filter down courses you're interested in instead of dealing with complex course attributes and filters.
  
- **Generate Attributes:**  
  Create custom AI-powered attributes to get granular information about the courses you're interested in.

## File Structure

- **app.py**  
  The main entry point of the application. This file integrates all modules and initializes the interactive chat system.

- **filter.py**  
  Contains functions and logic for filtering and processing user inputs to ensure data integrity and proper handling.

- **course_bot.py**  
  Implements the logic specific to course-related inquiries. This module processes user questions about courses and returns relevant information.

- **swarm.py**  
  Manages a group (swarm) of agents. This is useful for handling parallel processes, load balancing, or coordinating multiple service instances.

- **interactive_chat.py**  
  Provides the interactive chat functionality that allows users to communicate with the bot in real time.


## Contact

  For questions, feedback, or further information, please contact daprice@seas, darshk@seas, or tanaytan@seas
