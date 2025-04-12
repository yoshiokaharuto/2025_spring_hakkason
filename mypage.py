from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db,json

mypage_bp = Blueprint('mypage', __name__)


@mypage_bp.route('/mypage', methods=['GET'])
def mypage():
    
    return render_template('mypage.html')