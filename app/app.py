from flask import (Flask,
                   request,
                   jsonify,
                   render_template,
                   send_file,
                   request,
                   Response
                   )
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email.mime.text import MIMEText
from weasyprint import HTML
from io import BytesIO

import os
import smtplib    # for sending emails
# autentication
from functools import wraps

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@meetingdb.cj20m40eazwi.eu-north-1.rds.amazonaws.com/meetings')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Authentication
USERNAME = os.getenv("APP_USER", "admin")
PASSWORD = os.getenv("APP_PASS", "admin")

# Models
class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    datetime = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='In preparation')

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))
    subject = db.Column(db.String(200))
    owner = db.Column(db.String(100))
    expected_duration = db.Column(db.Integer)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    responsible = db.Column(db.String(100))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='open')

class Decision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    responsible = db.Column(db.String(100))

class Risk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    responsible = db.Column(db.String(100))
    status = db.Column(db.String(20), default='open')
    decision = db.Column(db.String(20))  # accept, mitigate, solve, ignore


# Email utility
def send_email(subject, body, recipients):
    sender = os.getenv("EMAIL_SENDER", "noreply@example.com")
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    with smtplib.SMTP('localhost') as server:
        server.sendmail(sender, recipients, msg.as_string())

# Routes
@app.route('/')
def index():
    meetings = Meeting.query.all()
    return render_template('index.html', meetings=meetings)


@app.route('/meetings', methods=['POST'])
def create_meeting():
    data = request.json
    meeting = Meeting(title=data['title'], datetime=datetime.fromisoformat(data['datetime']))
    db.session.add(meeting)
    db.session.commit()
    return jsonify({'id': meeting.id})


@app.route('/meetings/<int:meeting_id>/status', methods=['PATCH'])
def update_meeting_status(meeting_id):
    status = request.json.get('status')
    meeting = Meeting.query.get_or_404(meeting_id)
    meeting.status = status
    db.session.commit()
    return jsonify({'status': status})


@app.route('/meetings/<int:meeting_id>/invite', methods=['POST'])
def invite_participants(meeting_id):
    participants = request.json['participants']  # List of {name, email}
    for p in participants:
        db.session.add(Participant(name=p['name'], email=p['email'], meeting_id=meeting_id))
    db.session.commit()
    emails = [p['email'] for p in participants]
    send_email("Meeting Invitation", f"You are invited to meeting #{meeting_id}.", emails)
    return jsonify({'status': 'sent'})


@app.route('/meetings/<int:meeting_id>/report')
def html_report(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    actions = Action.query.filter_by(meeting_id=meeting_id).all()
    decisions = Decision.query.filter_by(meeting_id=meeting_id).all()
    risks = Risk.query.filter_by(meeting_id=meeting_id).all()
    return render_template('report.html', meeting=meeting, actions=actions, decisions=decisions, risks=risks)


@app.route('/meetings/<int:meeting_id>/report.pdf')
def pdf_report(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    actions = Action.query.filter_by(meeting_id=meeting_id).all()
    decisions = Decision.query.filter_by(meeting_id=meeting_id).all()
    risks = Risk.query.filter_by(meeting_id=meeting_id).all()
    html = render_template('report.html', meeting=meeting, actions=actions, decisions=decisions, risks=risks)
    pdf = HTML(string=html).write_pdf()
    return send_file(BytesIO(pdf), download_name=f'meeting_{meeting_id}_report.pdf', as_attachment=True)


@app.route('/actions/<int:action_id>', methods=['PATCH'])
def update_action(action_id):
    action = Action.query.get_or_404(action_id)
    data = request.json
    action.status = data.get('status', action.status)
    db.session.commit()
    return jsonify({'status': action.status})


@app.route('/risks/<int:risk_id>', methods=['PATCH'])
def update_risk(risk_id):
    risk = Risk.query.get_or_404(risk_id)
    data = request.json
    risk.status = data.get('status', risk.status)
    risk.decision = data.get('decision', risk.decision)
    db.session.commit()
    return jsonify({'status': risk.status, 'decision': risk.decision})


# Authentication
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Example use: apply @requires_auth to any route
# @app.route('/meetings')
# @requires_auth
# def list_meetings():
#     ...


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')
