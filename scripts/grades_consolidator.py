import csv


def consolidate_grades(input_file, output_file):
    """Consolidates the homework, midterm, and final exam grades in the given CSV."""
    with open(input_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        _ = next(reader)  # Read header

        # Create new header by eliminating duplicate columns
        new_header = ["Student", "Total", "Grade"]
        for i in range(1, 13):
            new_header.insert(i, f"Homework {i}")
        new_header.insert(13, "Midterm exam")
        new_header.insert(14, "Final exam")

        # Prepare to write the output CSV file
        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(new_header)

            # Process each student's data
            for row in reader:
                student_id = row[0]
                homeworks = []
                for i in range(1, 13):
                    en_col = row[2 * i - 1]  # English version
                    ee_col = row[2 * i]  # Estonian version
                    hw_max = max(
                        float(en_col) if en_col != "-" else 0,
                        float(ee_col) if ee_col != "-" else 0,
                    )
                    homeworks.append(hw_max if hw_max > 0 else "-")

                # Handle midterms (consolidating all into one column)
                midterm = max(
                    float(row[25]) if row[25] != "-" else 0,
                    float(row[26]) if row[26] != "-" else 0,
                    float(row[27]) if row[27] != "-" else 0,
                    float(row[28]) if row[28] != "-" else 0,
                )

                # Handle finals (consolidating all into one column)
                final_exam = max(
                    float(row[29]) if row[29] != "-" else 0,
                    float(row[30]) if row[30] != "-" else 0,
                    float(row[31]) if row[31] != "-" else 0,
                    float(row[32]) if row[32] != "-" else 0,
                )

                # Handle bonus column: Check if it exists and ignore
                total_index = len(row) - 2
                total = row[total_index]
                grade = row[total_index + 1]

                # Write the consolidated row to the output CSV file
                writer.writerow(
                    [student_id] + homeworks + [midterm, final_exam, total, grade]
                )
