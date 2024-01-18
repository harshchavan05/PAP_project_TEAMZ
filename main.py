import mysql.connector
from mysql.connector import Error
import re

class Person:
    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name

    def __str__(self):
        return f"ID: {self.person_id}, Name: {self.name}"

class Student(Person):
    def __init__(self, student_id, name, courses):
        super().__init__(student_id, name)
        self.courses = courses

    def __str__(self):
        return f"Student {super().__str__()}, Courses: {', '.join(self.courses)}"

class AttendanceManager:
    def __init__(self, host, database, user, password):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )

            if self.connection.is_connected():
                print("Connected to MySQL Database")
                self.cursor = self.connection.cursor(buffered=True)
                self.create_tables()

        except Error as e:
            print(f"Error: {e}")

    def create_tables(self):
        create_persons_table = """
        CREATE TABLE IF NOT EXISTS persons (
            person_id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """

        create_students_table = """
        CREATE TABLE IF NOT EXISTS students (
            student_id INT PRIMARY KEY,
            courses VARCHAR(255),
            FOREIGN KEY (student_id) REFERENCES persons(person_id)
        )
        """

        create_attendance_table = """
        CREATE TABLE IF NOT EXISTS attendance (
            student_id INT,
            date DATE,
            status VARCHAR(50),
            PRIMARY KEY (student_id, date),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
        """

        try:
            self.cursor.execute(create_persons_table)
            self.cursor.execute(create_students_table)
            self.cursor.execute(create_attendance_table)
            self.connection.commit()
            print("Tables created successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")

    def add_student(self, student_id, name, courses):
        student = Student(student_id, name, courses)
        query_person = "INSERT INTO persons (person_id, name) VALUES (%s, %s)"
        query_student = "INSERT INTO students (student_id, courses) VALUES (%s, %s)"
        data_person = (student_id, name)
        data_student = (student_id, ', '.join(courses))

        try:
            self.cursor.execute(query_person, data_person)
            self.cursor.execute(query_student, data_student)
            self.connection.commit()
            print(f"Student {name} added successfully.")
        except Error as e:
            print(f"Error adding student: {e}")

    def mark_attendance(self, student_id, date, status):
        query = "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)"
        data = (student_id, date, status)

        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            print(f"Attendance marked for student {student_id} on {date}.")
        except Error as e:
            print(f"Error marking attendance: {e}")

    def view_attendance(self, student_id):
        query = "SELECT date, status FROM attendance WHERE student_id = %s"
        data = (student_id,)

        try:
            self.cursor.execute(query, data)
            rows = self.cursor.fetchall()
            if rows:
                print(f"Attendance for student {student_id}:")
                for row in rows:
                    print(f"{row[0]}: {row[1]}")
            else:
                print("No attendance records found.")
        except Error as e:
            print(f"Error fetching attendance: {e}")

    def search_students(self, keyword):
        query = "SELECT person_id, name FROM persons WHERE name LIKE %s"
        data = ('%' + keyword + '%',)

        try:
            self.cursor.execute(query, data)
            rows = self.cursor.fetchall()
            if rows:
                print("Search Results:")
                for row in rows:
                    print(f"{row[0]}: {row[1]}")
            else:
                print("No matching students found.")
        except Error as e:
            print(f"Error searching students: {e}")

    def __del__(self):
        try:

            if hasattr(self, 'cursor') and self.cursor is not None:
                self.cursor.close()

            if hasattr(self, 'connection') and self.connection.is_connected():
                self.connection.close()
                print("MySQL connection closed.")
        except Error as e:
            print(f"Error: {e}")


host = 'localhost'
database = 'python_project'
user = 'root'
password = '@Harsh05'

attendance_manager = AttendanceManager(host, database, user, password)

attendance_manager.add_student(1, "Suyog", ["Math", "Physics"])
attendance_manager.add_student(2, "Sharath R", ["Chemistry", "Biology"])
attendance_manager.add_student(3, "Harsh", ["Biology"])


attendance_manager.mark_attendance(1, "2024-01-13", "Present")
attendance_manager.mark_attendance(2, "2024-01-13", "Absent")
attendance_manager.mark_attendance(3, "2024-01-13", "Present")

attendance_manager.view_attendance(1)
attendance_manager.view_attendance(2)
attendance_manager.view_attendance(3)

attendance_manager.search_students("Suyog")


