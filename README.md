# CodeSense — AI Code Reviewer

CodeSense is an AI-powered code review application that analyzes source code and provides professional feedback on bugs, security, performance, readability, code quality, and refactoring.

## Features

* Bug and error detection
* Security analysis
* Performance analysis
* Readability evaluation
* Code quality review
* Refactoring suggestions
* Time and space complexity analysis
* Simple code explanations
* Refactored code suggestions
* Quick Scan and Deep Review modes

## Technologies

* Python
* Streamlit
* Google Gemini API
* python-dotenv

## Project Structure

```text
CodeSense/
│
├── app.py
├── reviewer.py
├── requirements.txt
├── .gitignore
└── README.md
```

### app.py

Contains the Streamlit user interface and handles user input.

### reviewer.py

Contains the AI code review logic and Gemini API integration.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CodeSense
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## API Key Setup

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload the `.env` file or your API key to GitHub.

Make sure `.env` is included in `.gitignore`.

## Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## How It Works

```text
User enters source code
        ↓
Selects review depth
        ↓
Code is sent to the AI model
        ↓
Code analysis
        ↓
Bug, security and performance review
        ↓
Complexity analysis
        ↓
Refactoring suggestions
        ↓
Review displayed in Streamlit
```

## Example

Input:

```python
def add(a, b):
    return a - b

print(add(10, 5))
```

CodeSense analyzes the code and identifies potential logical issues and improvements.

## Future Improvements

* Automatic code fixing
* Syntax highlighting
* Downloadable review reports
* Code review history
* GitHub repository integration
* Test-case generation
* Support for additional programming languages

## Author

**Archana Nadakattin**

A project developed to explore AI-assisted software development and automated code review.
