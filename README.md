# Meeting Management System

A Python Flask-based Meeting Management API that supports scheduling, invitations, topic planning, outcomes tracking (actions, decisions, risks), reporting (HTML/PDF), and secure access. Runs with PostgreSQL using Docker and deployable to AWS EC2.

## Features

- 📅 Schedule and manage meetings with participants, topics, and expected durations
- 📧 Email invitations to participants
- 📝 Record meeting outcomes: notes, actions, decisions, and risks
- 📈 Track status of actions (open, running, closed) and risks (with resolution strategy)
- 🧾 Generate HTML and PDF reports
- 🔐 Basic authentication for protected endpoints
- 🐳 Dockerized for easy deployment with PostgreSQL

---

## Technologies Used

- Python 3
- Flask
- SQLAlchemy
- PostgreSQL
- WeasyPrint (for PDF generation)
- Docker + Docker Compose
- SMTP (email sending)

---

## Getting Started

### Prerequisites
- Docker & Docker Compose installed
- Local SMTP service or SMTP credentials for email sending

### Setup

1. Clone the repository
2. Create a `.env` file with the following:

```env
DATABASE_URL=postgresql://user:password@db:5432/meetings
EMAIL_SENDER=noreply@example.com
APP_USER=admin
APP_PASS=admin
```

3. Start the application:

```bash
docker-compose up --build
```

4. Load sample data:

```bash
docker exec -it meeting-api python sample_data.py
```

---

## API Endpoints (example)

- `POST /meetings`: Create a meeting
- `PATCH /meetings/<id>/status`: Update meeting status
- `POST /meetings/<id>/invite`: Invite participants
- `GET /meetings/<id>/report`: View HTML report
- `GET /meetings/<id>/report.pdf`: Download PDF report
- `PATCH /actions/<id>`: Update action status
- `PATCH /risks/<id>`: Update risk status and resolution

Use Basic Auth with `APP_USER` and `APP_PASS` for protected routes.

---

## Deployment on AWS EC2

1. Launch an EC2 instance (Ubuntu recommended)
2. Install Docker & Docker Compose
3. Clone the repo and configure `.env`
4. Run `docker-compose up -d`
5. Open ports 80 or 5000 in security group

---

## To-Do / Roadmap

- Frontend interface with Streamlit or HTML templates
- User login and token-based auth
- Email provider integration (e.g., SMTP2GO, Mailgun)
- CI/CD pipeline

---

## License
MIT License








✅ Tech Stack
Backend: Python + Flask (API)
Database: PostgreSQL (freeware, supports SQL training well)
ORM: SQLAlchemy (for easier DB interaction and raw SQL when needed)
Email: smtplib or Flask-Mail
Cloud: AWS EC2 (Ubuntu-based instance)
Optional UI: Streamlit or simple HTML (for local interface if needed)

🧱 Core Modules & Features
1. Meeting Scheduler
Create/Update meeting:
Title, date/time, status (In Preparation, Scheduled, Running, Closed)
List of topics: subject, presenter (from participants), expected duration
REST API: POST /meeting, GET /meeting/<id>, PUT /meeting/<id>

2. Participant Manager
Add/search/edit participants
REST API: GET /participants, POST /participants

3. Email Invitations
On Scheduled, trigger email invites to participants
SMTP or Flask-Mail integration
REST API: POST /meeting/<id>/send-invites

4. Meeting Runtime Operations
Collect:
Notes, Actions, Decisions, Risks
Assign to person + target date
API: POST /meeting/<id>/notes, /actions, /decisions, /risks

5. Actions and Risk Management
View/update status (Open, Running, Closed)
Risk decisions: Accept, Mitigate, Solve, Ignore
API: GET /actions, PUT /actions/<id>, same for risks

6. Meeting Reports
Generate and send report via email at meeting end
Include all notes, actions, decisions, risks
API: POST /meeting/<id>/close-and-report

7. Dashboard Reports
* View meetings and filter:
* By status
* By outcome type (Actions, Decisions, Risks)
* API: GET /report/meeting/<id>, GET /report/actions, ...

📊 Database Tables (PostgreSQL schema)
meetings(id, title, datetime, status)
participants(id, name, email)
meeting_participants(meeting_id, participant_id)
topics(id, meeting_id, subject, owner_id, duration)
notes(id, meeting_id, content, owner_id, timestamp)
actions(id, meeting_id, description, status, owner_id, target_date)
decisions(id, meeting_id, description, owner_id, timestamp)
risks(id, meeting_id, description, status, decision, owner_id, target_date)

