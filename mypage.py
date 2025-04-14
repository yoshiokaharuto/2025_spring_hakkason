from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db,json

mypage_bp = Blueprint('mypage', __name__)


@mypage_bp.route('/mypage', methods=['GET'])
def mypage():
    
    account_id = session.get('user_id')
    account_data = db.get_account_data(account_id)
    subject_data = db.subject_data(account_id)
    credit_data = db.credit_data(account_id)
    my_credit_data = db.my_credit_data(account_id)
    
    keys = ['subject_name', 'credit','attendance']
    dict_subject = [dict(zip(keys, row)) for row in subject_data]
    
    units_list = [item[1] for item in credit_data]
    
    subject_order = ['情報システム概論', 'システム開発演習', 'システム開発実践', 'キャリアデザイン']
    my_dict = dict(my_credit_data)
    my_data = [my_dict.get(subject, 0) for subject in subject_order]
    
    return render_template('mypage.html', account_data=account_data, dict_subject=dict_subject, credit_data=units_list,my_data = my_data)