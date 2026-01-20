from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==============================
# MODELS
# ==============================

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject_expert = db.Column(db.String(100))
    courses = db.relationship('Course', backref='teacher', lazy=True)

    def __repr__(self):
        return f'<Teacher {self.name}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    students = db.relationship('Student', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.name}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

# ==============================
# ROUTES
# ==============================

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course_id = request.form['course_id']

        new_student = Student(name=name, email=email, course_id=course_id)
        db.session.add(new_student)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('add.html', courses=courses)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.course_id = request.form['course_id']
        db.session.commit()
        flash('Student updated!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('edit.html', student=student, courses=courses)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted!', 'danger')
    return redirect(url_for('index'))

@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    teachers = Teacher.query.all()  # Get all teachers for the dropdown

    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        teacher_id = request.form['teacher_id']  # Make sure the form has this field

        new_course = Course(name=name, description=description, teacher_id=teacher_id)
        db.session.add(new_course)
        db.session.commit()

        flash('Course added!', 'success')
        return redirect(url_for('courses'))

    return render_template('add_course.html', teachers=teachers)


@app.route('/teachers')
def teachers():
    all_teachers = Teacher.query.all()
    return render_template('teacher.html', teachers=all_teachers)

@app.route('/add-teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject_expert']

        new_teacher = Teacher(name=name, subject_expert=subject)
        db.session.add(new_teacher)
        db.session.commit()

        flash('Teacher added successfully!', 'success')
        return redirect(url_for('teachers'))

    return render_template('add_teacher.html')

@app.route('/edit-teacher/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    if request.method == 'POST':
        teacher.name = request.form['name']
        teacher.subject_expert = request.form['subject_expert']
        db.session.commit()
        flash('Teacher updated successfully!', 'success')
        return redirect(url_for('teachers'))

    return render_template('edit_teacher.html', teacher=teacher)

@app.route('/delete-teacher/<int:id>')
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    # Delete all courses of this teacher first
    for course in teacher.courses:
        db.session.delete(course)
    db.session.delete(teacher)
    db.session.commit()
    flash('Teacher and their courses deleted!', 'danger')
    return redirect(url_for('teachers'))

# ==============================
# INIT DB & SAMPLE DATA
# ==============================

def init_db():
    with app.app_context():
        db.create_all()

        # Add sample teachers if empty
        if Teacher.query.count() == 0:
            t1 = Teacher(name="Mr. Sharma", subject_expert="Python")
            t2 = Teacher(name="Ms. Patil", subject_expert="Web Dev")
            db.session.add_all([t1, t2])
            db.session.commit()

        # Add sample courses if empty
        if Course.query.count() == 0:
            sample_courses = [
                Course(name='Python Basics', description='Learn Python', teacher_id=1),
                Course(name='Web Development', description='HTML, CSS, Flask', teacher_id=2),
                Course(name='Data Science', description='Data analysis with Python'),
            ]
            db.session.add_all(sample_courses)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
