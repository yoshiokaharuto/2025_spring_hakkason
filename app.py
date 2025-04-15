from flask import Flask, render_template, request, url_for, redirect, session
import db, string, random
from timetable import timetable_bp
from mypage import mypage_bp
from syllabus import syllabus_bp
from datetime import timedelta


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

app.register_blueprint(timetable_bp)
app.register_blueprint(mypage_bp)
app.register_blueprint(syllabus_bp)


@app.route('/')
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
        todos = db.get_todos(session['user_id'])
        return render_template('main.html', todos=todos)
    else:
        return redirect(url_for('login'))

    
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))



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

@app.route('/review_form')
def review_form():
    return render_template('review.html')

@app.route('/review', methods=['POST'])
def create_review():
    user_id = session['user_id']
    sub_id = session['subject_id']
    content = request.form.get('content')
    difficulty = request.form.get('difficulty')
    speed = request.form.get('speed')
    interest = request.form.get('interest')
    understanding = request.form.get('understanding')
    assignment = request.form.get('assignment')

    count = db.review(user_id,sub_id,content,difficulty,speed,interest, understanding,assignment)

    if count == 1:
        return redirect(url_for('main'))
    else:
        return render_template('review.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        deadline = request.form.get('deadline')
        todo_text = request.form.get('todo')
        account_id = session['user_id']

        if deadline and todo_text:
            db.insert_todo(deadline, todo_text, account_id)
            return redirect(url_for('main'))
        else:
            error_message = "期限とTODO内容の両方を入力してください。"
            return render_template('todo_register.html', error=error_message)
    else:
        return render_template('todo_register.html')
    
@app.route('/complete_todo', methods=['POST'])
def complete_todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    todo_ids = request.form.getlist('todo_id')  

    if todo_ids:
        for todo_id in todo_ids:
            db.delete_todo_by_id(todo_id, session['user_id'])  
        return redirect(url_for('main'))
    else:
        error_message = "削除するTODOを選択してください。"
        todos = db.get_todos(session['user_id'])
        return render_template('main.html', error=error_message, todos=todos)

if __name__ == '__main__':
    app.run(debug=True)


