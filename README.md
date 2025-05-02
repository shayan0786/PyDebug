# PyDebug 🐍🛠️

## 👨‍💻 A Flask-Based Python Debugging Chatbot (Partial AI Integration)

**PyDebug** is a web-based Python code debugging assistant built using Flask. It simulates an AI chatbot that helps users analyze and correct Python code. The **Debugger section is powered by Gemini API**, while the **Home page currently runs dummy logic** for testing purposes.

---

## 🎯 Project Purpose

This is a student project built as part of a self-learning program:  
📘 **"Learn Python - Section 1 to Section 6"**

Goals:
- Learn Flask web development
- Implement AI-based code debugging using Gemini API
- Create a structured learning chatbot for beginners

---

## ⚙️ Features

- 🧠 **Debugger Section:** Uses **Gemini API** to analyze and fix buggy Python code
- 💬 **Home Chatbot Section:** Dummy logic using random messages (for layout testing)
- 🧾 3-Panel Output:
  - **Buggy Code Output**
  - **Line-by-line Error Analysis & Fix Suggestions**
  - **Fully Corrected Code**
- 💡 Shows useful Python tips after debugging

---

## 🗃️ Project Structure

PyDebug/
│
├── templates/ # All HTML pages
│ ├── index.html # Homepage with dummy chatbot
│ ├── debugger.html # Functional Gemini debugger
│ ├── learnpy.html # Python Learning main page
│ ├── section1py.html # Section 1: Introduction
│ ├── section2py.html # Section 2: Variables & Data Types
│ ├── section3py.html # Section 3: Conditional Statements
│ ├── section4py.html # Section 4: Loops
│ ├── section5py.html # Section 5: Functions
│ ├── section6py.html # Section 6: Error Handling
│
├── app.py # Main Flask application
├── test_gemini.py # Testing Gemini debugger separately
├── README.md # Project documentation
└── requirements.txt # All dependencies
---

## AI Integration

The project uses the **Gemini API** (via Google Generative AI Python library) to:
- Analyze the provided Python code
- Identify logical or syntactical issues
- Generate detailed error messages and explanations
- Return corrected and working code snippets
- Provide best practices and Python tips

Only the **Debugger section** uses this AI logic. The homepage chatbot is currently non-functional and will be updated in future versions.

---

## Python Topics Covered (Learning Scope)

This project aligns with the following foundational Python sections:

1. **Introduction to Python**
2. **Variables and Data Types**
3. **Conditional Statements**
4. **Loops (for, while)**
5. **Functions**
6. **Error Handling and Debugging**

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection for Gemini API access

### Steps

1. Clone the repository:

```bash
git clone https://github.com/shayan0786/PyDebug.git
cd PyDebug
