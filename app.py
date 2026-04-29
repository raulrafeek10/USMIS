from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import chatbot_ai
import random
import os

app = Flask(__name__)
app.secret_key = "lms_secret_key"

# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect("lms.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= CREATE TABLES =================

def create_tables():
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()

    # ================= USERS =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # ================= STUDENTS =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ================= GRADES =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        assignment INTEGER,
        midterm INTEGER,
        final INTEGER,
        total INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    # ================= ASSIGNMENTS =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        course TEXT,
        description TEXT,
        start_date TEXT,
        due_date TEXT,
        file_name TEXT
    )
    """)

    # ================= NEW TABLE (SUBMISSIONS) 🔥 =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignment_submissions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_name TEXT,

        assignment_title TEXT,

        filename TEXT,

        course_name TEXT,

        submission_date TEXT

    )
    """)

    # ================= NEW TABLE (NOTIFICATIONS) 🔔 =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        message TEXT,

        created_at TEXT

    )
    """)

    # ================= COURSES =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # ================= LECTURES =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lectures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        filename TEXT,
        course_id INTEGER,
        FOREIGN KEY(course_id) REFERENCES courses(id)
    )
    """)

    # ================= STUDENT COURSES =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_name TEXT,
        grade TEXT,
        credits INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    conn.commit()
    conn.close()
# ================= INSERT STUDENT COURSES =================

def insert_student_courses():
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM student_courses")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("SELECT id FROM students WHERE user_id IS NOT NULL LIMIT 1")
        student = cursor.fetchone()

        if student:
            courses = [
                (student[0], "DSS", "A", 3),
                (student[0], "Mobile Computing", "A+", 2),
                (student[0], "GIS", "A", 3),
                (student[0], "English", "B+", 2),
                (student[0], "ITPM", "A+", 3),
                (student[0], "Data Mining", "A", 3),
            ]
            cursor.executemany(
                "INSERT INTO student_courses (student_id, course_name, grade, credits) VALUES (?, ?, ?, ?)",
                courses
            )
            print("✅ Student Courses Added")

    conn.commit()
    conn.close()

# ================= INSERT DEFAULT DATA =================

def insert_default_data():
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM courses")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO courses (name) VALUES ('GIS')")
        cursor.execute("INSERT INTO courses (name) VALUES ('DSS')")

        cursor.execute("SELECT id FROM courses WHERE name='GIS'")
        gis_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM courses WHERE name='DSS'")
        dss_id = cursor.fetchone()[0]

        for i in range(1, 7):
            cursor.execute("INSERT INTO lectures VALUES (NULL,?,?,?)",
                (f"Chapter {i}", f"gis{i}.pdf", gis_id))

        for i in range(1, 7):
            cursor.execute("INSERT INTO lectures VALUES (NULL,?,?,?)",
                (f"Chapter {i}", f"dss{i}.pdf", dss_id))

    conn.commit()
    conn.close()

# ================= INSERT RANDOM STUDENTS =================

def insert_random_students():
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    if count == 0:
        first_names = ["Ahmed","Mohamed","Omar","Youssef","Mahmoud",
                       "Mostafa","Ibrahim","Karim","Amr","Ali"]
        last_names = ["Hassan","Mahmoud","Ali","Khaled",
                      "Tarek","Samir","Nasser","Hany","Salah","Adel"]

        for i in range(100):
            name = random.choice(first_names) + " " + random.choice(last_names)
            cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
            student_id = cursor.lastrowid

            assignment = random.randint(10, 20)
            midterm = random.randint(15, 30)
            final = random.randint(30, 50)
            total = assignment + midterm + final

            cursor.execute("""
            INSERT INTO grades (student_id, assignment, midterm, final, total)
            VALUES (?, ?, ?, ?, ?)
            """, (student_id, assignment, midterm, final, total))

        print("✅ 100 Random Students Added")

    conn.commit()
    conn.close()

# ================= LOGIN =================

@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=?", (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            if user["role"] != role:
                error = f"❌ This account must login as {user['role']}."
            else:
                session["role"] = user["role"]
                session["name"] = user["name"]
                session["email"] = user["email"]

                if user["role"] == "student":
                    return redirect(url_for("student_dashboard"))
                elif user["role"] == "professor":
                    return redirect(url_for("professor_dashboard"))
                elif user["role"] == "staff":
                    return redirect(url_for("admin_dashboard"))
        else:
            error = "❌ Wrong Email or Password"

    return render_template("login.html", error=error)

# ================= FORGOT PASSWORD =================

@app.route("/forgot", methods=["GET","POST"])
def forgot():
    if request.method == "POST":
        return redirect(url_for("check_email"))
    return render_template("forgot.html")

@app.route("/check_email")
def check_email():
    return render_template("check_email.html")

@app.route("/reset_password", methods=["GET","POST"])
def reset_password():
    if request.method == "POST":
        return redirect(url_for("login"))
    return render_template("reset_password.html")

# ================= DASHBOARDS =================

@app.route("/student_dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("login"))
    return render_template("student_dashboard.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "staff":
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html")

@app.route("/professor_dashboard")
def professor_dashboard():

    if session.get("role") != "professor":
        return redirect(url_for("login"))

    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM notifications
    ORDER BY id DESC
    LIMIT 5
    """)

    notifications = cursor.fetchall()

    conn.close()

    return render_template(
        "professor_dashboard.html",
        notifications=notifications
    )
# ================= LOGOUT =================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================= COURSES =================

@app.route("/courses")
def courses():
    conn = get_db()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("courses.html", courses=courses)

@app.route("/course/<course_name>")
def course_details(course_name):
    conn = get_db()
    course = conn.execute(
        "SELECT * FROM courses WHERE LOWER(name)=LOWER(?)", (course_name,)
    ).fetchone()

    if course is None:
        conn.close()
        return "❌ Course Not Found"

    lectures = conn.execute(
        "SELECT * FROM lectures WHERE course_id=?", (course["id"],)
    ).fetchall()
    conn.close()

    if course_name.lower() == "gis":
        instructor = "Dr. Nermeen"
        day = "Monday"
        time = "11:00 AM – 12:00 PM"
        room = "R 106"
    elif course_name.lower() == "dss":
        instructor = "Dr. Lamia"
        day = "Monday"
        time = "12:00 PM – 2:00 PM"
        room = "R 106"
    else:
        instructor = "Unknown"
        day = "-"
        time = "-"
        room = "-"

    return render_template("course_details.html",
        course=course, lectures=lectures,
        instructor=instructor, day=day, time=time, room=room)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("static/files", filename, as_attachment=True)

# ================= CHATBOT =================

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"reply": "⚠ Please enter a question."})
    reply = chatbot_ai.ask_question(message)
    return jsonify({"reply": reply})

@app.route("/quiz", methods=["POST"])
def quiz():
    quiz_text = chatbot_ai.generate_quiz()
    return jsonify({"quiz": quiz_text})

@app.route("/summarize", methods=["POST"])
def summarize_ai():
    summary_text = chatbot_ai.summarize()
    return jsonify({"summary": summary_text})

# ================= OTHER PAGES =================

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")

@app.route("/today_classes")
def today_classes():
    return render_template("today_classes.html")

@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/signup', methods=['POST'])
def signup():
    first = request.form.get('first_name')
    last = request.form.get('last_name')
    email = request.form.get('email')
    print("New User:", first, last, email)
    return redirect(url_for('login'))

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/help")
def help_page():
    return render_template("help.html")

# ================= GRADES =================

@app.route("/view_grades")
def view_grades():
    conn = get_db()
    grades = conn.execute("""
        SELECT grades.id, students.name,
               grades.assignment, grades.midterm,
               grades.final, grades.total
        FROM grades
        JOIN students ON grades.student_id = students.id
    """).fetchall()
    conn.close()
    return render_template("view_grades.html", grades=grades)

@app.route("/update_grade", methods=["POST"])
def update_grade():
    try:
        id = request.form["id"]
        assignment = int(request.form["assignment"])
        midterm = int(request.form["midterm"])
        final = int(request.form["final"])
        total = assignment + midterm + final

        conn = sqlite3.connect("lms.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE grades SET assignment=?, midterm=?, final=?, total=?
            WHERE id=?
        """, (assignment, midterm, final, total, id))
        conn.commit()
        conn.close()
        return "success"

    except ValueError:
        return "error: invalid numbers", 400

# ================= PROFESSOR =================

@app.route("/courses_professor")
def courses_professor():
    return render_template("courses_professor.html")

@app.route("/add_assignment", methods=["GET","POST"])
def add_assignment():
    if request.method == "POST":
        title = request.form["title"]
        course = request.form["course"]
        description = request.form["description"]
        start_date = request.form["start_date"]
        due_date = request.form["due_date"]
        file = request.files.get("file")
        file_name = ""

        if file and file.filename != "":
            allowed = {"pdf", "docx", "pptx"}
            ext = file.filename.rsplit(".", 1)[-1].lower()
            if ext not in allowed:
                flash("❌ File type not allowed")
                return redirect("/add_assignment")
            file_name = file.filename
            file.save("static/files/" + file_name)

        conn = sqlite3.connect("lms.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO assignments (title, course, description, start_date, due_date, file_name)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, course, description, start_date, due_date, file_name))
        conn.commit()
        conn.close()

        flash("Assignment Submitted Successfully ✅")
        return redirect("/add_assignment")

    return render_template("add_assignment.html")

@app.route("/publish_announcement")
def publish_announcement():
    return render_template("publish_announcement.html")



UPLOAD_FOLDER = "static/files"

@app.route("/upload_material", methods=["GET", "POST"])
def upload_material():

    if session.get("role") != "professor":
        return redirect(url_for("login"))

    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()

    # ✅ جلب الكورسات
    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()

    if request.method == "POST":

        file = request.files.get("file")
        course_id = request.form.get("course_id")
        title = request.form.get("title")

        if file and file.filename != "":

            filename = file.filename

            filepath = os.path.join(
                "static/files",
                filename
            )

            file.save(filepath)

            # حفظ lecture
            cursor.execute("""
            INSERT INTO lectures
            (title, filename, course_id)
            VALUES (?, ?, ?)
            """,
            (
                title,
                filename,
                course_id
            ))

            conn.commit()

            flash("✅ File Uploaded Successfully")

            return redirect(url_for("upload_material"))

    conn.close()

  
    return render_template(
        "upload_material.html",
        courses=courses
    )
# ================= STUDENT =================

@app.route("/student_profile")
def student_profile():
    return render_template("student_profile.html")

@app.route('/view_gpa')
def view_gpa():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    email = session.get("email")
    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email=?", (email,)
    ).fetchone()

    student = conn.execute(
        "SELECT * FROM students WHERE user_id=?", (user["id"],)
    ).fetchone()

    if not student:
        conn.close()
        return render_template("view_gpa.html", courses=None, name="Student", gpa=0)

    courses = conn.execute(
        "SELECT * FROM student_courses WHERE student_id=?", (student["id"],)
    ).fetchall()

    grade_points = {"A+": 4.0, "A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0}
    total_points = 0
    total_credits = 0

    for c in courses:
        points = grade_points.get(c["grade"], 0)
        total_points += points * c["credits"]
        total_credits += c["credits"]

    gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0

    conn.close()
    return render_template("view_gpa.html", courses=courses, name=user["name"], gpa=gpa)

# ================= STUDENT SUBMIT ASSIGNMENT =================

@app.route("/submit_assignment/<course_name>", methods=["POST"])
def submit_assignment(course_name):

    if session.get("role") != "student":
        return redirect(url_for("login"))

    file = request.files.get("file")

    if file and file.filename != "":

        filename = file.filename

        filepath = os.path.join(
            "static/files",
            filename
        )

        file.save(filepath)

        conn = sqlite3.connect("lms.db")
        cursor = conn.cursor()

        # حفظ submission

        cursor.execute("""
        INSERT INTO assignment_submissions
        (student_name,
         assignment_title,
         filename,
         course_name,
         submission_date)

        VALUES (?, ?, ?, ?, datetime('now'))
        """,
        (
            session.get("name"),
            "Assignment 1",
            filename,
            course_name
        ))

        # 🔔 Notification

        cursor.execute("""
        INSERT INTO notifications
        (message, created_at)

        VALUES (?, datetime('now'))
        """,
        (
            f"{session.get('name')} submitted assignment",
        ))

        conn.commit()
        conn.close()

        flash("Assignment submitted successfully ✅")

    return redirect(
        url_for(
            "course_details",
            course_name=course_name
        )
    )


@app.route("/view_submissions")
def view_submissions():

    if session.get("role") != "professor":
        return redirect(url_for("login"))

    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM assignment_submissions
    ORDER BY id DESC
    """)

    submissions = cursor.fetchall()

    conn.close()

    return render_template(
        "view_submissions.html",
        submissions=submissions
    )

@app.route("/test-ai")
def test_ai():

    import os
    from groq import Groq

    try:

        client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": "Say hello"
                }
            ],

            max_tokens=10

        )

        return response.choices[0].message.content

    except Exception as e:

        return str(e)
# ================= RUN =================
import os

if __name__ == "__main__":
    create_tables()
    insert_default_data()
    insert_random_students()
    insert_student_courses()

    print(" Server Started...")

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)