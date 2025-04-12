from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db,json

mypage_bp = Blueprint('mypage', __name__)


@mypage_bp.route('/mypage', methods=['GET'])
def mypage():
    
    account_id = session.get('user_id')
    account_data = db.get_account_data(account_id)
    
    
    
    return render_template('mypage.html')