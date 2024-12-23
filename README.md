# Chat BOT Application

This repository contains the code and resources for the Chat BOT application, which includes features for AI-powered queries, CRUD operations, and data visualizations. The application is designed to interact with a student database, enabling advanced querying, real-time database updates, and insightful visualizations.

---

## Features

### 1. **AI Queries**
The application interprets natural language prompts in English and generates accurate Python or SQL queries along with their results. Examples of supported prompts include:
- **"List students with grades above B in Term 2."**
- **"Who are the top-performing students from low-income families?"**
  (Low-income families are defined as those with an income below ₹200,000.)
- **"Which students failed any subject in the last exam?"**

### 2. **CRUD Operations**
- Perform real-time **Create**, **Read**, **Update**, and **Delete** operations on the database.
- View dynamic data changes before and after the operations.

### 3. **Visualizations**
- A bar chart displaying the number of students admitted per year.
- Real-time marks data visualized from the student database.

---

## Installation

### Prerequisites
- Ensure Python is installed on your system.
- Obtain the Gemini AI API key from the [Gemini AI Studio](https://aistudio.google.com/apikey) by clicking on "Create API Key."

### Steps to Run
1. Clone the repository:
   ```bash
   git clone <repository_link>
   cd <repository_name>
   ```
   Or you can doenload the code into your folder
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add the API key to `api_key.txt`:
   - Create a file named `api_key.txt` in the project directory.
   - Paste the API key into the file (ensure it contains only the key, with no additional text).

5. Run the application:
   ```bash
   streamlit run app.py
   ```
   If the above command does not work, try:
   ```bash
   python -m streamlit run app.py
   ```

---

## Submission Links

- **GitHub Repository:** [Link to Repository]([#](https://github.com/monishavenkatesh7/AI-Student-Enquiry-Chatbot/tree/main))
- **Google Drive Link:** [Link to Drive](#)
- **Installation, Demo, and Explanation Video:** [Link to Video](#)

---

## Notes

- Ensure you are connected to the internet while running the application.
- Detailed explanation of the setup process is included in the demo video.

---

## License

This project is licensed under a **Personal License**. Unauthorized distribution, reproduction, or commercial use of this software is prohibited without explicit permission.

---

## Acknowledgments

Thank you for the opportunity to work on this assignment. For any queries or issues, please feel free to raise an issue in this repository or contact us via email.
