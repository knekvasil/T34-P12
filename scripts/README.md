# Clean Data Tool

`clean_data.py` is a command-line tool for consolidating CSV files related to student grades and activity logs. It processes files stored in the `data/original` directory and outputs consolidated results to the `data/new` directory. Additionally, the tool can merge consolidated files of the same type into a single CSV file and clean up the intermediate files.

## Features

- **Consolidation of Grades and Activity Logs**: 
  The tool processes CSV files for either grades or activity logs. It consolidates data across multiple columns and produces a streamlined CSV file for each category.
  
- **Merge Functionality**:
  Optionally merge all `grades` or `activity_log` CSVs into a single consolidated file.
  
- **Clean-up After Merge**:
  After merging files into a single CSV, the tool deletes the individual CSVs to ensure a clean directory structure.

## Directory Structure

The tool expects the following directory structure:
```
data/
  ├── original/    # Contains the original CSV files to be processed
  └── new/         # Stores the consolidated and/or merged CSV files
```

## Installation

1. Clone the repository or download the `clean_data.py` script.
2. Install required dependencies (e.g., `pandas`) using:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the `clean_data.py` script using the following options:

### Consolidation

You can choose to consolidate either "grades", "activity", or both types of CSV files.

- **Consolidate Grades:**
  ```bash
  python clean_data.py --type grades
  ```

- **Consolidate Activity Logs:**
  ```bash
  python clean_data.py --type activity
  ```

- **Consolidate Both:**
  ```bash
  python clean_data.py --type both
  ```

### Merging CSVs

You can optionally merge the consolidated CSVs into a single file per type (grades or activity) by adding the `--merge true` flag. This can be done after running a consolidation or as a standalone action.

- **Consolidate and Merge Grades:**
  ```bash
  python clean_data.py --type grades --merge true
  ```

- **Consolidate and Merge Activity Logs:**
  ```bash
  python clean_data.py --type activity --merge true
  ```

- **Consolidate Both and Merge:**
  ```bash
  python clean_data.py --type both --merge true
  ```

- **Merge Existing Files Only** (without running any new consolidations):
  ```bash
  python clean_data.py --merge true
  ```

### Help

To see the available options, you can run:
```bash
python clean_data.py --help
```

### Command Line Parameters

| Parameter        | Type    | Description                                                                                      | Example                       |
|------------------|---------|--------------------------------------------------------------------------------------------------|-------------------------------|
| `--type`         | string  | Specifies the type of consolidation to perform. Options: `grades`, `activity`, `both`.            | `--type grades`               |
| `--merge`        | boolean | Optional flag to merge consolidated CSVs into a single file. Default is `False`.                  | `--merge true`                |

### Notes

- Files starting with "grades" are processed by the grades consolidation logic.
- Files starting with "activity_log" are processed by the activity log consolidation logic.
- The tool will automatically merge files in the `data/new` directory when the `--merge` flag is set, then remove the individual CSVs that were merged.

## Output

The consolidated and/or merged CSV files are saved in the `data/new` directory. For example:
- `grades.csv`
- `activity_log.csv`

If the `--merge true` flag is used, all non-merged CSVs will be deleted, leaving only the final merged files.

## Example Workflows

1. **Consolidating Grades Only**:
   ```bash
   python clean_data.py --type grades
   ```
   This processes all grade-related CSV files in `data/original` and outputs them to `data/new`.

2. **Merging Activity Logs Only**:
   ```bash
   python clean_data.py --merge true
   ```
   This merges any activity log CSVs found in the `data/new` directory into a single file and deletes the individual files.

3. **Consolidating and Merging All Data**:
   ```bash
   python clean_data.py --type both --merge true
   ```
   This consolidates both grades and activity logs, merges the results into single files for each type, and deletes the individual consolidated files.
