from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db,json

syllabus_bp = Blueprint('syllabus',__name__)

@syllabus_bp.route('/syllabus_detail',methods=['GET'])
def syllabus_detail():
    
    id = request.args.get('id')
    detail_data = db.syllabus_detail(id)
    prev_data = db.previous_data(id)
    review_list = db.review_list(id)
    session['subject_id'] = detail_data[0]
    
    
    return render_template('sllabusconfirm.html',detail_data=detail_data,prev_data=prev_data,review_list=review_list)