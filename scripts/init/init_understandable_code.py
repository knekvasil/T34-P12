import pandas as pd
from difflib import SequenceMatcher

# Read in data
activity_log_a = pd.read_csv("activity_log_A(in).csv", delimiter=",")
activity_log_b = pd.read_csv("activity_log_B(in).csv", delimiter=",")
grades_a = pd.read_csv("grades_A(in).csv", delimiter=",")
grades_b = pd.read_csv("grades_B(in).csv", delimiter=",")

# Define activities
langs = {
    "English": "eng",
    "Estonian": "est"
}
exams = {
    "final": "fin_exam",
    "midterm": "mid_exam"
}
hws = range(1,16)
hw_funs = [
    lambda N, lang: f"Joined Week {N} lecture online",
    lambda N, lang: f"Watched Week {N} lecture recording",
    lambda N, lang: f"Watched past years' Week {N} lecture recording",
    lambda N, lang: f"Viewed Week {N} lecture slides",
    lambda N, lang: f"Viewed Week {N} study materials in {lang}",
    lambda N, lang: f"Started Homework {N} in {lang}",
    lambda N, lang: f"Submitted Homework {N} in {lang}",
    lambda N, lang: f"Practiced submitting the homework in {lang}",
    lambda N, lang: f"Viewed sample solutions of Homework {N}",
    lambda N, lang: f"Viewed the feedback of Homework {N} in {lang}"
]
exam_funs = [
    lambda exam, lang:"Viewed past years' exams",
    lambda exam, lang:"Viewed the midterm exam review quiz",
    lambda exam, lang : f"Viewed the feedback on the {exam}",
    lambda exam, lang : f"Viewed final/midterm exam tasks after the {exam} in {lang}",
    lambda exam, lang : f"Viewed sample solutions of the {exam}"
]
other_funs = [
    lambda :"Viewed the course information page",
    lambda :"Read a post in the announcements forum",
    lambda :"Viewed the dictionary of terms"
]
# Create activities
rows = set()
for lang in langs.keys():
    for exam in exams.keys():
        for fun in exam_funs:
            rows.add(fun(exam, lang))
    for hw in hws:
        for fun in hw_funs:
            rows.add(fun(hw, lang))

for fun in other_funs:
    rows.add(fun())

rows = list(rows)

# Find closest activity
def find_best_match(s):
    best_ratio = 0.0
    best_match = ""
    for row in rows:
        if s == row:
            return row
        ratio = SequenceMatcher(None, s, row).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = row
    return best_match

# Find unique activities
unique_activities = activity_log_a["Activity"].unique()
# For each activity, find what activity is closest to it (string-wise).
mapping = {}
for activity in unique_activities:
    mapping[activity] = find_best_match(activity)
# Map the closest values to the current values
activity_log_a["Activity"] = activity_log_a["Activity"].apply(lambda x : mapping[x])
# Do it again on b
unique_activities = activity_log_b["Activity"].unique()
mapping = {}
for activity in unique_activities:
    mapping[activity] = find_best_match(activity)
activity_log_b["Activity"] = activity_log_b["Activity"].apply(lambda x : mapping[x])

# Create mapping functions to map long sentences to short ones
hw_mapping_funs = [
    lambda N, lang: (f"Joined Week {N} lecture online", f"{N} online"),
    lambda N, lang: (f"Watched Week {N} lecture recording", f"{N} video"),
    lambda N, lang: (f"Watched past years' Week {N} lecture recording", f"{N} old_video"),
    lambda N, lang: (f"Viewed Week {N} lecture slides", f"{N} slides"),
    lambda N, lang: (f"Viewed Week {N} study materials in {lang}", f"{N} materials {langs[lang]}"),
    lambda N, lang: (f"Started Homework {N} in {lang}", f"{N} start {langs[lang]}"),
    lambda N, lang: (f"Submitted Homework {N} in {lang}", f"{N} submit {langs[lang]}"),
    lambda N, lang: (f"Practiced submitting the homework in {lang}", f"test_submit {langs[lang]}"),
    lambda N, lang: (f"Viewed sample solutions of Homework {N}", f"{N} solution"),
    lambda N, lang: (f"Viewed the feedback of Homework {N} in {lang}", f"{N} feedback {langs[lang]}")
]
exam_mapping_funs = [
    lambda exam, lang:("Viewed past years' exams", "old_exam"),
    lambda exam, lang:("Viewed the midterm exam review quiz", "mid_exam quiz"),
    lambda exam, lang : (f"Viewed the feedback on the {exam}", f"{exam} feedback"),
    lambda exam, lang : (f"Viewed final/midterm exam tasks after the {exam} in {lang}", f"{exam} tasks {langs[lang]}"),
    lambda exam, lang : (f"Viewed sample solutions of the {exam}", f"{exam} solution")
]
other_mapping_funs = [
    lambda :("Viewed the course information page", "info"),
    lambda :("Read a post in the announcements forum", "forum"),
    lambda :("Viewed the dictionary of terms", "terms")
]

# Create the actual pairs
mappings = {}
for lang in langs.keys():
    for exam in exams.keys():
        for fun in exam_mapping_funs:
            key, val = fun(exam, lang)
            mappings[key] = val
    for hw in hws:
        for fun in hw_mapping_funs:
            key, val = fun(hw, lang)
            mappings[key] = val

for fun in other_mapping_funs:
    key, val = fun()
    mappings[key] = val
# Map the values
activity_log_a["Activity"] = activity_log_a["Activity"].apply(lambda x : mappings[x])
activity_log_b["Activity"] = activity_log_b["Activity"].apply(lambda x : mappings[x])
