#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    events = Event.query.all()
    all_events = []
    for event in events:
        event_dict = {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        all_events.append(event_dict)
    return jsonify(all_events), 200
    


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.filter_by(id=id).first()
    if event:
        sessions = event.sessions
        all_sessions = []
        for s in sessions:
            sessions_dict = {
                'id': s.id,
                'title': s.title,
                'start_time': s.start_time.isoformat()
            }
            all_sessions.append(sessions_dict)
        return jsonify(all_sessions), 200
    else:
        return jsonify({"error": "Event not found"}), 404


@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()
    all_speakers = []
    for s in speakers:
        speaker_dict = {
            'id': s.id,
            'name': s.name,
        }
        all_speakers.append(speaker_dict)
    return jsonify(all_speakers), 200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = db.session.get(Speaker, id)
    if speaker:
        bio_content = speaker.bio.bio_text if speaker.bio else "No bio available"
        speaker_dict = {
            'id': speaker.id,
            'name': speaker.name,
            'bio_text': bio_content
        }
            
        return jsonify(speaker_dict), 200
    else:
        return jsonify({"error": "Speaker not found"}), 404
            


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = db.session.get(Session, id)
    if session:
        all_speakers = []
        for s in session.speakers :
            bio_content = s.bio.bio_text if s.bio else "No bio available"
            speaker_dict= {
                'id': s.id,
                'name': s.name,
                'bio_text': bio_content
            }
            all_speakers.append(speaker_dict)
        return jsonify(all_speakers), 200
    else:
        return jsonify({"error": "Session not found"}), 404
            


if __name__ == '__main__':
    app.run(port=5555, debug=True)