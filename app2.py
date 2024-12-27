import streamlit as st
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create tables if not already present
cursor.execute("""
CREATE TABLE IF NOT EXISTS StudentsMarksheet (
    UniqueStudentRegNo TEXT,
    Class TEXT,
    Section TEXT,
    TestTerm TEXT,
    Tamil INTEGER,
    English INTEGER,
    Maths INTEGER,
    Science INTEGER,
    SocialScience INTEGER,
    Total INTEGER,
    Average REAL,
    Grade TEXT,
    FOREIGN KEY (UniqueStudentRegNo) REFERENCES StudentsMaster (UniqueStudentRegNo)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS StudentsMaster (
    StudentName TEXT,
    Gender TEXT,
    DOB TEXT,
    FatherName TEXT,
    MotherName TEXT,
    FathersOccupation TEXT,
    FathersIncome REAL,
    BloodGroup TEXT,
    Address TEXT,
    City TEXT,
    State TEXT,
    DateOfJoining TEXT,
    DateOfRecordCreation TEXT,
    UniqueStudentRegNo TEXT PRIMARY KEY
)
""")
conn.commit()

# Streamlit app
st.title("Student Database Management")

# Add data to the database
if st.button("Add"):
    st.header("Add Student Information")

    # StudentsMaster table inputs
    st.subheader("Student Master Details")
    student_id = st.text_input("Unique Student Registration Number:")
    student_name = st.text_input("Student Name:")
    gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
    dob = st.date_input("Date of Birth:")
    father_name = st.text_input("Father's Name:")
    mother_name = st.text_input("Mother's Name:")
    fathers_occupation = st.text_input("Father's Occupation:")
    fathers_income = st.number_input("Father's Income:", min_value=0.0, step=1000.0)
    blood_group = st.selectbox("Blood Group:", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    address = st.text_area("Address:")
    city = st.text_input("City:")
    state = st.text_input("State:")
    date_of_joining = st.date_input("Date of Joining:")
    date_of_record_creation = st.date_input("Date of Record Creation:")

    # StudentsMarksheet table inputs
    st.subheader("Student Marksheet Details")
    student_class = st.text_input("Class:")
    section = st.text_input("Section:")
    test_term = st.text_input("Test Term:")
    tamil = st.number_input("Marks in Tamil:", min_value=0, max_value=100, step=1)
    english = st.number_input("Marks in English:", min_value=0, max_value=100, step=1)
    maths = st.number_input("Marks in Maths:", min_value=0, max_value=100, step=1)
    science = st.number_input("Marks in Science:", min_value=0, max_value=100, step=1)
    social_science = st.number_input("Marks in Social Science:", min_value=0, max_value=100, step=1)

    # Calculate total, average, and grade
    total = tamil + english + maths + science + social_science
    average = total / 5
    grade = (
        "Fail" if min(tamil, english, maths, science, social_science) < 50 else
        "A" if average >= 80 else
        "B" if average >= 60 else
        "C" if average >= 50 else "D"
    )

    # Save data to the database
    if st.button("Submit"):
        try:
            cursor.execute("""
            INSERT INTO StudentsMaster (
                StudentName, Gender, DOB, FatherName, MotherName, FathersOccupation, FathersIncome,
                BloodGroup, Address, City, State, DateOfJoining, DateOfRecordCreation, UniqueStudentRegNo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_name, gender, dob, father_name, mother_name, fathers_occupation, fathers_income,
                  blood_group, address, city, state, date_of_joining, date_of_record_creation, student_id))

            cursor.execute("""
            INSERT INTO StudentsMarksheet (
                UniqueStudentRegNo, Class, Section, TestTerm, Tamil, English, Maths, Science, SocialScience,
                Total, Average, Grade
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, student_class, section, test_term, tamil, english, maths, science, social_science,
                  total, average, grade))

            conn.commit()
            st.success("Student information added successfully!")
        except Exception as e:
            st.error(f"Error adding data: {e}")

# View data from the database
if st.button("View"):
    st.header("View Student Information")

    query = """
    SELECT 
        StudentsMarksheet.UniqueStudentRegNo AS StudentID,
        StudentsMaster.StudentName,
        StudentsMarksheet.Average,
        StudentsMarksheet.Grade
    FROM 
        StudentsMarksheet
    JOIN 
        StudentsMaster
    ON 
        StudentsMarksheet.UniqueStudentRegNo = StudentsMaster.UniqueStudentRegNo
    """

    try:
        # Read data using pandas
        student_data = pd.read_sql(query, conn)
        st.subheader("Student Performance Table")
        st.dataframe(student_data)
    except Exception as e:
        st.error(f"Error fetching data: {e}")

# Close the database connection when done
conn.close()
