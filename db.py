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
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

import os, psycopg2, string, random, hashlib

def get_salt():
    charset = string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, "utf-8")
    b_salt = bytes(salt, "utf-8")
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
    sql = 'SELECT hashed_password, salt FROM accounts WHERE email = %s'
    flg = False
    connection = None
    cursor = None
    
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
        flg = False  
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    return flg


def get_subjects():
    sql = "SELECT s.subject_id, s.name AS subject_name, t.name AS teacher_name, array_agg(sd.position ORDER BY sd.position) AS subject_positions FROM subject s JOIN subject_days sd ON s.subject_id = sd.subject_id LEFT JOIN teachers t ON s.teacher_id = t.teacher_id GROUP BY s.subject_id, s.name, t.name ORDER BY s.subject_id;"
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(sql,)
    
    result = cursor.fetchall()
    
    return result