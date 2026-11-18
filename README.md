# ClaimWise – Insurance Claims Processing Demo

A beginner-friendly Flask application with HTML, CSS, JavaScript, and SQLite.

## 1. Requirements

- Python 3.10 or newer
- pip

## 2. Run locally (Windows)

Open Command Prompt or the VS Code terminal in this project folder.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

On macOS/Linux, activate the virtual environment with:

```bash
source venv/bin/activate
```

## 3. Run with Docker

Build the image from the project root:

```bash
docker build -t insurance-claims-app .
```

Run the container:

```bash
docker run -d --name insurance-claims-container -p 5000:5000 insurance-claims-app
```

Open http://localhost:5000.

To stop the container:

```bash
docker stop insurance-claims-container
```

To remove it:

```bash
docker rm insurance-claims-container
```

The SQLite database is created inside the container. For data to survive container removal,
add a persistent Docker volume before using this beyond a classroom demonstration.

## 4. Example decision rules

- Inactive policy → Rejected
- Claim amount above ₹100,000 → Escalated for manual review
- Three or more previous claims for the same email → Escalated
- Otherwise → Approved

These are demonstration rules only. They are not real insurance policy rules or a trained AI model.

## 5. Important limitations

This is a classroom prototype. It does not authenticate users, verify policy details with an insurer,
upload supporting documents, detect fraud, or connect to a real AI model. Do not enter real
customer personal or financial information. Before real deployment, add authentication,
authorization, secure configuration, audit logging, validation, database backups, and human review.
