# Initialization file for colab notebooks
Put the following code block at the beginning of your notebook to get the data:
```
!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/data/original/activity_log_A(in).csv"
!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/data/original/activity_log_B(in).csv"
!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/data/original/grades_A(in).csv"
!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/data/original/grades_B(in).csv"

!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/scripts/init/init.py"
%run 'init.py'
```

or alternatively, run the understandable code one, because it is understandable and if any edits will go in, I do not think I will be changing the first one.
```
!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/data/original/activity_log_A(in).csv"
!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/data/original/activity_log_B(in).csv"
!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/data/original/grades_A(in).csv"
!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/data/original/grades_B(in).csv"

!wget -nc -q --show-progress "https://raw.githubusercontent.com/knekvasil/T34-P12/refs/heads/main/scripts/init/init_understandable_code.py"
%run 'init_understandable_code.py'
```

This will run download the data, download the init.py file and run it. <br>
init.py will:
1. Fix typos in activities
2. Replace bulky activity sentences with short sentences in the following format:
   * what (homework number/fin_exam/mid_exam)
   * specifier (video/recording/slides/submit/etc.)
   * language (est/eng)
3. Some do not have all the values, so those won't be shown (specifier is still there)
4. Leave you with 4 Pandas DataFrames:
   * activity_log_a
   * activity_log_b
   * grades_a
   * grades_b
5. These DataFrames do not need to be imported and can be used right away.
