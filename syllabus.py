from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db,json

syllabus_bp = Blueprint('syllabus',__name__)

@syllabus_bp.route('/syllabus_detail')
def syllabus_detial():
    return render_template('sllabusconfirm.html')