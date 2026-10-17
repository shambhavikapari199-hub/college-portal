# KLES RLSI College Belagavi Website

## About the Project
The KLES RLSI College Belagavi Website is a web application developed using Python and Streamlit. It helps manage student information and provides a simple interface for accessing college-related features.

## Features
- **Home Page:** Displays the college name and welcome message.
- **Student Registration:** Allows users to enter student details.
- **Student Records:** Displays registered student information.
- **Student Profile:** Provides student profile details.
- **Attendance:** Helps record or view student attendance.
- **Exam Details:** Displays examination-related information.
- **Subjects:** Provides subject-related information.
- **AI Assistant:** Uses Google Gemini API to generate answers to study-related questions.
- **About Page:** Displays information about the project.

## Technologies Used
- Python
- Streamlit
- SQLite Database
- Google Gemini API
- HTML and CSS

## Project Structure

```text
collegewebsite/
│
├── app.py
├── test_gemini.py
├── requirements.txt
├── college.db
├── college_logo.png
└── README.md
```

*Note: The files listed above depend on your actual project. Remove any file that you do not have.*

## Installation and Setup

### 1. Install Python
Download and install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).

### 2. Open the Project
Open the `collegewebsite` folder in Visual Studio Code.

### 3. Install Required Libraries

Open the VS Code terminal and run:

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

For Windows PowerShell, run the following command in the VS Code terminal:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your actual API key. Keep it private.

### 5. Run the Website

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The website will open in your browser. If it does not open automatically, follow the local URL displayed in the terminal.

## Database
The project uses SQLite to store student information. The database file is named `college.db`, if included in your project.

## AI Assistant
The AI Assistant uses the Google Gemini API to generate responses to study-related questions. An internet connection and a valid API key are required. API usage limits may apply.

## Future Enhancements
- Student login and authentication
- Improved dashboard design
- Attendance reports
- Examination performance reports
- Better student data management
- Additional AI-powered learning features

## Developed For
**KLES RLSI College, Belagavi**

## License
This project is intended for educational and academic purposes.
