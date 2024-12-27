import streamlit as st
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# Create the tables if they don't exist
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
conn.commit()

# Streamlit app
st.title("Student Management System")

# Add Button
if st.button("Add"):
    st.subheader("Add Student Details")
    
    # Input for StudentsMaster
    st.write("### Basic Details")
    student_name = st.text_input("Student Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    dob = st.date_input("Date of Birth")
    father_name = st.text_input("Father's Name")
    mother_name = st.text_input("Mother's Name")
    fathers_occupation = st.text_input("Father's Occupation")
    fathers_income = st.number_input("Father's Income", min_value=0.0, step=100.0)
    blood_group = st.text_input("Blood Group")
    address = st.text_area("Address")
    city = st.text_input("City")
    state = st.text_input("State")
    date_of_joining = st.date_input("Date of Joining")
    record_creation_date = st.date_input("Record Creation Date")
    unique_reg_no = st.text_input("Unique Student Registration Number")
    
    # Input for StudentsMarksheet
    st.write("### Marks Details")
    student_class = st.text_input("Class")
    section = st.text_input("Section")
    test_term = st.text_input("Test Term")
    tamil = st.number_input("Tamil Marks", min_value=0, max_value=100, step=1)
    english = st.number_input("English Marks", min_value=0, max_value=100, step=1)
    maths = st.number_input("Maths Marks", min_value=0, max_value=100, step=1)
    science = st.number_input("Science Marks", min_value=0, max_value=100, step=1)
    social_science = st.number_input("Social Science Marks", min_value=0, max_value=100, step=1)

    # Calculate total, average, and grade
    total = tamil + english + maths + science + social_science
    average = total / 5
    grade = (
        "A" if average >= 80 else
        "B" if average >= 60 else
        "C" if average >= 50 else
        "D"
    )
    
    # Save to the database
    if st.button("Submit"):
        try:
            cursor.execute("""
                INSERT INTO StudentsMaster (
                    StudentName, Gender, DOB, FatherName, MotherName, FathersOccupation,
                    FathersIncome, BloodGroup, Address, City, State, DateOfJoining,
                    DateOfRecordCreation, UniqueStudentRegNo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_name, gender, dob, father_name, mother_name, fathers_occupation,
                fathers_income, blood_group, address, city, state, date_of_joining,
                record_creation_date, unique_reg_no
            ))
            
            cursor.execute("""
                INSERT INTO StudentsMarksheet (
                    UniqueStudentRegNo, Class, Section, TestTerm, Tamil, English, Maths,
                    Science, SocialScience, Total, Average, Grade
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                unique_reg_no, student_class, section, test_term, tamil, english, maths,
                science, social_science, total, average, grade
            ))
            
            conn.commit()
            st.success("Student details added successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

# View Button
if st.button("View"):
    st.subheader("Student Performance Data")
    
    # SQL Query to fetch required data
    query = """
    SELECT 
        StudentsMarksheet.UniqueStudentRegNo AS StudentID,
        StudentsMaster.StudentName AS Name,
        StudentsMarksheet.Average AS AverageMarks,
        StudentsMarksheet.Grade AS Grade
    FROM 
        StudentsMarksheet
    JOIN 
        StudentsMaster
    ON 
        StudentsMarksheet.UniqueStudentRegNo = StudentsMaster.UniqueStudentRegNo
    """
    
    # Fetch data into a DataFrame
    try:
        data = pd.read_sql(query, conn)
        st.dataframe(data)
    except Exception as e:
        st.error(f"Error fetching data: {e}")

# Close the database connection at the end
conn.close()
