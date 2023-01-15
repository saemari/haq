# импорт фласка и sqlalchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avar.db'
db = SQLAlchemy()

# таблица с информацией о респонденте
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    age = db.Column(db.Integer)

# таблица с вопросами
class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

# таблица с ответами
class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q0 = db.Column(db.Integer)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)
    q9 = db.Column(db.Integer)

db.init_app(app) # соединяем базу и приложение

@app.before_first_request # создаем базу
def db_creation():
    db.create_all()

# задаём главную страницу
@app.route('/')
def index():
    return render_template('index.html')

# задаём страницу с опросником
@app.route('/questions')
def question_page():
    questions = Questions.query.all()
    return render_template(
        'questions.html',
        questions=questions)


# задаём страницу с обработкой
@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    gender = request.args.get('gender')
    age = request.args.get('age')
    user = User(
        age=age,
        gender=gender,
    )
    #вгружаем данные о пользователе
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    #обрабатываем ответы
    q0 = request.args.get('q0')
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    q6 = request.args.get('q6')
    q7 = request.args.get('q7')
    q8 = request.args.get('q8')
    q9 = request.args.get('q9')
    answer = Answers(id=user.id, q0=q0, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9)
    db.session.add(answer)
    db.session.commit()
    return 'Ok'


# задаём страницу со статистикой
@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0] #средний возраст респондентов
    all_info['total_count'] = User.query.count()  #количество прошедших
    all_info['q0_mean'] = db.session.query(func.avg(Answers.q0)).one()[0] # среднее за 1 вопрос
    all_info['q1_mean'] = db.session.query(func.avg(Answers.q1)).one()[0] # среднее за 2 вопрос
    all_info['q2_mean'] = db.session.query(func.avg(Answers.q2)).one()[0] # и так далее
    all_info['q3_mean'] = db.session.query(func.avg(Answers.q3)).one()[0]
    all_info['q4_mean'] = db.session.query(func.avg(Answers.q4)).one()[0]
    all_info['q5_mean'] = db.session.query(func.avg(Answers.q5)).one()[0]
    all_info['q6_mean'] = db.session.query(func.avg(Answers.q6)).one()[0]
    all_info['q7_mean'] = db.session.query(func.avg(Answers.q7)).one()[0]
    all_info['q8_mean'] = db.session.query(func.avg(Answers.q8)).one()[0]
    all_info['q9_mean'] = db.session.query(func.avg(Answers.q9)).one()[0]
    return render_template('results.html', all_info=all_info)


if __name__ == '__main__':
    app.run()

# я пыталась исправить internal server error ещё до прошлого дедлайна этой домашки и всё равно не смогла. однажды Хемингуэй поспорил.