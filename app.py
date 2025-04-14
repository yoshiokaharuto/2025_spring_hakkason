from flask import Flask, render_template, request, url_for, redirect, session
import db, string, random
from timetable import timetable_bp
from datetime import timedelta


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

app.register_blueprint(timetable_bp)


@app.route('/', methods = ['GET'])
def index():
    return render_template('login.html')

@app.route('/register')
def register_form():
    return render_template('register.html')


@app.route('/register_exe', methods=['POST'])
def register_exe():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    grade = request.form.get('year')
    department_id = request.form.get('department')

    session['name'] = name
    session['email'] = email
    session['password'] = password
    session['grade'] = grade
    session['department_id'] = department_id

    return render_template('registerconfirm.html',
                           name=name, email=email, password=password, grade=grade, department_id=department_id)

    
@app.route('/register_complete', methods=['POST'])
def register_complete():
    name = session.get('name')
    email = session.get('email')
    password = session.get('password')
    grade = session.get('grade')
    department_id = session.get('department_id')

    count = db.insert_user(name, email, password, grade, department_id)

    if count == 1:
        msg = '登録が完了しました。'
        session.clear() 
        return redirect(url_for('index'))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)



@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    
    if db.login(email, password):
        account = db.select_user(email)
        session['user'] = True
        session['user_id'] = account[0]
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        
        return redirect(url_for('main'))
    else :
        error = 'メールアドレスまたはパスワードが違います。'
        return render_template('login.html', error=error)
    
@app.route('/main', methods=['GET'])
def main():
    if 'user' in session:
        return render_template('main.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/syllabus', methods=['GET'])
def syllabus():
    subjects = db.syllabus()
    return render_template('syllabus.html', subjects=subjects)

@app.route('/serch', methods=['GET'])
def serch():
    semester_name = request.args.get('semester_name', '')
    subject_name = request.args.get('subject_name', '')
    subjects = db.search(semester_name, subject_name)
    return render_template('syllabus.html', subjects=subjects)

@app.route('/')
def review_form():
    return render_template('review.html')

@app.route('/review', methods=['POST'])
def create_review():
    content = request.form.get('content')
    difficulty = request.form.get('difficulty')
    assignment = request.form.get('assignment')
    interest = request.form.get('interest')
    speed = request.form.get('speed')
    other = request.form.get('other')

    count = db.review(content, difficulty, assignment, interest, speed, other)

    if count == 1:
        session.clear() 
        return render_template('main.html')
    else:
        return render_template('review.html')


if __name__ == '__main__':
    app.run(debug=True)
