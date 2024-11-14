import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def generate_grade_distribution(csv_file, output_folder):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Filter out rows with missing 'Total' or 'Grade' values
    data = data.dropna(subset=["Total", "Grade"])

    # Convert 'Total' to numeric, coercing errors if there are non-numeric values
    data["Total"] = pd.to_numeric(data["Total"], errors="coerce")

    # Drop rows where 'Total' or 'Grade' is NaN after conversion
    data = data.dropna(subset=["Total", "Grade"])

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Plot the distribution of 'Total' scores and save as PNG
    plt.figure(figsize=(10, 6))
    sns.histplot(data["Total"], bins=10, kde=True)
    plt.title("Grade Distribution by Total Score")
    plt.xlabel("Total Score")
    plt.ylabel("Number of Students")
    plt.savefig(os.path.join(output_folder, "total_score_distribution.png"))
    plt.close()

    # Plot the count of each letter grade and save as PNG
    plt.figure(figsize=(8, 5))
    sns.countplot(x="Grade", data=data, order=["A", "B", "C", "D", "E", "F"])
    plt.title("Distribution of Grades")
    plt.xlabel("Grade")
    plt.ylabel("Number of Students")
    plt.savefig(os.path.join(output_folder, "letter_grade_distribution.png"))
    plt.close()

    print(f"Distribution charts saved in '{output_folder}'.")


# Example usage:
generate_grade_distribution("../../data/new/grades.csv", "./")
