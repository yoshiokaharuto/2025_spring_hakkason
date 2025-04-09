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
    count = 0  # 正常時も count を初期化
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (name, email, hashed_password, salt, grade, department_id))
        connection.commit()
        count = cursor.rowcount  # 実際に影響を受けた行数を取得
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return count
