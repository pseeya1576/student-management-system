import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors


CSV_FILE = "students.csv"


def create_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Student ID", "Name", "Course", "Semester", "Email"])


def read_students():
    students = []
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        create_csv()
    return students


def save_students(students):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["Student ID", "Name", "Course", "Semester", "Email"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)


def clear_fields():
    student_id_var.set("")
    name_var.set("")
    course_var.set("")
    semester_var.set("")
    email_var.set("")

    for item in student_table.selection():
        student_table.selection_remove(item)


def validate_input():
    student_id = student_id_var.get().strip()
    name = name_var.get().strip()
    course = course_var.get().strip()
    semester = semester_var.get().strip()
    email = email_var.get().strip()

    if not student_id:
        messagebox.showerror("Validation Error", "Please enter Student ID.")
        return False

    if not name:
        messagebox.showerror("Validation Error", "Please enter Student Name.")
        return False

    if not course:
        messagebox.showerror("Validation Error", "Please enter Course.")
        return False

    if not semester:
        messagebox.showerror("Validation Error", "Please enter Semester.")
        return False

    if not email:
        messagebox.showerror("Validation Error", "Please enter Email.")
        return False

    if "@" not in email or "." not in email:
        messagebox.showerror("Validation Error", "Please enter a valid email address.")
        return False

    return True


def student_id_exists(student_id, exclude_id=None):
    for student in read_students():
        existing_id = student["Student ID"]
        if existing_id == student_id:
            if exclude_id is None or existing_id != exclude_id:
                return True
    return False


def add_student():
    if not validate_input():
        return

    student_id = student_id_var.get().strip()

    if student_id_exists(student_id):
        messagebox.showerror(
            "Duplicate Student ID",
            "This Student ID already exists."
        )
        return

    student = {
        "Student ID": student_id,
        "Name": name_var.get().strip(),
        "Course": course_var.get().strip(),
        "Semester": semester_var.get().strip(),
        "Email": email_var.get().strip()
    }

    students = read_students()
    students.append(student)
    save_students(students)
    load_students()
    clear_fields()

    messagebox.showinfo("Success", "Student added successfully.")


def load_students():
    for item in student_table.get_children():
        student_table.delete(item)

    for student in read_students():
        student_table.insert(
            "",
            "end",
            values=(
                student["Student ID"],
                student["Name"],
                student["Course"],
                student["Semester"],
                student["Email"]
            )
        )


def select_student(event=None):
    selected = student_table.selection()

    if not selected:
        return

    values = student_table.item(selected[0], "values")

    student_id_var.set(values[0])
    name_var.set(values[1])
    course_var.set(values[2])
    semester_var.set(values[3])
    email_var.set(values[4])


def update_student():
    selected = student_table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a student to update."
        )
        return

    if not validate_input():
        return

    old_values = student_table.item(selected[0], "values")
    old_id = old_values[0]
    new_id = student_id_var.get().strip()

    if student_id_exists(new_id, exclude_id=old_id):
        messagebox.showerror(
            "Duplicate Student ID",
            "Another student already has this Student ID."
        )
        return

    students = read_students()

    for student in students:
        if student["Student ID"] == old_id:
            student["Student ID"] = new_id
            student["Name"] = name_var.get().strip()
            student["Course"] = course_var.get().strip()
            student["Semester"] = semester_var.get().strip()
            student["Email"] = email_var.get().strip()
            break

    save_students(students)
    load_students()
    clear_fields()

    messagebox.showinfo("Success", "Student updated successfully.")


def delete_student():
    selected = student_table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a student to delete."
        )
        return

    values = student_table.item(selected[0], "values")
    student_id = values[0]
    student_name = values[1]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete {student_name} ({student_id})?"
    )

    if not confirm:
        return

    students = read_students()
    students = [
        student for student in students
        if student["Student ID"] != student_id
    ]

    save_students(students)
    load_students()
    clear_fields()

    messagebox.showinfo("Deleted", "Student deleted successfully.")


def search_student():
    search_text = search_var.get().strip().lower()

    for item in student_table.get_children():
        student_table.delete(item)

    for student in read_students():
        combined_text = (
            student["Student ID"] + " " +
            student["Name"] + " " +
            student["Course"] + " " +
            student["Semester"] + " " +
            student["Email"]
        ).lower()

        if search_text in combined_text:
            student_table.insert(
                "",
                "end",
                values=(
                    student["Student ID"],
                    student["Name"],
                    student["Course"],
                    student["Semester"],
                    student["Email"]
                )
            )


def show_all_students():
    search_var.set("")
    load_students()


def generate_pdf():
    selected = student_table.selection()

    if not selected:
        messagebox.showwarning(
            "No Student Selected",
            "Please select a student from the table first."
        )
        return

    values = student_table.item(selected[0], "values")

    student_id = values[0]
    name = values[1]
    course = values[2]
    semester = values[3]
    email = values[4]

    filename = "Student_Report_" + student_id.replace(" ", "_") + ".pdf"

    pdf = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Header
    pdf.setFillColor(colors.HexColor("#245A85"))
    pdf.rect(0, height - 105, width, 105, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawCentredString(width / 2, height - 60, "STUDENT REPORT")

    # Title
    pdf.setFillColor(colors.HexColor("#245A85"))
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(60, height - 155, "Student Management System")

    # Information box
    box_x = 60
    box_y = height - 420
    box_width = width - 120
    box_height = 225

    pdf.setStrokeColor(colors.HexColor("#245A85"))
    pdf.setLineWidth(1.5)
    pdf.roundRect(box_x, box_y, box_width, box_height, 10, fill=0, stroke=1)

    details = [
        ("Student ID", student_id),
        ("Name", name),
        ("Course", course),
        ("Semester", semester),
        ("Email", email)
    ]

    y = box_y + box_height - 45

    for label, value in details:
        pdf.setFillColor(colors.HexColor("#245A85"))
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(box_x + 25, y, label + ":")

        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(box_x + 135, y, str(value))

        y -= 37

    # Footer
    pdf.setStrokeColor(colors.HexColor("#CCCCCC"))
    pdf.line(60, 70, width - 60, 70)

    pdf.setFillColor(colors.grey)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(
        width / 2,
        50,
        "Generated using Student Management System"
    )

    pdf.save()

    messagebox.showinfo(
        "PDF Generated",
        f"PDF report generated successfully!\n\nSaved as:\n{filename}"
    )


# -------------------- Main Window --------------------

create_csv()

root = tk.Tk()
root.title("Student Management System")
root.geometry("1250x760")
root.minsize(1050, 680)
root.configure(bg="#F3F6FA")

student_id_var = tk.StringVar()
name_var = tk.StringVar()
course_var = tk.StringVar()
semester_var = tk.StringVar()
email_var = tk.StringVar()
search_var = tk.StringVar()

style = ttk.Style()

try:
    style.theme_use("clam")
except Exception:
    pass

style.configure(
    "Treeview",
    background="white",
    foreground="#222222",
    rowheight=34,
    fieldbackground="white",
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#245A85",
    foreground="white",
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#B8D7EF")],
    foreground=[("selected", "black")]
)

# Header
header = tk.Frame(root, bg="#245A85", height=100)
header.pack(fill="x")

tk.Label(
    header,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Segoe UI", 25, "bold"),
    bg="#245A85",
    fg="white"
).pack(pady=(17, 0))

tk.Label(
    header,
    text="Student Record Management  •  CSV Storage  •  PDF Report Generation",
    font=("Segoe UI", 10),
    bg="#245A85",
    fg="#E4EFF8"
).pack()

# Main area
main = tk.Frame(root, bg="#F3F6FA")
main.pack(fill="both", expand=True, padx=18, pady=18)

# Left panel
left_panel = tk.Frame(
    main,
    bg="white",
    bd=1,
    relief="solid",
    width=310
)
left_panel.pack(side="left", fill="y", padx=(0, 15))
left_panel.pack_propagate(False)

tk.Label(
    left_panel,
    text="Student Details",
    font=("Segoe UI", 17, "bold"),
    bg="white",
    fg="#245A85"
).pack(anchor="w", padx=22, pady=(18, 12))


def add_field(parent, label_text, variable):
    tk.Label(
        parent,
        text=label_text,
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg="#333333"
    ).pack(anchor="w", padx=22, pady=(5, 2))

    entry = tk.Entry(
        parent,
        textvariable=variable,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1
    )

    entry.pack(fill="x", padx=22, ipady=5)


add_field(left_panel, "Student ID", student_id_var)
add_field(left_panel, "Student Name", name_var)
add_field(left_panel, "Course", course_var)
add_field(left_panel, "Semester", semester_var)
add_field(left_panel, "Email", email_var)

buttons = tk.Frame(left_panel, bg="white")
buttons.pack(fill="x", padx=18, pady=15)


def make_button(parent, text, command, bg="#245A85"):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 9, "bold"),
        bg=bg,
        fg="white",
        activebackground=bg,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        pady=7
    )


make_button(buttons, "Add Student", add_student).grid(
    row=0, column=0, padx=3, pady=3, sticky="ew"
)

make_button(buttons, "Update", update_student).grid(
    row=0, column=1, padx=3, pady=3, sticky="ew"
)

make_button(buttons, "Delete", delete_student, "#B23B3B").grid(
    row=1, column=0, padx=3, pady=3, sticky="ew"
)

make_button(buttons, "Clear", clear_fields, "#6C757D").grid(
    row=1, column=1, padx=3, pady=3, sticky="ew"
)

make_button(buttons, "Generate PDF", generate_pdf, "#198754").grid(
    row=2, column=0, columnspan=2, padx=3, pady=(5, 3), sticky="ew"
)

buttons.columnconfigure(0, weight=1)
buttons.columnconfigure(1, weight=1)

# Right panel
right_panel = tk.Frame(
    main,
    bg="white",
    bd=1,
    relief="solid"
)
right_panel.pack(side="right", fill="both", expand=True)

search_frame = tk.Frame(right_panel, bg="white")
search_frame.pack(fill="x", padx=15, pady=15)

tk.Label(
    search_frame,
    text="Search:",
    font=("Segoe UI", 10, "bold"),
    bg="white"
).pack(side="left", padx=(0, 8))

tk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
).pack(side="left", fill="x", expand=True, ipady=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_student,
    font=("Segoe UI", 9, "bold"),
    bg="#245A85",
    fg="white",
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=6
).pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=show_all_students,
    font=("Segoe UI", 9, "bold"),
    bg="#6C757D",
    fg="white",
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=6
).pack(side="left")

# Table
table_frame = tk.Frame(right_panel, bg="white")
table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

columns = ("Student ID", "Name", "Course", "Semester", "Email")

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:
    student_table.heading(column, text=column)

student_table.column("Student ID", width=100, anchor="center")
student_table.column("Name", width=170)
student_table.column("Course", width=150)
student_table.column("Semester", width=90, anchor="center")
student_table.column("Email", width=230)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=student_table.yview
)

student_table.configure(yscrollcommand=scrollbar.set)

student_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

student_table.bind("<ButtonRelease-1>", select_student)

# Status bar
tk.Label(
    root,
    text="Select a student → Update / Delete / Generate PDF Report",
    font=("Segoe UI", 9),
    bg="#E5EBF2",
    fg="#555555",
    anchor="w",
    padx=18,
    pady=7
).pack(fill="x", side="bottom")

load_students()

root.mainloop(
