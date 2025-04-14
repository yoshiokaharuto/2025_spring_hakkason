from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db,json


timetable_bp = Blueprint('timetable', __name__)

@timetable_bp.route('/course_register', methods=['GET'])
def course_register():
    
    subject_list = db.get_subjects()
    
    keys = ['id', 'name', 'teacher', 'schedule']
    dict_list = [dict(zip(keys, row)) for row in subject_list]
    
    return render_template('course_register.html' ,dict_list=dict_list)

@timetable_bp.route('/register_subject', methods=['POST'])
def register_subject():
    
    user_id = session.get('user_id')
    subject_data = request.form.getlist('subjects')
    
    for data in subject_data:
        success = db.register_subject(user_id,data)
        if not success:
            return redirect(url_for('timetable.course_register'))
    return redirect(url_for('main'))
