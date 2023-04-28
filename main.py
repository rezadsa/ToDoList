
from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)


                                       
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:reza123@localhost:5432/blog_poster'
app.config['SECRET_KEY']='\x9a_\x8ck\x90\x19x-\xa6M\x8c\xc6C\x87\x06\xfc\xdc\xa5\x93\xac\x07\x1c\x90V'

db=SQLAlchemy(app)

class Topic(db.Model):
    __tablename__='topics'

    topic_id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(length=255))

    task=db.relationship('Task',cascade='all,delete-orphan')

class Task(db.Model):
    __tablename__='tasks'

    task_id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.String(length=255))
    topic_id=db.Column(db.Integer,db.ForeignKey('topics.topic_id'))

    topic=db.relationship('Topic',backref='topic')

@app.route('/')
def display_topics():
    return render_template('home.html',topics=Topic.query.all())

@app.route('/topic/<int:topic_id>')
def display_tasks(topic_id):
   topic=Topic.query.filter_by(topic_id=topic_id).first()
   tasks=Task.query.filter_by(topic_id=topic_id)
   return render_template('topic_tasks.html',topic=topic,tasks=tasks)

@app.route('/add/topic',methods=['POST'])
def add_topic():
    if not request.form['topic-title']:
        flash('Enter a title for your new topic','red')
    else:
        topic=Topic(title=request.form['topic-title'])
        db.session.add(topic)
        db.session.commit()
        flash('Topic Added Successfully','darkgreen')

    return redirect(url_for('display_topics'))



@app.route('/add/task/<int:topic_id>',methods=['POST'])
def add_task(topic_id):
    if not request.form['task-description']:
        flash('Peasle Enter your description','red')
    else:
        task=Task(topic_id=topic_id,description=request.form['task-description'])
        db.session.add(task)
        db.session.commit()
        flash('Description Added Succesfully','darkgreen')


    return redirect(url_for('display_tasks',topic_id=topic_id))


@app.route('/delete/task/<int:task_id>',methods=['POST'])
def delete_task(task_id):
    pending_delete_task=Task.query.filter_by(task_id=task_id).first()
    target_topic_id=pending_delete_task.topic.topic_id
    db.session.delete(pending_delete_task)
    db.session.commit()
    return redirect(url_for('display_tasks',topic_id=target_topic_id))

# Deletion topic without tasks
@app.route('/delete/topic/<int:topic_id>',methods=['POST'])
def delete_topic(topic_id):
    pending_delete_topic=Topic.query.filter_by(topic_id=topic_id).first()
    db.session.delete(pending_delete_topic)
    db.session.commit()

    return redirect(url_for('display_topics'))

    # session.remove()


if __name__=='__main__':
    app.run(debug=True,host='127.0.0.1',port='3320')
