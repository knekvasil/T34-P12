import csv
from collections import defaultdict


# TODO: Implement
def consolidate_activity(input_file, output_file):
    # Initialize a dictionary to store activity counters for each student
    student_activity = defaultdict(
        lambda: {
            "Week Lecture Recordings Watched": 0,
            "Past Years' Week Lecture Recordings Watched": 0,
            "Week Lecture Slides Viewed": 0,
            "Week Study Materials Viewed": 0,
            "Homework Started": 0,
            "Homework Submitted": 0,
            "Homework Sample Solutions Viewed": 0,
            "Homework Feedback Viewed": 0,
            "Past Years' Exams Viewed": 0,
            "Midterm Exam Review Quiz Viewed": 0,
            "Midterm Exam Feedback Viewed": 0,
            "Midterm Exam Sample Solutions Viewed": 0,
            "Other Activities": 0,
        }
    )

    # Open the input CSV file and read its contents
    with open(input_file, mode="r") as file:
        reader = csv.DictReader(file)

        # Loop through each row in the CSV
        for row in reader:
            student_id = row["Student"]  # The student identifier
            activity = row["Activity"]  # The activity name

            # Map activity types to the appropriate counter
            if "Watched Week" in activity and "lecture recording" in activity:
                student_activity[student_id]["Week Lecture Recordings Watched"] += 1
            elif "Watched past years'" in activity and "lecture recording" in activity:
                student_activity[student_id][
                    "Past Years' Week Lecture Recordings Watched"
                ] += 1
            elif "Viewed Week" in activity and "lecture slides" in activity:
                student_activity[student_id]["Week Lecture Slides Viewed"] += 1
            elif "Viewed Week" in activity and "study materials" in activity:
                student_activity[student_id]["Week Study Materials Viewed"] += 1
            elif "Started Homework" in activity:
                student_activity[student_id]["Homework Started"] += 1
            elif "Submitted Homework" in activity:
                student_activity[student_id]["Homework Submitted"] += 1
            elif "Viewed sample solutions of Homework" in activity:
                student_activity[student_id]["Homework Sample Solutions Viewed"] += 1
            elif "Viewed the feedback on Homework" in activity:
                student_activity[student_id]["Homework Feedback Viewed"] += 1
            elif "Viewed past years' exams" in activity:
                student_activity[student_id]["Past Years' Exams Viewed"] += 1
            elif "Viewed the midterm exam review quiz" in activity:
                student_activity[student_id]["Midterm Exam Review Quiz Viewed"] += 1
            elif "Viewed the feedback on the midterm exam" in activity:
                student_activity[student_id]["Midterm Exam Feedback Viewed"] += 1
            elif "Viewed sample solutions of the midterm exam" in activity:
                student_activity[student_id][
                    "Midterm Exam Sample Solutions Viewed"
                ] += 1
            else:
                student_activity[student_id]["Other Activities"] += 1

    # Open the output CSV file and write the consolidated data
    with open(output_file, mode="w", newline="") as file:
        fieldnames = [
            "Student",
            "Week Lecture Recordings Watched",
            "Past Years' Week Lecture Recordings Watched",
            "Week Lecture Slides Viewed",
            "Week Study Materials Viewed",
            "Homework Started",
            "Homework Submitted",
            "Homework Sample Solutions Viewed",
            "Homework Feedback Viewed",
            "Past Years' Exams Viewed",
            "Midterm Exam Review Quiz Viewed",
            "Midterm Exam Feedback Viewed",
            "Midterm Exam Sample Solutions Viewed",
            "Other Activities",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        # Write each student's consolidated activity data
        for student_id, activities in student_activity.items():
            writer.writerow({"Student": student_id, **activities})
