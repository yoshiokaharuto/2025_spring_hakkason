import os, psycopg2, string, random, hashlib

def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw=bytes(password, "utf-8")
    b_salt=bytes(salt, "utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password

def get_connection():
    url = os.environ.get('DATABASE_URL')
    if url is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
    connection = psycopg2.connect(url)
    return connection

def insert_user(name, email, password, grade, department_id):
    
    print(f'アカウント登録:{department_id}')
    sql = 'INSERT INTO accounts (name, email, password_hash, salt, grade, department_id) VALUES (%s, %s, %s, %s, %s, %s)'
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    count = 0  
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (name, email, hashed_password, salt, grade, department_id))
        connection.commit()
        count = cursor.rowcount  
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return count


def login(email, password):
    sql = 'SELECT password_hash, salt FROM accounts WHERE email = %s'
    flg = False  

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (email,))
        user = cursor.fetchone()

        if user:
            salt = user[1]
            hashed_password = get_hash(password, salt)

            if hashed_password == user[0]:
                flg = True  
    except psycopg2.DatabaseError as db_error:
        print(f"DBエラー: {db_error}")
        flg = False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return flg

def select_user(email):
    sql = "select account_id,name from accounts where email = %s"
    
    connection = get_connection()
    cursor = connection.cursor()
        
    cursor.execute(sql, (email,))
    result = cursor.fetchone()
    
    return result

def get_subjects():
    sql = "SELECT s.subject_id, s.name AS subject_name, t.name AS teacher_name, array_agg(sd.position ORDER BY sd.position) AS subject_positions FROM subject s JOIN subject_days sd ON s.subject_id = sd.subject_id LEFT JOIN teachers t ON s.teacher_id = t.teacher_id GROUP BY s.subject_id, s.name, t.name ORDER BY s.subject_id;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql,)
    
    result = cursor.fetchall()
    
    return result

def register_subject(user_id,subject_id):
    sql = "INSERT INTO timetable (account_id,subject_id) VALUES (%s,%s);"
    result = True
    
    print (user_id)
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_id,subject_id))
        
        connection.commit()
    except psycopg2.DatabaseError:
        result = False
    finally:
        cursor.close()
        connection.close()
    return result

def syllabus():
    sql = 'SELECT subject.subject_id,regulation_subject.name, subject.name, subject.credit, subject.semester, subject.recommended_grade FROM subject JOIN regulation_subject ON subject.regulation_subject_id = regulation_subject.regulation_subject_id'
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"エラー: {e}")
        return []
 
def search(semester_name, subject_name):
    sql = 'SELECT subject.subject_id,  regulation_subject.name, subject.name, subject.credit, subject.semester, subject.recommended_grade FROM subject JOIN regulation_subject ON subject.regulation_subject_id = regulation_subject.regulation_subject_id WHERE regulation_subject.name LIKE %s AND subject.name LIKE %s'
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(sql, ('%' + semester_name + '%', '%' + subject_name + '%'))
            return cursor.fetchall()
    except Exception as e:
        print(f"エラー: {e}")
        return []


      
def review(user_id,sub_id,content,difficulty,speed,interest, understanding,assignment):
    sql = 'INSERT INTO reviews (account_id,subject_id,content, difficulty, assignment, interest, speed, other) VALUES (%s,%s,%s, %s, %s, %s, %s, %s);'
    count = 0  
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_id,sub_id,content, difficulty, assignment, interest, speed, understanding))
        connection.commit()
        count = cursor.rowcount  
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return count

def get_account_data(account_id):
    sql = "SELECT accounts.name,accounts.grade,departments.name FROM accounts JOIN departments ON accounts.department_id = departments.department_id WHERE accounts.account_id =%s;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (account_id,))
    
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return result

def subject_data(account_id):
    sql="SELECT s.name AS subject_name, s.credit, COUNT(a.attendance_id) AS absent_count FROM subject s JOIN timetable t ON s.subject_id = t.subject_id LEFT JOIN attendances a ON t.timetable_id = a.timetable_id WHERE t.account_id = %s GROUP BY s.subject_id, s.name, s.credit;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (account_id,))
    
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result 

def credit_data(account_id):
    sql = "SELECT rs.name,ru.required_units FROM accounts a JOIN required_units ru ON a.grade = ru.grade AND a.department_id = ru.department_id JOIN regulation_subject rs ON ru.subject_id = rs.regulation_subject_id WHERE a.account_id = %s;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (account_id,))
    
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

def my_credit_data(account_id):
    sql = "SELECT rs.name AS regulation_subject_name, SUM(s.credit) AS total_credits FROM timetable t JOIN subject s ON t.subject_id = s.subject_id JOIN regulation_subject rs ON s.regulation_subject_id = rs.regulation_subject_id WHERE t.account_id = %s GROUP BY rs.name ORDER BY rs.name;"
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (account_id,))
    
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result


def absence(date, timetable_id):
    sql = 'INSERT INTO attendances (absent_date,timetable_id) VALUES (%s, %s)'
    count = 0  
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (date,timetable_id))
        connection.commit()
        count = cursor.rowcount  
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return count

def attendance(timetable_id):
    sql="SELECT absent_date FROM attendances WHERE timetable_id = %s;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (timetable_id))
    
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

def get_timetable_id(subject_id, account_id):
    sql="SELECT timetable_id FROM timetable WHERE subject_id = %s AND account_id = %s;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (subject_id,account_id))
    
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return result
    
    

    
def insert_todo(deadline, todo_text, account_id):
    sql = 'INSERT INTO todos (deadline, content, account_id) VALUES (%s, %s, %s)'
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(sql, (deadline, todo_text, account_id))
            connection.commit()
    except Exception as e:
        print(f"エラー: {e}")


def get_todos(account_id):
    sql = 'SELECT todo_id, deadline, content FROM todos WHERE account_id = %s ORDER BY deadline ASC'
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(sql, (account_id,))
            return cursor.fetchall()
    except Exception as e:
        print(f"エラー: {e}")
        return []

    
def get_user_id(email):
    sql = 'SELECT account_id FROM accounts WHERE email = %s'

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            print(f"ユーザーID取得結果: {result}")  
            if result:
                return result[0]
            else:
                return None
    except Exception as e:
        print(f"ユーザーID取得エラー: {e}")
        return None


def delete_todo_by_id(todo_id, account_id):
    sql = 'DELETE FROM todos WHERE todo_id = %s AND account_id = %s'
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(sql, (todo_id, account_id))
            connection.commit()
    except Exception as e:
        print(f"TODO削除エラー: {e}")

def syllabus_detail(id):
    sql = "SELECT subject_id,subject.name,regulation_subject.name,credit,semester,recommended_grade,teachers.name FROM subject JOIN regulation_subject ON subject.regulation_subject_id = regulation_subject.regulation_subject_id JOIN teachers ON subject.teacher_id = teachers.teacher_id where subject_id = %s;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (id,))
    
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return result

def previous_data(id):
    sql = "SELECT g.grade,COALESCE(pa.student_count, 0) AS student_count FROM generate_series(1, 4) AS g(grade) LEFT JOIN previous_attendance pa ON pa.grade = g.grade AND pa.subject_id = %s ORDER BY g.grade;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (id,))
    
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result
    
def review_list(id):
    sql="SELECT content, difficulty, assignment, interest, speed, other,created_at::date FROM reviews WHERE subject_id = %s"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (id,))
    
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

def get_timetable(id):
    sql = "SELECT s.subject_id,s.name, sd.position FROM timetable t JOIN subject_days sd ON t.subject_id = sd.subject_id JOIN subject s ON s.subject_id = t.subject_id WHERE t.account_id = %s;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql, (id,))
    
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result