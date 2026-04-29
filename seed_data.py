import sqlite3

conn = sqlite3.connect("lms.db")
cursor = conn.cursor()

# امسح القديم
cursor.execute("DELETE FROM lectures")
cursor.execute("DELETE FROM courses")

# ================= COURSES =================

courses = [

("GIS","Dr. Nermeen Lauz","Monday","10:00 AM – 12:00 PM","Room R106"),

("English 8","Dr. Ahmed","Tuesday","12:00 PM – 2:00 PM","Room R204"),

("Data Mining","Dr. Mohamed","Wednesday","2:00 PM – 4:00 PM","Room R305"),

("Mobile Computing","Dr. Sara","Thursday","9:00 AM – 11:00 AM","Room R101"),

("IT Project Management","Dr. Khaled","Sunday","11:00 AM – 1:00 PM","Room R202"),

# ✅ DSS الجديد
("DSS","Dr. Lamiaa","Monday","12:00 PM – 2:00 PM","Room R106")

]

cursor.executemany(

"INSERT INTO courses (name,doctor,day,time,room) VALUES (?,?,?,?,?)",

courses

)

# ================= GET GIS ID =================

cursor.execute(
"SELECT id FROM courses WHERE name='GIS'"
)

gis_id = cursor.fetchone()[0]

# GIS Chapters

gis_lectures = [

(gis_id,"Chapter 1","CH1.pdf"),
(gis_id,"Chapter 2","CH2.pdf"),
(gis_id,"Chapter 3","CH3.pdf"),
(gis_id,"Chapter 4","CH4.pdf"),
(gis_id,"Chapter 5","CH5.pdf"),
(gis_id,"Chapter 6","CH6.pdf")

]

cursor.executemany(

"INSERT INTO lectures (course_id,title,filename) VALUES (?,?,?)",

gis_lectures

)

# ================= GET DSS ID =================

cursor.execute(
"SELECT id FROM courses WHERE name='DSS'"
)

dss_id = cursor.fetchone()[0]

# DSS Lectures

dss_lectures = [

(dss_id,"Lecture 1","Lecture 1.pdf"),
(dss_id,"Lecture 2","Lecture 2.pdf"),
(dss_id,"Lecture 3","Lecture 3.pdf"),
(dss_id,"Lecture 4","Lecture 4.pdf")

]

cursor.executemany(

"INSERT INTO lectures (course_id,title,filename) VALUES (?,?,?)",

dss_lectures

)

conn.commit()
conn.close()

print("Data Inserted Successfully")