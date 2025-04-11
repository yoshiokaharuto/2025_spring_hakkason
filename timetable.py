from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db,json


timetable_bp = Blueprint('timetable', __name__)

@timetable_bp.route('/course_register')
def course_register():
    
    subject_list = db.get_subjects()
    
    keys = ['id', 'name', 'teacher', 'schedule']
    dict_list = [dict(zip(keys, row)) for row in subject_list]
    
    print(dict_list)
    
    # json_list = json.dumps(dict_list, ensure_ascii=False)
    
    # print(json_list)

    
    return render_template('syllabusregistration.html' ,dict_list=dict_list)
