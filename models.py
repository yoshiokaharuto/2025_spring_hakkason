from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_years = db.Column(db.Integer)


class RegulationSubject(db.Model):
    __tablename__ = 'regulation_subject'
    regulation_subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Account(db.Model):
    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    salt = db.Column(db.Text, nullable=False)
    grade = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=True)
    display_flag = db.Column(db.Boolean, default=True)
    promote_flag = db.Column(db.Boolean, default=False)

    department = db.relationship('Department', backref='accounts')


class Subject(db.Model):
    __tablename__ = 'subject'
    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    regulation_subject_id = db.Column(db.Integer, db.ForeignKey('regulation_subject.regulation_subject_id'), nullable=True)
    semester = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=True)
    recommended_grade = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)

    regulation_subject = db.relationship('RegulationSubject', backref='subjects')
    teacher = db.relationship('Teacher', backref='subjects')
    category = db.relationship('Category', backref='subjects')


class SubjectTeacher(db.Model):
    __tablename__ = 'subject_teacher'
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id', ondelete="CASCADE"), primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id', ondelete="CASCADE"), primary_key=True)


class Timetable(db.Model):
    __tablename__ = 'timetable'
    timetable_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id', ondelete="CASCADE"))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id', ondelete="CASCADE"))

    account = db.relationship('Account', backref='timetables')
    subject = db.relationship('Subject', backref='timetables')


class SubjectDay(db.Model):
    __tablename__ = 'subject_days'
    subject_day_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id', ondelete="CASCADE"))
    position = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.CheckConstraint('position BETWEEN 1 AND 20', name='check_position'),
    )


class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id', ondelete="CASCADE"))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id', ondelete="CASCADE"))
    content = db.Column(db.Text)
    difficulty = db.Column(db.Integer)
    assignment = db.Column(db.Integer)
    interest = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    other = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (
        db.CheckConstraint('difficulty BETWEEN 1 AND 5', name='check_difficulty'),
        db.CheckConstraint('assignment BETWEEN 1 AND 5', name='check_assignment'),
        db.CheckConstraint('interest BETWEEN 1 AND 5', name='check_interest'),
        db.CheckConstraint('speed BETWEEN 1 AND 5', name='check_speed'),
        db.CheckConstraint('other BETWEEN 1 AND 5', name='check_other'),
    )


class Attendance(db.Model):
    __tablename__ = 'attendances'
    attendance_id = db.Column(db.Integer, primary_key=True)
    timetable_id = db.Column(db.Integer, db.ForeignKey('timetable.timetable_id', ondelete="CASCADE"))
    absent_date = db.Column(db.Date, nullable=False)


class Todo(db.Model):
    __tablename__ = 'todos'
    todo_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id', ondelete="CASCADE"))
    content = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.Date, nullable=False)


class PreviousAttendance(db.Model):
    __tablename__ = 'previous_attendance'
    previous_attendance_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id', ondelete="CASCADE"))
    grade = db.Column(db.Integer, nullable=False)
    student_count = db.Column(db.Integer, nullable=False)


class RequiredUnit(db.Model):
    __tablename__ = 'required_units'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    grade = db.Column(db.Integer)
    subject_id = db.Column(db.Integer, db.ForeignKey('regulation_subject.regulation_subject_id'))
    required_units = db.Column(db.Integer)