import sqlite3
from datetime import datetime

conn = sqlite3.connect('school.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE school (
    id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    phone_number CHAR(15),
    davlat_maktabi BOOLEAN
)
''')

cursor.execute('''
CREATE TABLE teacher (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone_number CHAR(15),
    school_id INTEGER,
    FOREIGN KEY (school_id) REFERENCES school (id)
)
''')

cursor.execute('''
CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    gender TEXT,
    school_id INTEGER,
    FOREIGN KEY (school_id) REFERENCES school (id)
)
''')

cursor.execute('''
CREATE TABLE class (
    id INTEGER PRIMARY KEY,
    name TEXT,
    teacher_id INTEGER,
    school_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id),
    FOREIGN KEY (school_id) REFERENCES school (id)
)
''')

cursor.execute('''
CREATE TABLE subject (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class_id INTEGER,
    teacher_id INTEGER,
    FOREIGN KEY (class_id) REFERENCES class (id),
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)
)
''')

cursor.execute('''
CREATE TABLE enrollment (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    class_id INTEGER,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (student_id) REFERENCES student (id),
    FOREIGN KEY (class_id) REFERENCES class (id)
)
''')

cursor.execute('''
CREATE TABLE grade (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    subject_id INTEGER,
    grade_value INTEGER,
    date_given DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (student_id) REFERENCES student (id),
    FOREIGN KEY (subject_id) REFERENCES subject (id)
)
''')

cursor.execute('''
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    class_id INTEGER,
    date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (student_id) REFERENCES student (id),
    FOREIGN KEY (class_id) REFERENCES class (id)
)
''')

# Insert
cursor.executemany('''
INSERT INTO school (name, address, phone_number, davlat_maktabi) VALUES (?, ?, ?, ?)
''', [
    ('School A', '123 Main St', '1234567890', True),
    ('School B', '456 Elm St', '0987654321', False)
])

cursor.executemany('''
INSERT INTO teacher (first_name, last_name, email, phone_number, school_id) VALUES (?, ?, ?, ?, ?)
''', [
    ('John', 'Doe', 'johndoe@example.com', '1234567890', 1),
    ('Jane', 'Smith', 'janesmith@example.com', '0987654321', 2)
])

cursor.executemany('''
INSERT INTO student (first_name, last_name, date_of_birth, gender, school_id) VALUES (?, ?, ?, ?, ?)
''', [
    ('Alice', 'Johnson', '2005-05-15', 'Female', 1),
    ('Bob', 'Brown', '2006-06-20', 'Male', 2)
])

cursor.executemany('''
INSERT INTO class (name, teacher_id, school_id) VALUES (?, ?, ?)
''', [
    ('Math 101', 1, 1),
    ('History 202', 2, 2)
])

cursor.executemany('''
INSERT INTO subject (name, class_id, teacher_id) VALUES (?, ?, ?)
''', [
    ('Algebra', 1, 1),
    ('World History', 2, 2)
])

cursor.executemany('''
INSERT INTO enrollment (student_id, class_id) VALUES (?, ?)
''', [
    (1, 1),
    (2, 2)
])

cursor.executemany('''
INSERT INTO grade (student_id, subject_id, grade_value) VALUES (?, ?, ?)
''', [
    (1, 1, 90),
    (2, 2, 85)
])

cursor.executemany('''
INSERT INTO attendance (student_id, class_id) VALUES (?, ?)
''', [
    (1, 1),
    (2, 2)
])

# Select and display data
for row in cursor.execute('SELECT * FROM school'):
    print(row)

# Rename tables
cursor.execute('ALTER TABLE school RENAME TO educational_institution')
cursor.execute('ALTER TABLE teacher RENAME TO educator')

# Rename columns
cursor.execute('ALTER TABLE educational_institution RENAME COLUMN phone_number TO contact_number')
cursor.execute('ALTER TABLE student RENAME COLUMN date_of_birth TO birth_date')
cursor.execute('ALTER TABLE student RENAME COLUMN gender TO sex')

# Add new columns
cursor.execute('ALTER TABLE educator ADD COLUMN middle_name TEXT')
cursor.execute('ALTER TABLE student ADD COLUMN nationality TEXT')

# Remove a column
cursor.execute('ALTER TABLE grade DROP COLUMN date_given')

# Update data
cursor.execute('UPDATE educational_institution SET name = ? WHERE id = ?', ('Updated School A', 1))
cursor.execute('UPDATE educator SET last_name = ? WHERE id = ?', ('Updated Doe', 1))
cursor.execute('UPDATE student SET first_name = ? WHERE id = ?', ('Updated Alice', 1))
cursor.execute('UPDATE class SET name = ? WHERE id = ?', ('Updated Math 101', 1))

# Delete data
cursor.execute('DELETE FROM grade WHERE id = ?', (1,))
cursor.execute('DELETE FROM enrollment WHERE id = ?', (1,))
cursor.execute('DELETE FROM attendance WHERE id = ?', (1,))
cursor.execute('DELETE FROM subject WHERE id = ?', (1,))

# Commit and close connection
conn.commit()
conn.close()

