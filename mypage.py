from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db,json

mypage_bp = Blueprint('mypage', __name__)


@mypage_bp.route('/mypage', methods=['GET'])
def mypage():
    
    account_id = session.get('user_id')
    account_data = db.get_account_data(account_id)
    subject_data = db.subject_data(account_id)
    
    keys = ['subject_name', 'credit','attendance']
    dict_subject = [dict(zip(keys, row)) for row in subject_data]
    
    return render_template('mypage.html', account_data=account_data, dict_subject=dict_subject)