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

### 1. Install uv

If you don't have `uv` installed, install it using the official script:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies (Optional)

If you want to create a local virtual environment for IDE autocompletion, run:

```bash
uv sync
```

### 3. Run the App

You can run the application directly, and `uv` will automatically manage dependencies and virtual environments:

```bash
uv run streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.
