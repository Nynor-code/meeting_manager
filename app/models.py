from . import db
from datetime import datetime

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)  # corrigir utcnow
    status = db.Column(db.String(20), default='Scheduled')

    def __repr__(self):
        return f"<Meeting {self.id} - {self.title}>"