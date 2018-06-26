from flask import Flask, render_template, request, redirect, url_for
from flask_modus import Modus
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

DB = "postgresql://localhost/users"

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
Modus(app)
toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    messages = db.relationship(
        'Message', backref='users', lazy='dynamic', cascade="all,delete")


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    message_content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


message_tag_table = db.Table(
    'message_tags',
    db.Column('message_id', db.Integer, db.ForeignKey('messages.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.Text, unique=True)
    messages = db.relationship(
        'Message',
        secondary=message_tag_table,
        cascade="all,delete",
        lazy='dynamic',
        backref=db.backref('tags', lazy='dynamic'))


# create tables as needed
db.create_all()

# Routing for USERS


@app.route('/users', methods=['GET'])
def index():
    user_list = User.query.all()
    return render_template('index.html', user_list=user_list)


@app.route('/users/new', methods=['GET'])
def add_user():
    return render_template('new.html')


@app.route('/users', methods=['POST'])
def create():
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>', methods=['GET'])
def show(user_id):
    user = User.query.get(user_id)
    return render_template('show.html', user=user)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def destroy(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/edit', methods=['GET'])
def edit(user_id):
    found_user = User.query.get(user_id)
    return render_template('edit.html', user=found_user)


@app.route('/users/<int:user_id>', methods=['PATCH'])
def update(user_id):
    found_user = User.query.get(user_id)
    found_user.first_name = request.form['first_name']
    found_user.last_name = request.form['last_name']
    db.session.add(found_user)
    db.session.commit()
    return redirect(url_for('index'))


# Routing for MESSAGES


@app.route('/users/<int:user_id>/messages', methods=["GET"])
def message_index(user_id):
    found_user = User.query.get(user_id)
    return render_template('message_index.html', user=found_user)


@app.route('/users/<int:user_id>/messages/new', methods=["GET"])
def messages_new(user_id):
    tag_list = Tag.query.all()
    found_user = User.query.get(user_id)
    return render_template(
        'message_new.html', user=found_user, tag_list=tag_list)


@app.route('/users/<int:user_id>/messages', methods=['POST'])
def messages_create(user_id):
    message_content = request.form['message_content']
    new_msg = Message(message_content=message_content, user_id=user_id)
    tag_ids = request.form.getlist('tags')
    new_tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_msg.tags = new_tags
    db.session.add(new_msg)
    db.session.commit()

    return redirect(url_for('message_index', user_id=user_id))


@app.route('/messages/<int:msg_id>', methods=["GET"])
def messages_show(msg_id):
    found_message = Message.query.get_or_404(msg_id)
    user_id = found_message.user_id
    return render_template(
        'message_show.html', message=found_message, user_id=user_id)


@app.route('/users/<int:msg_id>/messages', methods=['DELETE'])
def destroy_message(msg_id):
    found_msg = Message.query.get(msg_id)
    user_id = found_msg.user_id
    db.session.delete(found_msg)
    db.session.commit()
    return redirect(url_for('message_index', user_id=user_id))


@app.route('/user/<int:msg_id>/messages/edit', methods=['GET'])
def messages_edit(msg_id):
    found_msg = Message.query.get(msg_id)
    tag_list = Tag.query.all()
    return render_template(
        'message_edit.html', msg=found_msg, tag_list=tag_list)


@app.route('/user/<int:msg_id>/messages', methods=['PATCH'])
def messages_update(msg_id):
    found_msg = Message.query.get(msg_id)
    found_msg.message_content = request.form['message_content']
    tag_ids = request.form.getlist('tags')
    new_tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    found_msg.tags = new_tags
    db.session.add(found_msg)
    db.session.commit()
    return redirect(url_for('message_index', user_id=found_msg.user_id))


# ROUTING FOR TAGS


@app.route('/tags', methods=['GET'])
def tag_index():
    tag_list = Tag.query.all()
    return render_template('tag_index.html', tag_list=tag_list)


@app.route('/tags/new', methods=['GET'])
def tag_new():
    return render_template('tag_new.html')


@app.route('/tags', methods=['POST'])
def tag_create():
    tag_name = request.form['tag_name']
    new_tag = Tag(tag_name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(url_for('tag_index'))


@app.route('/tags/<int:tag_id>', methods=['GET'])
def tag_show(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tag_show.html', tag=tag)


@app.route('/tags/<int:tag_id>', methods=['DELETE'])
def tag_destroy(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tag_index'))


@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def tags_edit(tag_id):
    found_tag = Tag.query.get(tag_id)
    return render_template('tags_edit.html', tag=found_tag)


@app.route('/tags/<int:tag_id>', methods=['PATCH'])
def tags_update(tag_id):
    found_tag = Tag.query.get(tag_id)
    found_tag.tag_name = request.form['tag_name']
    db.session.add(found_tag)
    db.session.commit()
    return redirect(url_for('tag_index'))
