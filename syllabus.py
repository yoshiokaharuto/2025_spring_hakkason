from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db,json

syllabus_bp = Blueprint('syllabus',__name__)

@syllabus_bp.route('/syllabus_detail',methods=['GET'])
def syllabus_detail():
    
    id = request.args.get('id')
    detail_data = db.syllabus_detail(id)
    
    return render_template('sllabusconfirm.html',detail_data=detail_data)