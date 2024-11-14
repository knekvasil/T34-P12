import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def generate_student_activity_boxplot(csv_file, output_folder="./"):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Set the 'Student' column as the index (optional, for easier identification)
    data.set_index("Student", inplace=True)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Generate the box plot for all activity columns
    plt.figure(figsize=(14, 8))  # Increase width if necessary
    sns.boxplot(data=data)
    plt.title("Distribution of Student Activity Levels")
    plt.xlabel("Activity")
    plt.ylabel("Frequency of Engagement")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")  # Tilt labels at 45 degrees

    # Save the plot as a PNG file in the specified output folder
    plt.savefig(
        os.path.join(output_folder, "student_activity_boxplot.png"), bbox_inches="tight"
    )
    plt.close()

    print(f"Box plot saved as 'student_activity_boxplot.png' in '{output_folder}'.")


# Example usage:
generate_student_activity_boxplot("../../data/new/activity_log.csv", "./")


def generate_homework_feedback_histogram(csv_file, output_folder="./"):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Set the 'Student' column as the index (optional, for easier identification)
    data.set_index("Student", inplace=True)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Generate the histogram for the 'Homework Feedback Viewed' column without the trend line
    plt.figure(figsize=(10, 6))
    sns.histplot(
        data["Homework Feedback Viewed"], bins=10, kde=False
    )  # kde=False removes the trend line
    plt.title("Example Feature Outlier")
    plt.xlabel("Feature")
    plt.ylabel("Frequency")

    # Save the plot as a PNG file in the specified output folder
    plt.savefig(
        os.path.join(output_folder, "homework_feedback_histogram.png"),
        bbox_inches="tight",
    )
    plt.close()

    print(f"Histogram saved as 'homework_feedback_histogram.png' in '{output_folder}'.")


# Example usage:
generate_homework_feedback_histogram("../../data/new/activity_log.csv", "./")
