from flask import Flask, render_template, request, session
import db,  string, random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

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
        return render_template('login.html', msg=msg)
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)


if __name__=="__main__":
    app.run(debug=True)