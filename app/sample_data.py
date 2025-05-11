# sample_data.py
from app import db, Meeting, Topic, Participant, Action, Decision, Risk
from datetime import datetime, timedelta

# Clear existing data
db.drop_all()
db.create_all()

# Create a meeting
meeting = Meeting(title="Q2 Planning Meeting", datetime=datetime.now() + timedelta(days=3))
db.session.add(meeting)
db.session.commit()

# Add participants
participants = [
    Participant(name="Alice Johnson", email="alice@example.com", meeting_id=meeting.id),
    Participant(name="Bob Smith", email="bob@example.com", meeting_id=meeting.id)
]
db.session.bulk_save_objects(participants)

# Add topics
topics = [
    Topic(meeting_id=meeting.id, subject="Project Delta Update", owner="Alice Johnson", expected_duration=30),
    Topic(meeting_id=meeting.id, subject="Risk Review", owner="Bob Smith", expected_duration=20)
]
db.session.bulk_save_objects(topics)

# Add actions
actions = [
    Action(meeting_id=meeting.id, description="Update project roadmap", responsible="Alice Johnson", due_date=datetime.now() + timedelta(days=7)),
    Action(meeting_id=meeting.id, description="Prepare Q3 hiring plan", responsible="Bob Smith", due_date=datetime.now() + timedelta(days=10))
]
db.session.bulk_save_objects(actions)

# Add decisions
decisions = [
    Decision(meeting_id=meeting.id, description="Go ahead with vendor selection phase", responsible="Alice Johnson")
]
db.session.bulk_save_objects(decisions)

# Add risks
risks = [
    Risk(meeting_id=meeting.id, description="Data center dependency", responsible="Bob Smith", status="open", decision="mitigate")
]
db.session.bulk_save_objects(risks)

db.session.commit()
print("Sample data inserted.")
