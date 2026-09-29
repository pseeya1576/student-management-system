# ============================================================
# STUDENT MANAGEMENT SYSTEM - GTU PBL-3
# Subject: Python for Data Science
#
# OOS IMPLEMENTATION:
# Secure Student Data using Symmetric Encryption
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

from cryptography.fernet import Fernet


# ============================================================
# FILES AND CONSTANTS
# ============================================================

FILE_NAME = "students.csv"
KEY_FILE = "secret.key"

HEADERS = ["Student ID", "Name", "Course", "Semester", "Email"]


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()
window.title("Student Management System")
window.geometry("1100x650")
window.minsize(950, 550)
window.configure(bg="#F4F6F8")


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#F4F6F8"
HEADER_COLOR = "#1F4E78"
BUTTON_COLOR = "#2E75B6"
WHITE = "#FFFFFF"
TEXT_COLOR = "#222222"
GREY_COLOR = "#666666"
DELETE_COLOR = "#C0392B"
SECURITY_COLOR = "#2F855A"


# ============================================================
# VARIABLES
# ============================================================

student_id_var = tk.StringVar()
name_var = tk.StringVar()
course_var = tk.StringVar()
semester_var = tk.StringVar()
email_var = tk.StringVar()
search_var = tk.StringVar()


# ============================================================
# ENCRYPTION
# ============================================================

def create_encryption_key():
    """
    Creates a secret encryption key if it does not already exist.
    """
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)


def load_encryption_key():
    """
    Loads the existing encryption key.
    """
    create_encryption_key()

    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()


ENCRYPTION_KEY = load_encryption_key()
cipher = Fernet(ENCRYPTION_KEY)


def encrypt_data(data):
    """
    Encrypts sensitive data before storing it.
    """
    encrypted_data = cipher.encrypt(data.encode("utf-8"))
    return encrypted_data.decode("utf-8")


def decrypt_data(encrypted_data):
    """
    Decrypts encrypted data when displaying it.

    Older records that were stored as plain text
    are also supported.
    """
    try:
        decrypted_data = cipher.decrypt(
            encrypted_data.encode("utf-8")
        )

        return decrypted_data.decode("utf-8")

    except Exception:
        return encrypted_data


# ============================================================
# CSV FILE
# ============================================================

def create_csv_file():
    """
    Creates the CSV file with column headings
    if the file does not already exist.
    """

    if not os.path.exists(FILE_NAME):

        with open(
            FILE_NAME,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)
            writer.writerow(HEADERS)


# ============================================================
# VALIDATION
# ============================================================

def validate_student_data():

    student_id = student_id_var.get().strip()
    name = name_var.get().strip()
    course = course_var.get().strip()
    semester = semester_var.get().strip()
    email = email_var.get().strip()


    # Student ID
    if not student_id:

        messagebox.showwarning(
            "Invalid Student ID",
            "Student ID cannot be empty."
        )

        return False


    if not student_id.isdigit():

        messagebox.showwarning(
            "Invalid Student ID",
            "Student ID must contain numbers only."
        )

        return False


    # Name
    if not name:

        messagebox.showwarning(
            "Invalid Name",
            "Name cannot be empty."
        )

        return False


    if not all(
        character.isalpha() or character.isspace()
        for character in name
    ):

        messagebox.showwarning(
            "Invalid Name",
            "Name should contain letters and spaces only."
        )

        return False


    # Course
    if not course:

        messagebox.showwarning(
            "Invalid Course",
            "Course cannot be empty."
        )

        return False


    # Semester
    if not semester:

        messagebox.showwarning(
            "Invalid Semester",
            "Semester cannot be empty."
        )

        return False


    if not semester.isdigit():

        messagebox.showwarning(
            "Invalid Semester",
            "Semester must be a number from 1 to 8."
        )

        return False


    semester_number = int(semester)


    if semester_number < 1 or semester_number > 8:

        messagebox.showwarning(
            "Invalid Semester",
            "Semester must be between 1 and 8."
        )

        return False


    # Email
    if not email:

        messagebox.showwarning(
            "Invalid Email",
            "Email cannot be empty."
        )

        return False


    if "@" not in email or "." not in email:

        messagebox.showwarning(
            "Invalid Email",
            "Please enter a valid email address."
        )

        return False


    return True


# ============================================================
# CLEAR FIELDS
# ============================================================

def clear_fields():

    student_id_var.set("")
    name_var.set("")
    course_var.set("")
    semester_var.set("")
    email_var.set("")


    for item in table.selection():

        table.selection_remove(item)


    student_id_entry.focus()

    status_label.config(
        text="Fields cleared."
    )


# ============================================================
# LOAD STUDENTS
# ============================================================

def load_students():

    create_csv_file()


    # Clear table
    for item in table.get_children():

        table.delete(item)


    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)


        for row in reader:

            decrypted_email = decrypt_data(
                row["Email"]
            )


            table.insert(
                "",
                "end",
                values=(
                    row["Student ID"],
                    row["Name"],
                    row["Course"],
                    row["Semester"],
                    decrypted_email
                )
            )


    count = len(table.get_children())


    status_label.config(
        text=f"Showing {count} student record(s)."
    )


# ============================================================
# SEARCH
# ============================================================

def search_student():

    search_text = search_var.get().strip().lower()


    if not search_text:

        messagebox.showwarning(
            "Search",
            "Please enter a Student ID or Name to search."
        )

        return


    # Clear table
    for item in table.get_children():

        table.delete(item)


    found = False


    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)


        for row in reader:

            student_id = row["Student ID"].lower()
            name = row["Name"].lower()


            if (
                search_text in student_id
                or search_text in name
            ):

                decrypted_email = decrypt_data(
                    row["Email"]
                )


                table.insert(
                    "",
                    "end",
                    values=(
                        row["Student ID"],
                        row["Name"],
                        row["Course"],
                        row["Semester"],
                        decrypted_email
                    )
                )


                found = True


    if found:

        count = len(table.get_children())

        status_label.config(
            text=f"Found {count} matching student record(s)."
        )

    else:

        status_label.config(
            text="No matching student found."
        )

        messagebox.showinfo(
            "Search Result",
            "No student matched your search."
        )


# ============================================================
# SHOW ALL
# ============================================================

def show_all():

    search_var.set("")

    load_students()


# ============================================================
# SELECT STUDENT
# ============================================================

def select_student(event):

    selected_row = table.identify_row(event.y)


    if not selected_row:

        return


    table.selection_set(selected_row)


    values = table.item(
        selected_row,
        "values"
    )


    if not values:

        return


    student_id_var.set(values[0])
    name_var.set(values[1])
    course_var.set(values[2])
    semester_var.set(values[3])
    email_var.set(values[4])


    status_label.config(
        text=f"Student {values[0]} selected."
    )


# ============================================================
# CHECK DUPLICATE STUDENT ID
# ============================================================

def student_id_exists(student_id, ignore_id=None):

    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)


        for row in reader:

            existing_id = row["Student ID"]


            if existing_id == student_id:

                if (
                    ignore_id is not None
                    and existing_id == ignore_id
                ):

                    continue


                return True


    return False


# ============================================================
# ADD STUDENT
# ============================================================

def add_student():

    if not validate_student_data():

        return


    student_id = student_id_var.get().strip()
    name = name_var.get().strip()
    course = course_var.get().strip()
    semester = semester_var.get().strip()
    email = email_var.get().strip()


    create_csv_file()


    # Duplicate ID checking
    if student_id_exists(student_id):

        messagebox.showerror(
            "Duplicate Student ID",
            f"Student ID {student_id} already exists."
        )

        return


    # Encrypt email
    encrypted_email = encrypt_data(email)


    with open(
        FILE_NAME,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)


        writer.writerow(
            [
                student_id,
                name,
                course,
                semester,
                encrypted_email
            ]
        )


    load_students()

    clear_fields()


    status_label.config(
        text=f"Student {student_id} added successfully."
    )


    messagebox.showinfo(
        "Success",
        "Student added successfully!\n\n"
        "Email was securely encrypted before storage."
    )


# ============================================================
# UPDATE STUDENT
# ============================================================

def update_student():

    selected = table.selection()


    if not selected:

        messagebox.showwarning(
            "No Student Selected",
            "Please select a student from the table first."
        )

        return


    old_values = table.item(
        selected[0],
        "values"
    )


    if not old_values:

        return


    old_student_id = old_values[0]


    if not validate_student_data():

        return


    student_id = student_id_var.get().strip()
    name = name_var.get().strip()
    course = course_var.get().strip()
    semester = semester_var.get().strip()
    email = email_var.get().strip()


    # Check duplicate ID if ID was changed
    if student_id != old_student_id:

        if student_id_exists(
            student_id,
            ignore_id=old_student_id
        ):

            messagebox.showerror(
                "Duplicate Student ID",
                f"Student ID {student_id} already belongs "
                "to another student."
            )

            return


    # Read all students
    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        students = list(reader)


    student_found = False


    for student in students:

        if student["Student ID"] == old_student_id:

            student["Student ID"] = student_id
            student["Name"] = name
            student["Course"] = course
            student["Semester"] = semester

            # Encrypt updated email
            student["Email"] = encrypt_data(email)

            student_found = True

            break


    if not student_found:

        messagebox.showerror(
            "Student Not Found",
            "The selected student could not be found."
        )

        return


    # Rewrite CSV
    with open(
        FILE_NAME,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=HEADERS
        )

        writer.writeheader()
        writer.writerows(students)


    load_students()

    clear_fields()


    status_label.config(
        text=f"Student {student_id} updated successfully."
    )


    messagebox.showinfo(
        "Success",
        "Student information updated successfully!\n\n"
        "Email was encrypted before storage."
    )


# ============================================================
# DELETE STUDENT
# ============================================================

def delete_student():

    selected = table.selection()


    if not selected:

        messagebox.showwarning(
            "No Student Selected",
            "Please click on a student row first."
        )

        return


    values = table.item(
        selected[0],
        "values"
    )


    if not values:

        return


    student_id = values[0]
    student_name = values[1]


    # Confirmation
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete\n\n"
        f"Student ID: {student_id}\n"
        f"Name: {student_name}?"
    )


    if not confirm:

        status_label.config(
            text="Delete cancelled."
        )

        return


    # Read students
    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        students = list(reader)


    updated_students = []
    student_found = False


    for student in students:

        if student["Student ID"] == student_id:

            student_found = True

        else:

            updated_students.append(student)


    if not student_found:

        messagebox.showerror(
            "Error",
            "Student could not be found."
        )

        return


    # Rewrite CSV without deleted student
    with open(
        FILE_NAME,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=HEADERS
        )

        writer.writeheader()
        writer.writerows(updated_students)


    load_students()

    clear_fields()


    status_label.config(
        text=f"Student {student_id} deleted successfully."
    )


    messagebox.showinfo(
        "Deleted",
        f"Student {student_id} - {student_name}\n"
        "was deleted successfully."
    )


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    window,
    bg=HEADER_COLOR,
    height=80
)

header.pack(fill="x")


title_label = tk.Label(
    header,
    text="Student Management System",
    font=("Segoe UI", 22, "bold"),
    bg=HEADER_COLOR,
    fg=WHITE
)

title_label.pack(
    pady=(15, 2)
)


subtitle_label = tk.Label(
    header,
    text="GTU PBL-3 | Python for Data Science | Secure Data",
    font=("Segoe UI", 10),
    bg=HEADER_COLOR,
    fg=WHITE
)

subtitle_label.pack()


# ============================================================
# MAIN FRAME
# ============================================================

main_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# ============================================================
# LEFT FORM
# ============================================================

form_frame = tk.LabelFrame(
    main_frame,
    text=" Student Details ",
    font=("Segoe UI", 12, "bold"),
    bg=WHITE,
    fg=HEADER_COLOR,
    padx=20,
    pady=15
)

form_frame.pack(
    side="left",
    fill="y",
    padx=(0, 15)
)


# Student ID
tk.Label(
    form_frame,
    text="Student ID",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    pady=(5, 3)
)


student_id_entry = ttk.Entry(
    form_frame,
    textvariable=student_id_var,
    width=30
)

student_id_entry.pack(
    pady=(0, 12)
)


# Name
tk.Label(
    form_frame,
    text="Name",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    pady=(5, 3)
)


name_entry = ttk.Entry(
    form_frame,
    textvariable=name_var,
    width=30
)

name_entry.pack(
    pady=(0, 12)
)


# Course
tk.Label(
    form_frame,
    text="Course",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    pady=(5, 3)
)


course_entry = ttk.Entry(
    form_frame,
    textvariable=course_var,
    width=30
)

course_entry.pack(
    pady=(0, 12)
)


# Semester
tk.Label(
    form_frame,
    text="Semester",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    pady=(5, 3)
)


semester_entry = ttk.Entry(
    form_frame,
    textvariable=semester_var,
    width=30
)

semester_entry.pack(
    pady=(0, 12)
)


# Email
tk.Label(
    form_frame,
    text="Email",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    pady=(5, 3)
)


email_entry = ttk.Entry(
    form_frame,
    textvariable=email_var,
    width=30
)

email_entry.pack(
    pady=(0, 15)
)


# ============================================================
# BUTTONS
# ============================================================

button_frame = tk.Frame(
    form_frame,
    bg=WHITE
)

button_frame.pack(
    fill="x",
    pady=5
)


tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    bg=BUTTON_COLOR,
    fg=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    cursor="hand2",
    width=13
).pack(pady=4)


tk.Button(
    button_frame,
    text="Update Student",
    command=update_student,
    bg=BUTTON_COLOR,
    fg=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    cursor="hand2",
    width=13
).pack(pady=4)


tk.Button(
    button_frame,
    text="Delete Student",
    command=delete_student,
    bg=DELETE_COLOR,
    fg=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    cursor="hand2",
    width=13
).pack(pady=4)


tk.Button(
    button_frame,
    text="Clear Fields",
    command=clear_fields,
    bg=GREY_COLOR,
    fg=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    cursor="hand2",
    width=13
).pack(pady=4)


# Security indicator
security_label = tk.Label(
    form_frame,
    text="🔐 Email encrypted in CSV",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=SECURITY_COLOR
)

security_label.pack(
    pady=(12, 0)
)


# ============================================================
# RIGHT SIDE
# ============================================================

right_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

right_frame.pack(
    side="right",
    fill="both",
    expand=True
)


# ============================================================
# SEARCH
# ============================================================

search_frame = tk.Frame(
    right_frame,
    bg=WHITE,
    padx=12,
    pady=12
)

search_frame.pack(
    fill="x",
    pady=(0, 12)
)


tk.Label(
    search_frame,
    text="Search Student",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).pack(
    side="left",
    padx=(0, 8)
)


search_entry = ttk.Entry(
    search_frame,
    textvariable=search_var,
    width=28
)

search_entry.pack(
    side="left",
    padx=5
)


tk.Button(
    search_frame,
    text="Search",
    command=search_student,
    bg=BUTTON_COLOR,
    fg=WHITE,
    font=("Segoe UI", 9, "bold"),
    relief="flat",
    cursor="hand2",
    width=9
).pack(
    side="left",
    padx=5
)


tk.Button(
    search_frame,
    text="Show All",
    command=show_all,
    bg=GREY_COLOR,
    fg=WHITE,
    font=("Segoe UI", 9, "bold"),
    relief="flat",
    cursor="hand2",
    width=9
).pack(
    side="left",
    padx=5
)


# ============================================================
# TABLE
# ============================================================

table_frame = tk.Frame(
    right_frame,
    bg=WHITE
)

table_frame.pack(
    fill="both",
    expand=True
)


table = ttk.Treeview(
    table_frame,
    columns=HEADERS,
    show="headings"
)


for column in HEADERS:

    table.heading(
        column,
        text=column
    )


table.column(
    "Student ID",
    width=100,
    anchor="center"
)

table.column(
    "Name",
    width=160,
    anchor="w"
)

table.column(
    "Course",
    width=150,
    anchor="w"
)

table.column(
    "Semester",
    width=90,
    anchor="center"
)

table.column(
    "Email",
    width=220,
    anchor="w"
)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(
    yscrollcommand=scrollbar.set
)


table.pack(
    side="left",
    fill="both",
    expand=True
)


scrollbar.pack(
    side="right",
    fill="y"
)


table.bind(
    "<ButtonRelease-1>",
    select_student
)


# ============================================================
# STATUS BAR
# ============================================================

status_label = tk.Label(
    window,
    text="Loading student records...",
    font=("Segoe UI", 9),
    bg="#E9EDF1",
    fg=GREY_COLOR,
    anchor="w",
    padx=15
)

status_label.pack(
    fill="x"
)


# ============================================================
# START APPLICATION
# ============================================================

create_csv_file()
load_students()

window.mainloop()