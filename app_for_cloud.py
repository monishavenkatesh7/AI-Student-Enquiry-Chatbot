import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import google.generativeai as genai

# Database Connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Read the API key from the text file
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()

# Configure Google Generative AI
YOUR_API_KEY = api_key
genai.configure(api_key=YOUR_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# App Title
st.title("AI-Powered Student Inquiry Application")

# Sidebar for Navigation
st.sidebar.title("Navigation")
options = ["Home", "CRUD Operations", "AI Queries", "Visualizations"]
choice = st.sidebar.radio("Select Option", options)

# Load Data
df = pd.read_sql("SELECT * FROM joinedstudents", conn)

# Home Section
if choice == "Home":
    st.header("Welcome to the Student Inquiry App")
    st.write("Use the sidebar to navigate between features.")

# CRUD Operations
elif choice == "CRUD Operations":
    st.header("Perform CRUD Operations")
    action = st.radio("Select Action", ["Add", "View", "Update", "Delete"], horizontal=True)

    if action == "Add":
        with st.form("add_form"):
            student_data = {
                "StudentName": st.text_input("Student Name"),
                "Gender": st.selectbox("Gender", ["Male", "Female", "Other"]),
                "DOB": st.date_input("Date of Birth"),
                "FatherName": st.text_input("Father's Name"),
                "MotherName": st.text_input("Mother's Name"),
                "FathersOccupation": st.text_input("Father's Occupation"),
                "FathersIncome": st.number_input("Father's Income", min_value=0),
                "BloodGroup": st.text_input("Blood Group"),
                "Address": st.text_area("Address"),
                "City": st.text_input("City"),
                "State": st.text_input("State"),
                "DateOfJoining": st.date_input("Date of Joining"),
                "DateOfRecordCreation": st.date_input("Date of Record Creation"),
                "UniqueStudentRegNo": st.text_input("Unique Registration Number")
            }
            if st.form_submit_button("Add Student"):
                query = """
                INSERT INTO joinedstudents 
                (StudentName, Gender, DOB, FatherName, MotherName, FathersOccupation, FathersIncome, BloodGroup, Address, City, State, DateOfJoining, DateOfRecordCreation, UniqueStudentRegNo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, tuple(student_data.values()))
                conn.commit()
                st.success("Student added successfully!")

    elif action == "View":
        st.dataframe(df)

    elif action == "Update":
        reg_no = st.text_input("Enter the Unique Registration Number of the student to update")

        if reg_no:
            query = f"SELECT * FROM joinedstudents WHERE UniqueStudentRegNo = '{reg_no}'"
            student_data = pd.read_sql(query, conn)

            if not student_data.empty:
                st.write("Current Record:")
                st.dataframe(student_data)

                updated_data = {}
                for column in student_data.columns:
                    if column != "UniqueStudentRegNo":
                        value = student_data[column].iloc[0]
                        if isinstance(value, (int, float)):
                            updated_data[column] = st.number_input(column, value=value)
                        elif isinstance(value, str):
                            updated_data[column] = st.text_input(column, value=value)
                        else:
                            updated_data[column] = st.text_area(column, value=str(value))

                if st.button("Update Record"):
                    update_query = f"""
                    UPDATE joinedstudents
                    SET {", ".join([f"{col} = '{val}'" for col, val in updated_data.items()])}
                    WHERE UniqueStudentRegNo = '{reg_no}'
                    """
                    cursor.execute(update_query)
                    conn.commit()
                    st.success("Record updated successfully!")
            else:
                st.error("No student found with this registration number.")

    elif action == "Delete":
        reg_no = st.text_input("Enter the Unique Registration Number of the student to delete")

        if reg_no and st.button("Delete Record"):
            query = f"SELECT * FROM joinedstudents WHERE UniqueStudentRegNo = '{reg_no}'"
            student_data = pd.read_sql(query, conn)

            if not student_data.empty:
                delete_query = f"DELETE FROM joinedstudents WHERE UniqueStudentRegNo = '{reg_no}'"
                cursor.execute(delete_query)
                conn.commit()
                st.success("Record deleted successfully!")
            else:
                st.error("No student found with this registration number.")

# AI Queries
elif choice == "AI Queries":
    st.header("AI-Powered Queries")

    # Prompt the user to input their Gemini API key
    api_key = st.text_input("""Enter your Gemini API Key
    you can get free gemini API Key from here https://aistudio.google.com/apikey""", type="password")

    if api_key:
        # Configure Google Generative AI using the entered API key
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat()

        user_message = st.text_area(
            """
            Enter your question based on the database. 
            Follow these rules for better results:
            1. Use keywords from the columns: {}
            2. Avoid punctuation and abbreviations.
            3. Be precise and clear.
            4. If it shows an error, try the same prompt again with the same rules above. It must work fine.

            Example Prompts:
            - Show all students admitted in 2024
            - List students with grades above B in Term 2
            - Who are the top-performing students from low-income families (less than 200,000 income)?
            - Which students failed any subject in the last exam?
            """.format(", ".join(list(df.columns)))
        )

        if st.button("Submit Query"):
            query = f'''
            I have a SQL table named JoinedStudents with the following columns: {df.columns}.
            Please generate a SQL query to fulfill the following request:
            {user_message}.
            Provide the SQL code without explanations or extra text.
            '''
            try:
                response = chat.send_message(query)
                sql_query = response.text.strip()

                # Extract the SQL query portion
                k = sql_query
                k1 = k.split('sql\n')[-1]
                k2 = k1.split(';')[0]

                sql_query = k2

                st.code(sql_query, language="sql")

                # Execute and display the SQL query result
                try:
                    result = pd.read_sql(sql_query, conn)
                    st.dataframe(result)
                except Exception as e:
                    st.error(f"Error executing query: {e}")
            except Exception as e:
                st.error(f"Error generating SQL query: {e}")
    else:
        st.warning("Please enter your Gemini API key to proceed.")

elif choice == "Visualizations":
    st.header("Data Visualizations")

    if "dateofjoining" in df.columns:
        if df["dateofjoining"].dtype != "object":
            df["dateofjoining"] = df["dateofjoining"].astype(str)
        admission_stats = df.groupby(df["dateofjoining"].str[:4])["uniquestudentregno"].count()
        st.subheader("Admissions Per Year")
        st.bar_chart(admission_stats)
    else:
        st.error("The 'dateofjoining' column is missing.")

    # SQL Query to fetch performance data
    query = """
    SELECT 
        StudentsMarksheet.UniqueStudentRegNo AS StudentID,
        StudentsMaster.StudentName,
        StudentsMarksheet.Average,
        CASE 
            WHEN (Tamil < 50 OR English < 50 OR Maths < 50 OR Science < 50 OR SocialScience < 50) THEN 'Fail'
            ELSE CASE 
                WHEN StudentsMarksheet.Average >= 80 THEN 'A'
                WHEN StudentsMarksheet.Average >= 60 THEN 'B'
                WHEN StudentsMarksheet.Average >= 50 THEN 'C'
                ELSE 'D'
            END
        END AS Grade
    FROM 
        StudentsMarksheet
    JOIN 
        StudentsMaster
    ON 
        StudentsMarksheet.UniqueStudentRegNo = StudentsMaster.UniqueStudentRegNo
    """

    # Read the SQL query into a DataFrame
    try:
        performance_table = pd.read_sql(query, conn)
        st.subheader("Student Performance Summary")
        st.dataframe(performance_table)
    except Exception as e:
        st.error(f"Error fetching performance data: {e}")

# Close the database connection
conn.close()
