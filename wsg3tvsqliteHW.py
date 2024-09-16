import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

connection = sqlite3.connect('student_grades.db')
cursor = connection.cursor()

# Create Students and Grades Tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Grades (
        grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        grade INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(student_id))''')

# Insert information into Students and Grades Tables
Students = [
    ('Alice', 'Johnson'),
    ('Bob', 'Smith'),
    ('Carol', 'White'),
    ('David', 'Brown'),
    ('Eve', 'Davis')]

Grades = [
    (1, 'Math', 95),
    (1, 'English', 88),
    (1, 'History', 90),
    (2, 'Math', 82),
    (2, 'English', 76),
    (2, 'History', 85),
    (3, 'Math', 81),
    (3, 'English', 99),
    (3, 'History', 100),
    (4, 'Math', 67),
    (4, 'English', 89),
    (4, 'History', 77),
    (5, 'Math', 75),
    (5, 'English', 100),
    (5, 'History', 98)]

cursor.executemany('INSERT INTO Students (first_name, last_name) VALUES (?, ?)', Students)
cursor.executemany('INSERT INTO Grades (student_id, subject, grade) VALUES (?, ?, ?)', Grades)
connection.commit()

# 1. Retrieve all students' names and their grades.
cursor.execute('''
    SELECT Students.first_name, Students.last_name, Grades.subject, Grades.grade
    FROM Students
    JOIN Grades ON Students.student_id = Grades.student_id''')

StudentGrades = cursor.fetchall()
for row in StudentGrades:
    print(row)

# 2. Find the average grade for each student.
cursor.execute('''
    SELECT Students.first_name, Students.last_name, AVG(Grades.grade)
    FROM Students
    JOIN Grades ON Students.student_id = Grades.student_id
    GROUP BY Students.student_id''')

StudentAverages = cursor.fetchall()
for row in StudentAverages:
    print(row)

# 3. Find the student with the highest average grade.
cursor.execute('''
    SELECT Students.first_name, students.last_name, AVG(grades.grade) as average_grade
    FROM Students
    JOIN Grades ON students.student_id = grades.student_id
    GROUP BY Students.student_id
    ORDER BY average_grade DESC
    LIMIT 1''')

HighestAverage = cursor.fetchone()
print(HighestAverage)

# 4. Find the average grade for the Math subject.
cursor.execute('''
    SELECT AVG(grade) FROM Grades WHERE subject = 'Math' ''')

AverageMathGrade = cursor.fetchone()
print(AverageMathGrade)

# 5. List all students who scored above 90 in any subject.
cursor.execute('''
    SELECT Students.first_name, Students.last_name, Grades.subject, Grades.grade
    FROM Students
    JOIN Grades ON Students.student_id = Grades.student_id
    WHERE Grades.grade > 90''')

GradesAbove90 = cursor.fetchall()
for row in GradesAbove90:
    print(row)

# 1. Use Pandas to load the data from the students and grades tables into DataFrames.
# 2. Use JOIN queries to combine the data from both tables into a single DataFrame that includes each student's name, subject, and grade.
Students_df = pd.read_sql_query('SELECT * FROM students', connection)
Grades_df = pd.read_sql_query('SELECT * FROM grades', connection)

Single_df = pd.read_sql_query('''
    SELECT students.first_name, students.last_name, grades.subject, grades.grade
    FROM students
    JOIN grades ON students.student_id = grades.student_id''', connection)

print(Single_df)

# 3. Visualize the data with Matplotlib. Plot the average grades for each student. Create a bar chart showing the average grade for each subject
AverageGrades_df = Single_df.groupby(['first_name', 'last_name'])['grade'].mean().reset_index()
plt.bar(AverageGrades_df['first_name'], AverageGrades_df['grade'])
plt.title('Student Average Grade')
plt.xlabel('Student')
plt.ylabel('Grade')
plt.show()

SubjectAverage_df = Single_df.groupby('subject')['grade'].mean().reset_index()
plt.bar(SubjectAverage_df['subject'], SubjectAverage_df['grade'])
plt.title('Subject Average Grade')
plt.xlabel('Subject')
plt.ylabel('Grade')
plt.show()

# BONUS: Implement a query that finds the student with the highest grade in each subject. Visualize the results using a grouped bar chart
cursor.execute('''
    SELECT Students.first_name, Students.last_name, Grades.subject, MAX(Grades.grade)
    FROM Students
    JOIN Grades ON Students.student_id = Grades.student_id
    GROUP BY Grades.subject''')
HighestGrade = cursor.fetchall()
for row in HighestGrade:
    print(row)