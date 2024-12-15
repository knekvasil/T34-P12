import csv
from collections import defaultdict
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import linregress


def consolidate_activity(input_file, output_file, grades_file="grades.csv"):
    # Initialize a dictionary to store activity counters and trends for each student
    student_activity = defaultdict(
        lambda: {
            "Week Lecture Recordings Watched": 0,
            "Past Years' Week Lecture Recordings Watched": 0,
            "Week Lecture Slides Viewed": 0,
            "Week Study Materials Viewed": 0,
            "Dictionary of Terms Viewed": 0,
            "Homework Started": 0,
            "Homework Submitted": 0,
            "Homework Sample Solutions Viewed": 0,
            "Homework Feedback Viewed": 0,
            "Past Years' Exams Viewed": 0,
            "Midterm Exam Review Quiz Viewed": 0,
            "Midterm Exam Feedback Viewed": 0,
            "Midterm Exam Sample Solutions Viewed": 0,
            "Other Activities": 0,
            "Weekly Activity Counts": [],
            "Last Activity Timestamp": None,  # To track the previous activity timestamp
            "Timeliness Scores": [],  # Differences between activity times
        }
    )

    # Assume the course starts on a base date (e.g., January 1, 2024)
    base_date = datetime(2024, 1, 1)

    # Open the input CSV file and read its contents
    with open(input_file, mode="r") as file:
        reader = csv.DictReader(file)

        # Loop through each row in the CSV
        for row in reader:
            student_id = row["Student"]  # The student identifier
            activity = row["Activity"]  # The activity name

            # Parse the timestamp
            try:
                activity_date = base_date + timedelta(days=int(row["Day"]) - 1)
                timestamp = datetime.combine(
                    activity_date, datetime.strptime(row["Time"], "%H:%M:%S").time()
                )
            except Exception as e:
                print(f"Error log: {row}")
                print(f"Exception: {e}")
                continue

            # Track timeliness between activities
            last_time = student_activity[student_id]["Last Activity Timestamp"]
            if last_time is not None:
                time_diff = (timestamp - last_time).total_seconds()
                student_activity[student_id]["Timeliness Scores"].append(time_diff)
            student_activity[student_id]["Last Activity Timestamp"] = timestamp

            # Determine the week number (1-based index)
            week_number = (activity_date - base_date).days // 7 + 1

            # Ensure the "Weekly Activity Counts" list is long enough
            while (
                len(student_activity[student_id]["Weekly Activity Counts"])
                < week_number
            ):
                student_activity[student_id]["Weekly Activity Counts"].append(0)

            # Increment the weekly activity count
            student_activity[student_id]["Weekly Activity Counts"][week_number - 1] += 1

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
            elif "Viewed the dictionary of terms" in activity:
                student_activity[student_id]["Dictionary of Terms Viewed"] += 1
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

    grades_dict = prepare_grades_data(grades_file)

    # Open the output CSV file and write the consolidated data
    with open(output_file, mode="w", newline="") as file:
        fieldnames = [
            "Student",
            "Week Lecture Recordings Watched",
            "Past Years' Week Lecture Recordings Watched",
            "Week Lecture Slides Viewed",
            "Week Study Materials Viewed",
            "Dictionary of Terms Viewed",
            "Homework Started",
            "Homework Submitted",
            "Homework Sample Solutions Viewed",
            "Homework Feedback Viewed",
            "Past Years' Exams Viewed",
            "Midterm Exam Review Quiz Viewed",
            "Midterm Exam Feedback Viewed",
            "Midterm Exam Sample Solutions Viewed",
            "Other Activities",
            "Total Weekly Activities",
            "Average Weekly Activity",
            "Peak Activity Week",
            "Week of Peak Activity",
            "Activity Volatility",
            "Proportion of Inactive Weeks",
            "Trend Slope",
            "Activity Concentration",
            "Activity Momentum",
            "Homework Completion Ratio",
            "Engagement Breadth",
            "Consistency Score",
            "Average Timeliness",
            "Total",
            "Grade",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        # Write each student's consolidated activity data
        for student_id, activities in student_activity.items():
            weekly_counts = activities.pop("Weekly Activity Counts")
            timeliness_scores = activities.pop("Timeliness Scores")

            # Calculate derived features
            total_weekly_activities = sum(weekly_counts)
            average_weekly_activity = np.mean(weekly_counts) if weekly_counts else 0
            peak_activity = max(weekly_counts) if weekly_counts else 0
            week_of_peak_activity = (
                weekly_counts.index(peak_activity) + 1 if peak_activity > 0 else 0
            )
            activity_volatility = np.std(weekly_counts) if weekly_counts else 0
            proportion_inactive_weeks = (
                weekly_counts.count(0) / len(weekly_counts) if weekly_counts else 0
            )
            trend_slope = (
                linregress(range(1, len(weekly_counts) + 1), weekly_counts).slope
                if len(weekly_counts) > 1
                else 0
            )
            activity_concentration = (
                peak_activity / total_weekly_activities
                if total_weekly_activities > 0
                else 0
            )
            activity_momentum = (
                weekly_counts[-1] - weekly_counts[0] if len(weekly_counts) > 1 else 0
            )
            homework_completion_ratio = (
                activities["Homework Submitted"] / activities["Homework Started"]
                if activities["Homework Started"] > 0
                else 0
            )

            # Update engagement_breadth calculation to exclude non-numeric values
            engagement_breadth = sum(
                1 for v in activities.values() if isinstance(v, (int, float)) and v > 0
            )

            consistency_score = np.std(weekly_counts) if weekly_counts else 0
            average_timeliness = (
                np.mean(timeliness_scores) if len(timeliness_scores) > 0 else 0
            )

            # Parse grades for prediction
            grade_info = grades_dict.get(student_id, {"Total": 0, "Grade": "-"})

            # Add derived features to the row
            activities.update(
                {
                    "Total Weekly Activities": total_weekly_activities,
                    "Average Weekly Activity": average_weekly_activity,
                    "Peak Activity Week": peak_activity,
                    "Week of Peak Activity": week_of_peak_activity,
                    "Activity Volatility": activity_volatility,
                    "Proportion of Inactive Weeks": proportion_inactive_weeks,
                    "Trend Slope": trend_slope,
                    "Activity Concentration": activity_concentration,
                    "Activity Momentum": activity_momentum,
                    "Homework Completion Ratio": homework_completion_ratio,
                    "Engagement Breadth": engagement_breadth,
                    "Consistency Score": consistency_score,
                    "Average Timeliness": average_timeliness,
                    "Total": grade_info["Total"],
                    "Grade": grade_info["Grade"],
                }
            )
            activities.pop("Last Activity Timestamp", None)

            writer.writerow({"Student": student_id, **activities})


def prepare_grades_data(grades_file):
    """
    Read and preprocess grades data.

    Args:
        grades_file (str): Path to grades CSV file

    Returns:
        dict: Processed grades information keyed by student ID
    """
    grades_dict = {}
    with open(grades_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_id = row["Student"]
            grades_dict[student_id] = {
                "Total": float(row["Total"]) if row["Total"] != "-" else 0,
                "Grade": row["Grade"] if row["Grade"] != "-" else "F",
            }
    return grades_dict
