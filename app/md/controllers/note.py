from webbrowser import get
from flask import jsonify,request,session
from flask_restful import Resource
from app import db
from app.auth.decorators import token_required
from app.exception import PGAPIException
from app.md.models import Note
from app.md.serde import NotesSchema

class NoteView(Resource):

    @token_required
    def get(self):
        note=Note.query.filter_by(user_id=self.id).all()
        notes=NotesSchema().dump(note,many=True)
        return notes
    
    @token_required
    def post(self):
        note = request.get_json()
        if len(note) < 1:
            raise PGAPIException({'note':'Note is too short!'})
        else:
            new_note = Note(data=note['note'],user_id = session['user_id'])
            db.session.add(new_note)
            db.session.commit()
            return NotesSchema().dump(new_note)
        
    
    @token_required
    def delete(self):
        data = request.get_json()
        Note.query.filter_by(id=data['id']).delete()

        db.session.commit()

        return jsonify({'message':'note is deleted'})
    
    @token_required
    def put(Self):
        data = request.get_json()
        Note.query.filter_by(id = data['id']).update(data,synchronize_session=False)

        db.session.commit()

        return jsonify({'message':'note is updated'})
    