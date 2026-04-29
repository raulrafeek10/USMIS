import sqlite3

conn = sqlite3.connect("lms.db")

cursor = conn.cursor()

# ================= COURSES TABLE =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS courses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL UNIQUE,

    doctor TEXT,

    day TEXT,

    time TEXT,

    room TEXT

)

""")

# ================= LECTURES TABLE =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS lectures (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    course_id INTEGER,

    title TEXT,

    filename TEXT,

    FOREIGN KEY(course_id)
    REFERENCES courses(id)

)

""")

# ================= ASSIGNMENTS TABLE =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS assignments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    course_id INTEGER,

    title TEXT,

    description TEXT,

    due_date TEXT,

    FOREIGN KEY(course_id)
    REFERENCES courses(id)

)

""")

# ================= ASSIGNMENT SUBMISSIONS =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS assignment_submissions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    assignment_id INTEGER,

    student_name TEXT,

    filename TEXT,

    submission_date TEXT,

    FOREIGN KEY(assignment_id)
    REFERENCES assignments(id)

)

""")

# ================= NOTIFICATIONS TABLE =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS notifications (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    message TEXT,

    created_at TEXT

)

""")

conn.commit()

conn.close()

print("Database Created Successfully ✅")