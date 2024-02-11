from flask import Blueprint, flash, render_template, request, jsonify #bunch of urls to support our files
from flask_login import login_required, current_user
from . import db 
from .models import Note, User
import json

views = Blueprint('views', __name__) #defining the variable

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/', methods=['GET'])
@login_required
def view_notes():
    all_notes = Note.query.join(User).filter(User.id != current_user.id).all()
    return render_template('dashboard.html', notes=all_notes, user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})







