from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db


timetable = Blueprint('timetable', __name__)

@timetable.route('/course_register')
def course_register():
    
    subject_list = db.get_subjects()
    
    return render_template('course_register.html' , subject_list=subject_list)
