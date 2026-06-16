# Python & Streamlit Backend-Frontend Boilerplate

A modern, highly-polished boilerplate codebase displaying a clean separation between the frontend/presentation layer (Streamlit) and the backend service layer (Python logic).

## Project Structure

```text
.
├── app.py                # Frontend presentation layer
├── requirements.txt      # Python dependencies
├── README.md             # Project instruction
└── backend/
    ├── __init__.py       # Package marker
    └── main.py           # Backend business logic and simulation
```

## Getting Started

Follow these steps to run the application locally:

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.
