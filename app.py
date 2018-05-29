# import Flask and jsonify from flask
# import SQLAlchemy from flask_sqlalchemy
import requests
from flask import Flask, render_template, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy

# initialize new flask app
app = Flask(__name__)
# add configurations and database
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# connect flask_sqlalchemy to the configured flask app
db = SQLAlchemy(app)

# create models for application
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    tweets = db.relationship('Tweet', backref='users', lazy=True)
    def to_dict(self):
        user = {'id': self.id, 'username': self.username, 'tweets': [tweet.to_dict() for tweet in self.tweets]}
        return user

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates="tweets")
    def to_dict(self):
        tweet = {'id': self.id, 'text': self.text, 'user_id': self.user.id, 'user': self.user.username}
        return tweet

# define routes and their respective functions that return the correct data
@app.route('/api/users')
def user_index():
    all_users = db.session.query(User).all()
    all_users_dicts = [user.to_dict() for user in all_users]
    return jsonify(all_users_dicts)

@app.route('/api/users/<int:id>')
def find_user(id):
    user = User.query.filter(User.id == id).first()
    return jsonify(user.to_dict())


@app.route('/api/users/<name>')
def find_user_by_name(name):
    user = User.query.filter(User.username.like(name)).first()
    return jsonify(user.to_dict())

@app.route('/api/tweets')
def tweet_index():
    all_tweets = Tweet.query.all()
    all_tweets_dicts = [tweet.to_dict() for tweet in all_tweets]
    return jsonify(all_tweets_dicts)

@app.route('/api/tweets/<int:id>')
def find_tweet(id):
    return jsonify(Tweet.query.filter(Tweet.id == id).first().to_dict())

@app.route('/api/users/<int:user_id>/tweets')
def find_users_tweets(user_id):
    return jsonify(User.query.filter(User.id == user_id).first().to_dict())

@app.route('/api/users/<user_name>/tweets')
def find_users_tweets_by_user_name(user_name):
    return jsonify(User.query.filter(User.name == user_name.lower().title()).first().tweets())

@app.route('/api/tweets/<int:tweet_id>/user')
def find_tweets_user(tweet_id):
    return jsonify(Tweet.query.filter(Tweet.id == tweet_id).first().user.to_dict())


# define routes that return appropriate HTML Templates
@app.route('/users')
def users_index():
    users = requests.get('http://localhost:5000/api/users').json()
    return render_template('users.html', users=users)

@app.route('/users/<int:id>')
def user_show_by_id(id):
    user = requests.get('http://localhost:5000/api/users/' + str(id))
    json = user.json()
    return render_template('user_show.html', user=json)

@app.route('/users/<name>')
def user_show_by_name(name):
    user = requests.get('http://localhost:5000/api/users/' + name)
    json = user.json()
    return render_template('user_show.html', user=json)

@app.route('/tweets')
def tweets_index():
    tweets = requests.get('http://localhost:5000/api/tweets').json()
    return render_template('tweets.html', tweets=tweets)

@app.route('/tweets/<int:id>')
def tweet_show_by_id(id):
    tweet = requests.get('http://localhost:5000/api/tweets/' + str(id))
    json = tweet.json()
    return render_template('tweet_show.html', tweet=json)

#BONUS
@app.route('/users/<int:user_id>/tweets')
def find_tweets_by_user_id(user_id):
    user = requests.get('http://localhost:5000/api/users/' + str(user_id))
    user_json = user.json()
    return render_template('tweets.html', tweets=user_json['tweets'])

@app.route('/users/<user_name>/tweets')
def find_tweets_by_username(user_name):
    user = requests.get('http://localhost:5000/api/users/' + user_name)
    user_json = user.json()
    return render_template('tweets.html', tweets=user_json['tweets'])

@app.route('/tweets/<int:tweet_id>/user')
def find_user_by_tweet(tweet_id):
    tweet = requests.get('http://localhost:5000/api/tweets/' + str(tweet_id))
    tweet_json = tweet.json()
    user = requests.get('http://localhost:5000/api/users/' + tweet_json['user'])
    user_json = user.json()
    return render_template('user_show.html', user=user_json)


if __name__ == "__main__":
    app.run()
