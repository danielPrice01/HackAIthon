#!/usr/bin/env python3
import json
import os

from courses.labels.labels import label_keywords  # Ensure filter.py contains your thorough label_keywords dictionary

def assign_labels(course_text, label_dict):
    """
    Given course_text (string) and a dictionary mapping labels to keywords,
    return a list of matching labels.
    """
    text = course_text.lower()
    assigned = []
    for label, keywords in label_dict.items():
        for keyword in keywords:
            if keyword.lower() in text:
                assigned.append(label)
                break  # No need to check more keywords once label is matched
    return assigned

def load_course_text(course, syllabus_base_dir="courses/syllabi"):
    """
    Combines the course description and syllabus text (if available).
    Adjusts the file path if the syllabus path already includes the base directory.
    """
    text = course.get("description", "")
    syllabus_path = course.get("syllabus", "").strip()
    
    if syllabus_path:
        # If the syllabus_path already starts with the base directory, use it as is
        if syllabus_path.startswith(syllabus_base_dir):
            full_path = syllabus_path
        else:
            full_path = os.path.join(syllabus_base_dir, syllabus_path)
            
        if os.path.exists(full_path):
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    syllabus_text = f.read()
                text += "\n" + syllabus_text
            except Exception as e:
                print(f"Error reading syllabus for {course.get('id', 'Unknown')}: {e}")
        else:
            print(f"Warning: Syllabus file {full_path} not found for course {course.get('id', 'Unknown')}")
    
    return text

def main():
    # Load courses from JSON (adjust the path if necessary)
    json_filename = os.path.join("courses", "courses.json")
    with open(json_filename, "r", encoding="utf-8") as f:
        courses = json.load(f)
    
    # Output file for the component snippets
    output_filename = "labeled_components.txt"
    
    with open(output_filename, "w", encoding="utf-8") as out_file:
        for course in courses:
            course_id = course.get("id", "Unknown")
            
            # Combine description and syllabus text
            course_text = load_course_text(course, syllabus_base_dir="courses/syllabi")
            
            # Assign labels based on keywords
            labels = assign_labels(course_text, label_keywords)
            
            # Build output in the requested format:
            # e.g., CIS 0099 Labels = "labels": ["Operating Systems", "Computer Networks", ...]
            line = f'{course_id} Labels = \n"labels": {json.dumps(labels)}\n\n'
            out_file.write(line)
    
    print(f"Done! Labeled component lines written to {output_filename}.")

if __name__ == "__main__":
    main()
