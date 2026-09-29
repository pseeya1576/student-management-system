Student Management System

GTU PBL-3 — Python for Data Science (BE05000231)

A simple and polished desktop-based Student Management System developed using Python.

Objective

The project provides a simple way to maintain student records and perform common record-management operations.

Features

Add student

View student records

Search student

Update student

Delete student

Clear fields

Input validation

Duplicate Student ID checking

Delete confirmation

Select a student record

Generate a formatted PDF report for a selected student

Beyond Syllabus Topic

PDF Report Generation

The project includes PDF Report Generation as the additional topic.

After selecting a student, the application collects:

Student ID

Name

Course

Semester

Email

and generates a formatted PDF report using the ReportLab Python library.

The generated report is saved as:

Student_Report_<StudentID>.pdf

Technologies Used

Python

Tkinter

CSV file handling

ReportLab

No database, machine learning, Pandas, NumPy, API, or unnecessary external technology is required.

Project Structure

student-management-system/
│
├── main.py
├── README.md
├── requirements.txt
└── students.csv

students.csv is created automatically when the application runs if it does not already exist.

Installation

Open a terminal in the project folder and run:

python -m pip install -r requirements.txt

Or directly:

python -m pip install reportlab

Run the Project

python main.py

How to Generate a PDF

Add or select a student.

Click the student record in the table.

Click Generate PDF.

The report is saved in the project folder.

Example:

Student_Report_101.pdf

Author
PBL-3 Student Project
