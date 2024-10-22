import pandas as pd
from difflib import SequenceMatcher

activity_log_a = pd.read_csv("activity_log_A(in).csv", delimiter=",")
activity_log_b = pd.read_csv("activity_log_B(in).csv", delimiter=",")
grades_a = pd.read_csv("grades_A(in).csv", delimiter=",")
grades_b = pd.read_csv("grades_B(in).csv", delimiter=",")

langs = {"English": "eng","Estonian": "est"}
exams = {"final": "fin_exam","midterm": "mid_exam"}
hw_funs = [lambda N, lang: f"Joined Week {N} lecture online",lambda N, lang: f"Watched Week {N} lecture recording",lambda N, lang: f"Watched past years' Week {N} lecture recording",lambda N, lang: f"Viewed Week {N} lecture slides",lambda N, lang: f"Viewed Week {N} study materials in {lang}",lambda N, lang: f"Started Homework {N} in {lang}",lambda N, lang: f"Submitted Homework {N} in {lang}",lambda N, lang: f"Practiced submitting the homework in {lang}",lambda N, lang: f"Viewed sample solutions of Homework {N}",lambda N, lang: f"Viewed the feedback of Homework {N} in {lang}"]
exam_funs = [lambda exam, lang:"Viewed past years' exams",lambda exam, lang:"Viewed the midterm exam review quiz",lambda exam, lang : f"Viewed the feedback on the {exam}",lambda exam, lang : f"Viewed final/midterm exam tasks after the {exam} in {lang}",lambda exam, lang : f"Viewed sample solutions of the {exam}"]
other_funs = [lambda :"Viewed the course information page",lambda :"Read a post in the announcements forum",lambda :"Viewed the dictionary of terms"]

rows = list(set([ fun(exam, lang) for exam in exams.keys() for lang in langs.keys() for fun in exam_funs] + [ fun(hw, lang) for hw in range(1, 16) for lang in langs.keys() for fun in hw_funs] + [fun() for fun in other_funs]))
def fix_typos(df):
    mapping = {}
    for activity in df["Activity"].unique():
        mapping[activity] = (lambda s: max([(SequenceMatcher(None, s, row).ratio(), row) for row in rows], key=lambda x : x[0])[1])(activity)
    df["Activity"] = df["Activity"].apply(lambda x : mapping[x])
fix_typos(activity_log_a)
fix_typos(activity_log_b)

hw_mapping_funs = [lambda N, lang: f"{N} online",lambda N, lang: f"{N} video",lambda N, lang: f"{N} old_video",lambda N, lang: f"{N} slides",lambda N, lang: f"{N} materials {langs[lang]}",lambda N, lang: f"{N} start {langs[lang]}",lambda N, lang: f"{N} submit {langs[lang]}",lambda N, lang: f"test_submit {langs[lang]}",lambda N, lang: f"{N} solution",lambda N, lang: f"{N} feedback {langs[lang]}"]
exam_mapping_funs = [lambda exam, lang: "old_exam",lambda exam, lang: "mid_exam quiz",lambda exam, lang: f"{exam} feedback",lambda exam, lang: f"{exam} tasks {langs[lang]}",lambda exam, lang: f"{exam} solution"]
other_mapping_funs = [lambda :"info",lambda :"forum",lambda :"terms"]

mappings = dict([(fun1(exam, lang), fun2(exam, lang)) for exam in exams.keys() for lang in langs.keys() for fun1, fun2 in zip(exam_funs, exam_mapping_funs)] + [(fun1(hw, lang), fun2(hw, lang)) for hw in range(1, 16) for lang in langs.keys() for fun1, fun2 in zip(hw_funs, hw_mapping_funs)] + [(fun1(), fun2()) for fun1, fun2 in zip(other_funs, other_mapping_funs)])

activity_log_a["Activity"] = activity_log_a["Activity"].apply(lambda x : mappings[x])
activity_log_b["Activity"] = activity_log_b["Activity"].apply(lambda x : mappings[x])
