
import streamlit as st
import sqlite3
import re

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="College Student Portal",
    page_icon="🎓",
    layout="wide"
)

DB_NAME = "college.db"


# ---------------- DATABASE ----------------
def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                year TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)


def add_student(student_id, name, course, year, email):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            INSERT INTO students
            (student_id, name, course, year, email)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, name, course, year, email))


def get_students():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("""
            SELECT student_id, name, course, year, email
            FROM students ORDER BY name
        """).fetchall()


def delete_student(student_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )


create_database()


# ---------------- DESIGN ----------------
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: bold;
    color: #2457A7;
}
.subtitle {
    font-size: 18px;
    color: #64748b;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🎓 College Portal")
st.sidebar.caption("Student Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Register Student",
        "Student Records",
        "Student Profile",
        "Attendance",
        "Exam Details",
        "Subjects",
        "About"
    ]
)



# ---------------- HOME PAGE ----------------
if page == "Home":
    students = get_students()

        # College name and logo
    col1, col2 = st.columns([1, 4])

    with col1:
        st.image("college_logo.png", width=130)

    with col2:
        st.markdown(
            """
            <h1 style="color: #FFD700; text-align: center;">
                KLES RLSI COLLEGE BELAGAVI
            </h1>
            <h3>Welcome to RLS  College</h3>
            <p>Empowering Education, Inspiring Excellence</p>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown(
        '<p class="main-title">Welcome to KLEs RLS College</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">Student Management Portal</p>',
        unsafe_allow_html=True
    )

    st.info(
        "Manage student registrations and academic records "
        "using this simple college website."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Registered Students", len(students))

    with col2:
        st.metric("Available Courses", 4)

    st.subheader("Our Courses")
    st.write("💻 Computer Science")
    st.write("📊 Data Science")
    st.write("💼 Commerce")
    st.write("🔬 Science")

    st.success(
        "Use the navigation menu on the left to get started."
    )


# ---------------- REGISTRATION PAGE ----------------
elif page == "Register Student":
    st.title("📝 Student Registration")
    st.write("Enter the student's details below.")

    with st.form("student_registration"):
        student_id = st.text_input("Student ID")
        name = st.text_input("Full Name")

        course = st.selectbox(
            "Course",
            [
                "Computer Science",
                "Data Science",
                "Commerce",
                "Science"
            ]
        )

        year = st.selectbox(
            "Academic Year",
            ["1st Year", "2nd Year", "3rd Year", "4th Year"]
        )

        email = st.text_input("Email Address")

        submitted = st.form_submit_button(
            "Register Student",
            use_container_width=True
        )

        if submitted:
            student_id = student_id.strip()
            name = name.strip()
            email = email.strip()

            if not student_id or not name or not email:
                st.error("Please fill in all the fields.")

            elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                st.error("Please enter a valid email address.")

            else:
                try:
                    add_student(
                        student_id, name, course, year, email
                    )
                    st.success(
                        f"Student {name} registered successfully!"
                    )
                except sqlite3.IntegrityError:
                    st.error(
                        "This Student ID already exists. "
                        "Please use a different ID."
                    )


# ---------------- STUDENT RECORDS PAGE ----------------
elif page == "Student Records":
    st.title("📋 Student Records")

    students = get_students()

    if not students:
        st.warning(
            "No students registered yet. "
            "Go to Register Student to add one."
        )
    else:
        search = st.text_input(
            "Search by student ID, name or course"
        ).strip().lower()

        filtered = [
            student for student in students
            if search in " ".join(student).lower()
        ]

        st.write(f"Showing {len(filtered)} student(s)")

        if filtered:
            st.dataframe(
                [
                    {
                        "Student ID": s[0],
                        "Name": s[1],
                        "Course": s[2],
                        "Year": s[3],
                        "Email": s[4]
                    }
                    for s in filtered
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No matching student records found.")

        st.divider()
        st.subheader("Delete a Student Record")

        student_ids = [s[0] for s in students]

        selected_id = st.selectbox(
            "Select Student ID",
            student_ids
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this record."
        )

        if st.button("Delete Student", type="secondary"):
            if confirm:
                delete_student(selected_id)
                st.success("Student record deleted.")
                st.rerun()
            else:
                st.warning("Please confirm before deleting.")

                
# ---------------- STUDENT PROFILE PAGE ----------------
elif page == "Student Profile":
    st.title("👤 Student Profile")

    students = get_students()

    if not students:
        st.warning("Please register a student first.")
    else:
        student_ids = [s[0] for s in students]

        selected_id = st.selectbox(
            "Select Student",
            student_ids,
            key="profile_student"
        )

        student = next(
            s for s in students if s[0] == selected_id
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(student[1])
            st.write("**Student ID:**", student[0])
            st.write("**Course:**", student[2])
            st.write("**Academic Year:**", student[3])
            st.write("**Email:**", student[4])

        with col2:
            photo = st.file_uploader(
                "Upload Student Photo",
                type=["png", "jpg", "jpeg"],
                key="student_photo"
            )

            if photo:
                st.image(photo, caption=student[1],
                         width=220)
            else:
                st.info("Upload a photo to display it here.")


# ---------------- ATTENDANCE PAGE ----------------
elif page == "Attendance":
    st.title("📅 Student Attendance")

    students = get_students()

    if not students:
        st.warning("Please register a student first.")
    else:
        student_ids = [s[0] for s in students]

        with st.form("attendance_form"):
            student_id = st.selectbox(
                "Student ID",
                student_ids
            )

            attendance_date = st.date_input(
                "Attendance Date"
            )

            status = st.radio(
                "Attendance Status",
                ["Present", "Absent"],
                horizontal=True
            )

            save_attendance = st.form_submit_button(
                "Save Attendance"
            )

            if save_attendance:
                with sqlite3.connect(DB_NAME) as conn:
                    conn.execute("""
                        INSERT INTO attendance
                        (student_id, date, status)
                        VALUES (?, ?, ?)
                    """, (
                        student_id,
                        str(attendance_date),
                        status
                    ))

                st.success("Attendance saved successfully!")

    st.subheader("Attendance Records")

    with sqlite3.connect(DB_NAME) as conn:
        records = conn.execute("""
            SELECT a.student_id, s.name, a.date, a.status
            FROM attendance a
            LEFT JOIN students s
            ON a.student_id = s.student_id
            ORDER BY a.date DESC, a.id DESC
        """).fetchall()

    if records:
        st.dataframe(
            [
                {
                    "Student ID": r[0],
                    "Name": r[1] or "Student not found",
                    "Date": r[2],
                    "Status": r[3]
                }
                for r in records
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No attendance records available yet.")


# ---------------- EXAM DETAILS PAGE ----------------
elif page == "Exam Details":
    st.title("📝 Examination Details")

    st.info(
        "Sample examination timetable. "
        "Update it with your college's actual schedule."
    )

    exam_data = [
        {
            "Subject": "Python Programming",
            "Exam Date": "2026-11-10",
            "Time": "10:00 AM - 1:00 PM",
            "Room": "Room 101"
        },
        {
            "Subject": "Database Management",
            "Exam Date": "2026-11-12",
            "Time": "10:00 AM - 1:00 PM",
            "Room": "Room 102"
        },
        {
            "Subject": "Computer Networks",
            "Exam Date": "2026-11-15",
            "Time": "10:00 AM - 1:00 PM",
            "Room": "Room 103"
        },
    ]

    st.dataframe(
        exam_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Exam Instructions")
    st.write("• Bring your college ID card.")
    st.write("• Arrive at the examination hall early.")
    st.write("• Follow the examination rules.")
    st.write("• Contact the college office for timetable updates.")


# ---------------- SUBJECTS PAGE ----------------
elif page == "Subjects":
    st.title("📚 Subjects and Courses")

    subjects = [
        {
            "Code": "CS101",
            "Subject": "Python Programming",
            "Course": "Computer Science"
        },
        {
            "Code": "CS102",
            "Subject": "Database Management",
            "Course": "Computer Science"
        },
        {
            "Code": "CS103",
            "Subject": "Computer Networks",
            "Course": "Computer Science"
        },
        {
            "Code": "DS101",
            "Subject": "Statistics",
            "Course": "Data Science"
        },
        {
            "Code": "CM101",
            "Subject": "Business Accounting",
            "Course": "Commerce"
        },
    ]

    course_filter = st.selectbox(
        "Filter by Course",
        [
            "All Courses",
            "Computer Science",
            "Data Science",
            "Commerce",
            "Science"
        ]
    )

    if course_filter == "All Courses":
        filtered_subjects = subjects
    else:
        filtered_subjects = [
            subject for subject in subjects
            if subject["Course"] == course_filter
        ]

    st.dataframe(
        filtered_subjects,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "These are example subjects. "
        "Replace them with your college syllabus."
    )



# ---------------- ABOUT PAGE ----------------
elif page == "About":
    st.title("ℹ️ About Our College Portal")

    st.write("""
    The College Student Portal is a Python and Streamlit project
    designed to simplify student record management.

    **Main features**
    - Student registration
    - Student record storage
    - Search student details
    - Delete student records
    - Automatic database creation

    **Technologies used**
    - Python
    - Streamlit
    - SQLite
    """)

    st.info(
        "This is a demonstration project. "
        "Add login, access control and backups before using "
        "real student information."
    )

st.sidebar.divider()
st.sidebar.caption("College Student Portal | Python + Streamlit")
