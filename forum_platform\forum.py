from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.relationship('Answer', backref='question', lazy=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

@app.route('/')
def home():
    questions = Question.query.order_by(Question.timestamp.desc()).all()
    return render_template('index.html', questions=questions)

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if title and content:
            new_question = Question(title=title, content=content)
            db.session.add(new_question)
            db.session.commit()

            return redirect(url_for('home'))

    return render_template('ask.html')

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        content = request.form['content']

        if content:
            new_answer = Answer(content=content, question=question)
            db.session.add(new_answer)
            db.session.commit()

    return render_template('question.html', question=question)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
