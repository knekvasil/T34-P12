import os
import argparse
import pandas as pd
from scripts.grades_consolidator import consolidate_grades
from scripts.activity_consolidator import consolidate_activity


def run_grades_consolidation(input_dir="data/original", output_dir="data/new"):
    """Run grades consolidation for all grade-related CSVs."""
    files = [
        f
        for f in os.listdir(input_dir)
        if f.startswith("grades") and f.endswith(".csv")
    ]
    for file_name in files:
        input_file = os.path.join(input_dir, file_name)
        output_file = os.path.join(output_dir, file_name)
        print(f"Processing {file_name} with grades consolidator...")
        consolidate_grades(input_file, output_file)
        print(
            f"Grades consolidation complete for {file_name}. Output saved to {output_file}"
        )


def run_activity_consolidation(input_dir="data/original", output_dir="data/new"):
    """Run activity log consolidation for all activity-related CSVs."""
    files = [
        f
        for f in os.listdir(input_dir)
        if f.startswith("activity_log") and f.endswith(".csv")
    ]
    for file_name in files:
        input_file = os.path.join(input_dir, file_name)
        output_file = os.path.join(output_dir, file_name)
        print(f"Processing {file_name} with activity consolidator...")
        consolidate_activity(input_file, output_file)
        print(
            f"Activity consolidation complete for {file_name}. Output saved to {output_file}"
        )


def merge_csvs(output_dir="data/new", merge_type="grades"):
    """Merge all CSVs of the given type ('grades' or 'activity') in the output_dir into a single file."""
    csv_type = "grades" if merge_type == "grades" else "activity_log"
    files = [
        f
        for f in os.listdir(output_dir)
        if f.startswith(csv_type) and f.endswith(".csv")
    ]

    if not files:
        print(f"No {merge_type} CSV files found to merge.")
        return

    # Merge all relevant CSVs into one DataFrame
    df_list = []
    for file_name in files:
        file_path = os.path.join(output_dir, file_name)
        df_list.append(pd.read_csv(file_path))

    merged_df = pd.concat(df_list)
    merged_output_file = os.path.join(output_dir, f"{merge_type}.csv")

    # Save merged CSV
    merged_df.to_csv(merged_output_file, index=False)
    print(f"Merged {merge_type} CSVs into {merged_output_file}")

    # Remove the individual CSVs after merging
    for file_name in files:
        file_path = os.path.join(output_dir, file_name)
        os.remove(file_path)
        print(f"Removed {file_path} after merging.")


def run_all_consolidations(consolidation_type="both", merge=False):
    """Runs consolidation based on the type and optionally merges the results."""
    input_dir = "data/original"
    output_dir = "data/new"

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if consolidation_type == "grades":
        run_grades_consolidation(input_dir, output_dir)
        if merge:
            merge_csvs(output_dir, merge_type="grades")
    elif consolidation_type == "activity":
        run_activity_consolidation(input_dir, output_dir)
        if merge:
            merge_csvs(output_dir, merge_type="activity_log")
    elif consolidation_type == "both":
        run_grades_consolidation(input_dir, output_dir)
        run_activity_consolidation(input_dir, output_dir)
        if merge:
            merge_csvs(output_dir, merge_type="grades")
            merge_csvs(output_dir, merge_type="activity_log")
    else:
        print(
            f"Error: Unknown type '{consolidation_type}'. Use --help for valid options."
        )
        exit(1)

    print("All consolidations complete.")


def main():
    """Parse command-line arguments and run the appropriate consolidation."""
    parser = argparse.ArgumentParser(
        description="Run data consolidation for grades and activity logs."
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["grades", "activity", "both"],
        help="Specify which consolidation to run: 'grades', 'activity', or 'both'.",
    )
    parser.add_argument(
        "--merge",
        type=bool,
        default=False,
        help="Specify whether to merge all consolidated CSVs into a single file per type.",
    )

    args = parser.parse_args()

    if args.merge and not args.type:
        # If only merge is requested without a consolidation type, just perform merging
        merge_csvs(output_dir="data/new", merge_type="grades")
        merge_csvs(output_dir="data/new", merge_type="activity_log")
    else:
        # Run the consolidations and optionally merge the output
        run_all_consolidations(consolidation_type=args.type, merge=args.merge)


if __name__ == "__main__":
    main()
