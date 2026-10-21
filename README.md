# 🎓 EduAssist AI
### Your Personal AI Academic Assistant

<p align="center">
  <b>Deep Learning × Cloud Computing</b><br>
  Transforming student performance data into personalized academic insights with AI and cloud-based report storage.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Domain-Deep%20Learning-7257E8?style=for-the-badge&logo=pytorch&logoColor=white" alt="Deep Learning"/>
  <img src="https://img.shields.io/badge/Domain-Cloud%20Computing-FF9900?style=for-the-badge&logo=icloud&logoColor=white" alt="Cloud Computing"/>
  <img src="https://img.shields.io/badge/Python-Backend-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/AWS-S3%20Storage-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS S3"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn"/>
  <img src="https://img.shields.io/badge/Ollama-Local%20LLM-111111?style=flat-square&logo=ollama&logoColor=white" alt="Ollama"/>
  <img src="https://img.shields.io/badge/Status-Academic%20Project-20A67A?style=flat-square" alt="Academic Project"/>
</p>

---

## 🌟 Overview

**EduAssist AI** is an AI-powered academic assistance platform developed as an interdisciplinary project combining **Deep Learning and Cloud Computing**.

It analyzes student academic data, presents performance insights, identifies areas that may need improvement, and enables students to interact with an AI-powered academic assistant. The platform also generates student performance reports as PDF files and stores them in **Amazon S3**.

Instead of presenting academic data as numbers alone, EduAssist AI aims to make that information easier to understand and use for academic planning.

### 💡 What makes it special?

- 🧠 **Intelligent analysis:** Uses trained machine-learning models to support academic performance and risk analysis.
- 💬 **AI academic assistant:** Answers student questions using an NLP-based question-routing pipeline and AI response generation.
- 📊 **Performance insights:** Presents academic summaries, weak areas, and recommendations based on available student data.
- 📄 **PDF report generation:** Creates downloadable academic report content through the backend report workflow.
- ☁️ **Cloud integration:** Uploads generated PDF reports to Amazon S3.
- 🔄 **End-to-end workflow:** Connects a React interface, a FastAPI backend, AI components, and cloud object storage.

---

## 🎯 Project Objectives

1. Apply machine learning and AI techniques to student academic data.
2. Make academic performance information accessible through an interactive dashboard.
3. Provide conversational access to student-specific academic insights.
4. Generate structured PDF performance reports.
5. Integrate AWS cloud storage for report persistence.
6. Demonstrate the practical application of AI and cloud computing in education.

---

## 🧠 Deep Learning & AI Component

The AI component combines academic data processing, trained predictive models, question-intent handling, retrieval-based context, and language-model responses.

### Core capabilities

| Component | Purpose |
|---|---|
| Student Intelligence | Retrieves and processes academic information for the selected student. |
| Performance Prediction | Uses a trained Gradient Boosting Regressor to estimate academic performance. |
| Risk Classification | Uses a trained Random Forest Classifier for student-risk classification. |
| NLP Intent Engine | Identifies the type of academic question and helps route it to the relevant processing logic. |
| RAG Knowledge Retrieval | Uses a retrieval pipeline to supply relevant context to supported AI queries. |
| LLM Response Engine | Uses a local language model through Ollama to generate conversational responses. |
| Academic Insights | Organizes student information into understandable performance insights. |

### 🤖 AI assistant workflow

```text
       Student Question
              │
              ▼
       NLP Intent Engine
              │
              ▼
      Student Intelligence
              │
              ▼
       Academic Insights
              │
              ▼
        RAG Knowledge
              │
              ▼
        LLM Response
              │
              ▼
     Personalized AI Answer
```

*The exact processing path may vary by question type. The models and components contribute different functions; not every component is a deep-learning model.*

### Example student questions

- What is my current performance?
- What are my weak areas?
- Am I improving?
- How can I improve my performance?
- Give me an overall analysis.
- Create a study plan for me.

---

## ☁️ Cloud Computing Component

EduAssist AI integrates **Amazon Web Services (AWS), specifically Amazon S3**, to store generated academic reports.

### 📄 Student report workflow

```text
     Load Student in Dashboard
                │
                ▼
      Request Report Generation
                │
                ▼
        FastAPI Backend
                │
                ▼
     Prepare Student Report Data
                │
                ▼
         Generate PDF
                │
                ▼
       Upload PDF Using Boto3
                │
                ▼
         Amazon S3 Bucket
          (eduassist-ai)
```

### Cloud features

- **Amazon S3:** Stores generated PDF reports as cloud objects.
- **Boto3:** Connects the Python backend to AWS services.
- **FastAPI:** Exposes the backend report-generation endpoint.
- **Report generation:** Creates a PDF for the selected student when requested.
- **Timestamped object keys:** Helps distinguish reports generated at different times.

The report endpoint is:

```http
POST /student/{student_id}/report
```

The backend returns information about the generated report and its S3 object key when the operation succeeds.

**Cloud architecture note:** The current implementation integrates S3 storage. It does not imply that the entire application is deployed on AWS.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| Student selection | Load a student using their ID. |
| Academic dashboard | View available student performance metrics. |
| Performance prediction | Access predictions from the trained model. |
| Risk classification | View the risk category produced by the trained classifier. |
| AI chat assistant | Ask questions about student academic performance. |
| Academic insights | Review available strengths, weaknesses, and improvement guidance. |
| Study assistance | Request guidance and study-planning suggestions. |
| PDF report generation | Generate a report for the currently selected student. |
| AWS S3 integration | Save generated reports in cloud object storage. |
| Responsive interface | Access the React dashboard on supported screen sizes. |

---

## 🛠️ Technology Stack

### AI, Machine Learning & NLP

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/FAISS-Vector%20Search-0467DF?style=flat-square" alt="FAISS"/>
  <img src="https://img.shields.io/badge/Ollama-Local%20LLM-111111?style=flat-square&logo=ollama&logoColor=white" alt="Ollama"/>
</p>

- Python
- scikit-learn
- Pandas and NumPy
- Gradient Boosting Regressor
- Random Forest Classifier
- FAISS-based retrieval
- Sentence Transformers for embeddings
- Ollama with the configured `llama3.2:3b` model

### Cloud Computing

<p>
  <img src="https://img.shields.io/badge/Amazon%20S3-569A31?style=flat-square&logo=amazons3&logoColor=white" alt="Amazon S3"/>
  <img src="https://img.shields.io/badge/AWS%20SDK-Boto3-232F3E?style=flat-square&logo=amazonaws&logoColor=white" alt="Boto3"/>
</p>

- Amazon Simple Storage Service (Amazon S3)
- AWS SDK for Python (Boto3)
- Cloud object storage
- PDF report upload workflow

### Application Development

<p>
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/ReportLab-PDF%20Generation-336699?style=flat-square" alt="ReportLab"/>
</p>

- React and Vite
- Python and FastAPI
- REST APIs
- ReportLab for PDF generation
- CSS for responsive dashboard styling

---

## 🏗️ Project Structure

```text
EduAssist-AI/
│
├── backend/
│   ├── main.py
│   ├── s3_storage.py
│   ├── student_report.py
│   ├── requirements.txt
│   ├── student_intelligence.py
│   ├── academic_insights.py
│   ├── ai_orchestrator.py
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── Dataset/
│   └── OULAD/
│
├── .gitignore
└── README.md
```

*The tree highlights key files and known project components. Other files and folders may exist in your local repository.*

---

## 🚀 Getting Started

Follow these steps to run EduAssist AI locally on Windows.

### 1. Prerequisites

Install or prepare:

- Python 3.11
- Node.js and npm
- Git
- AWS account with an S3 bucket and appropriate permissions
- Ollama, if using the local LLM and RAG/chat pipeline
- The required datasets and trained model files

### 2. Clone the repository

```bash
git clone https://github.com/Sakshi-Zurale/EduAssist-AI.git
cd EduAssist-AI
```

### 3. Set up the Python backend

From the project root, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

If a required Python package is missing, install it in the active environment according to the project's dependency configuration.

### 4. Configure AWS S3

Configure AWS credentials securely using an AWS profile, environment variables, or an appropriate IAM role.

For local development, one option is:

```powershell
aws configure
```

Install the AWS CLI separately if you want to use that command. The application itself uses Boto3.

Verify that the backend configuration matches your bucket and AWS region. The current project configuration uses:

```text
Bucket: eduassist-ai
Region: ap-southeast-2
```

Ensure the configured AWS identity has permission to upload objects to the required bucket and prefix.

**Security:** Never commit AWS access keys, secret keys, `.env` files containing credentials, or other secrets to GitHub. Keep the bucket private unless you have a specific reason to expose its contents.

### 5. Start the backend

From the repository root:

```powershell
python -m uvicorn backend.main:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, commonly:

```text
http://localhost:5173
```

### 7. Run the AI assistant

If the chat workflow uses Ollama, ensure Ollama is installed, the configured model is available, and the local Ollama service is running. The current model configuration is:

```text
llama3.2:3b
```

The trained model files, dataset paths, and any retrieval resources must also be available in the locations expected by the backend.

---

## 📄 Generate a Student Report

1. Open the EduAssist AI dashboard.
2. Enter a valid student ID.
3. Load the student profile.
4. Select **Generate Report & Save to S3**.
5. Wait for the backend to generate the PDF and upload it.
6. Check the success message for the returned S3 object key.
7. Verify the stored object in the configured S3 bucket.

The backend report endpoint can also be tested through Swagger:

```http
POST /student/11391/report
```

Replace `11391` with another valid student ID.

Example object-key pattern:

```text
reports/student_11391_<timestamp>.pdf
```

Each report request creates a new timestamped object key, allowing reports for the same student to be stored separately.

---

## 🔐 Security & Data Handling

- Keep AWS credentials outside source control.
- Use least-privilege IAM permissions for report uploads.
- Keep student reports in a private S3 bucket.
- Avoid exposing student-identifiable information in public logs or screenshots.
- Use only datasets and student information that you are authorized to process.
- Do not place credentials or sensitive student data in GitHub issues or commits.

---

## 🎓 Academic Relevance

This project demonstrates concepts from two complementary subjects.

### Subject 1 — Deep Learning

- AI-powered conversational interfaces
- Language models and NLP
- Embedding-based semantic retrieval
- Retrieval-Augmented Generation (RAG)
- Machine-learning-based performance prediction
- Student-risk classification and data-driven insights

### Subject 2 — Cloud Computing

- Cloud object storage with Amazon S3
- AWS SDK integration using Boto3
- API-driven cloud operations
- Programmatic PDF report uploads
- Cloud resource permissions and credential management
- Integration between a local application and a cloud service

**Technical distinction:** The current performance-prediction and risk-classification models are Gradient Boosting and Random Forest models, respectively. They are machine-learning models rather than deep neural networks. The LLM and embedding-based components provide the project's language-model and retrieval-based AI functionality.

---

## 🔮 Future Enhancements

Potential future improvements include:

- Visual performance trends and historical comparisons.
- More comprehensive study-plan personalization.
- Additional evaluation of model performance and prediction quality.
- Improved report history and report-download workflows.
- Secure authentication and role-based access.
- Cloud deployment of the backend and frontend.
- Expanded monitoring, logging, and cloud-cost controls.

These are proposed enhancements, not claims that every feature is already implemented.

---

## 👩‍💻 Author

**Sakshi Zurale**

B.Tech — Electronics & Computer Engineering

Interested in Artificial Intelligence, Machine Learning, Software Engineering, and Cloud Computing.

- **GitHub:** [Sakshi-Zurale](https://github.com/Sakshi-Zurale)
- **Project Repository:** [EduAssist-AI](https://github.com/Sakshi-Zurale/EduAssist-AI)

---

<p align="center">
  <b>EduAssist AI — Smarter Insights. Better Learning. Connected Cloud.</b>
  <br/>
  Built as an academic project exploring AI-powered education and cloud computing.
</p>
