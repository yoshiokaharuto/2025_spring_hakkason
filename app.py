from flask import Flask, render_template, request, url_for, redirect, session
import db, string, random, re
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
    confirm_password = request.form.get('confirm_password')
    grade = request.form.get('year')
    department_id = request.form.get('department')
    
    # バリデーションチェック
    error = None
    if not name or not email or not password or not grade or not department_id:
        error = "すべての項目を入力してください。"
    elif len(name) > 50:
        error = "名前は50文字以内で入力してください。"
    elif '@' not in email or '.' not in email:
        error = "有効なメールアドレスを入力してください。"
    elif password != confirm_password:
        error = "パスワードが確認用と一致しません。"
    elif len(password) < 6:
        error = "パスワードは6文字以上で入力してください。"
    elif not re.search(r'[A-Za-z]', password):
        error = "パスワードには少なくとも1つの英字が必要です。"
    elif not re.search(r'[0-9]', password):
        error = "パスワードには少なくとも1つの数字が必要です。"

    if error:
        return render_template('register.html', error=error, name=name, email=email)

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

    # バリデーションチェック
    error = None
    if not email or not password:
        error = "メールアドレスとパスワードを入力してください。"
    elif '@' not in email or '.' not in email:
        error = "メールアドレスの形式が正しくありません。"

    if error:
        return render_template('login.html', error=error)

    if db.login(email, password):
        account = db.select_user(email)
        session['user'] = True
        session['user_id'] = account[0]
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)

        return redirect(url_for('main'))
    else:
        error = 'メールアドレスまたはパスワードが違います。'
        return render_template('login.html', error=error)
    
@app.route('/main', methods=['GET','POST'])
def main():
    if 'user' in session:
        todos = db.get_todos(session['user_id'])
        timetable = db.get_timetable(session['user_id'])
        
        timetable_map = {}
        for subject_id, name, position in timetable:
            timetable_map[position] = {
                "subject_id": subject_id,
                "name": name
            }
        
        subject_order = ['情報システム概論', 'システム開発演習', 'システム開発実践', 'キャリアデザイン']
        my_credit_data = db.my_credit_data(session['user_id'])
        my_dict = dict(my_credit_data)
        my_data = [my_dict.get(subject, 0) for subject in subject_order]
        
        return render_template('main.html', todos=todos,timetable_map=timetable_map, my_data=my_data)
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
        return redirect(url_for('syllabus.syllabus_detail'))
    else:
        return render_template('review.html')


@app.route('/absence_form')
def absence_form():
    
    user_id = session.get('user_id')
    id = request.args.get('id')
    session['absence_id'] = id
    result = db.syllabus_detail(id)
    
    timetable_id = db.get_timetable_id(id,user_id)
    
    attendance = db.attendance(timetable_id)
    session['subject_name'] = result[1]
    print(result)
    
    return render_template('absence.html',result=result,attendance=attendance)

@app.route('/absence_exe', methods=['POST'])
def absence_exe():
    absent_date = request.form.get('absent_date')
    
    session['absent_date'] = absent_date
    name = session['subject_name']

    return render_template('absenceconfirm.html', absent_date = absent_date, name=name)    

@app.route('/absence_registration', methods=['GET','POST'])
def absence_registration():
    absent_date = session.get('absent_date')
    subject_id = session.get('absence_id')
    account_id = session.get('user_id')
    
    timetable_id = db.get_timetable_id(subject_id, account_id)
    print(timetable_id)
    count = db.absence(absent_date,timetable_id)
    if count == 1:
        session.pop('subject_name', None)
        session.pop('absent_date', None)
        return redirect(url_for('main'))
    else:
        return render_template('absenceconfirm.html')



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
        timetable = db.get_timetable(session['user_id'])
        timetable_map = {position: subject_name for subject_name, position in timetable}
        return render_template('main.html', error=error_message, todos=todos, timetable_map=timetable_map)



if __name__ == '__main__':
    app.run(debug=True)


