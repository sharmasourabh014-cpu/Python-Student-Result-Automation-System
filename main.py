import csv
import sqlite3

# Connect to database
conn = sqlite3.connect("student_result.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT,
    marks INTEGER
)
""")

conn.commit()

print("Database and table ready.")

def insert_data():
    name = input("Enter student name: ")
    subject = input("Enter subject: ")
    marks = int(input("Enter marks: "))

    cursor.execute(
        "INSERT INTO students (name, subject, marks) VALUES (?,?,?)",
        (name, subject, marks)
    )
    conn.commit()
    print("Record inserted successfully.")


def show_all():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    print("\n--- All Records ---")
    for row in data:
        print(row)



#Average + Result + Grade system
def student_report():
    cursor.execute("""
        SELECT name, ROUND(AVG(marks),2) AS avg_marks
        FROM students
        GROUP BY name
    """)

    results = cursor.fetchall()

    print("\n--- Student Result Report ---")

    for row in results:
        name = row[0]
        avg = row[1]

        if avg >= 40:
            status = "PASS"
        else:
            status = "FAIL"

        if avg >= 75:
            grade = "A"
        elif avg >= 60:
            grade = "B"
        elif avg >= 50:
            grade = "C"
        else:
            grade = "D"

        print(f"{name} | Average: {avg} | Result: {status} | Grade: {grade}")

#Topper report
def topper():
    cursor.execute("""
        SELECT name, ROUND(AVG(marks),2) AS avg_marks
        FROM students
        GROUP BY name
        ORDER BY avg_marks DESC
        LIMIT 1
    """)

    top = cursor.fetchone()

    print("\n--- Top Performer ---")
    print(f"{top[0]} | Average Marks: {top[1]}")

#Report Generate in CSV
def export_to_csv():
    cursor.execute("""
        SELECT name, ROUND(AVG(marks),2) AS avg_marks
        FROM students
        GROUP BY name
    """)

    results = cursor.fetchall()

    with open("C:/Users/BCA/Documents/Python_Student_Result_Automation/student_results.csv", "w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["Name", "Average Marks", "Result", "Grade"])

        for row in results:
            name = row[0]
            avg = row[1]

            if avg >= 40:
                status = "PASS"
            else:
                status = "FAIL"

            if avg >= 75:
                grade = "A"
            elif avg >= 60:
                grade = "B"
            elif avg >= 50:
                grade = "C"
            else:
                grade = "D"

            writer.writerow([name, avg, status, grade])

    print("CSV report generated: student_results.csv")


#Menu update
while True:
    print("\n1. Add Student Record")
    print("2. View All Records")
    print("3. Student Result Report")
    print("4. Top Performer")
    print("5. Export Result to CSV")
    print("Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        insert_data()
    elif choice == "2":
        show_all()
    elif choice == "3":
        student_report()
    elif choice == "4":
        topper()
    elif choice == "5":
        export_to_csv()
    elif choice == "6":
        print("Exiting Program....")
        break
    else:
        print("Invalid choice. Try again.")

