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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


# define routes that return appropriate HTML Templates
@app.route('/users')
def users_index():
    all_users = db.session.query(User).all()
    all_users_dicts = [user.to_dict() for user in all_users]
    return render_template('users.html', users=all_users_dicts)

@app.route('/users/<int:id>')
def user_show_by_id(id):
    user = User.query.filter(User.id == id).first().to_dict()
    return render_template('user_show.html', user=user)

@app.route('/users/<name>')
def user_show_by_name(name):
    user = User.query.filter(User.username.like(name)).first().to_dict()
    return render_template('user_show.html', user=user)

@app.route('/tweets')
def tweets_index():
    all_tweets = Tweet.query.all()
    all_tweets_dicts = [tweet.to_dict() for tweet in all_tweets]
    return render_template('tweets.html', tweets=all_tweets_dicts)

@app.route('/tweets/<int:id>')
def tweet_show_by_id(id):
    tweet = Tweet.query.filter(Tweet.id == id).first().to_dict()
    return render_template('tweet_show.html', tweet=tweet)

#BONUS
@app.route('/users/<int:user_id>/tweets')
def find_tweets_by_user_id(user_id):
    user_tweets = User.query.filter(User.id == user_id).first().to_dict()
    return render_template('tweets.html', tweets=user_tweets['tweets'])

@app.route('/users/<user_name>/tweets')
def find_tweets_by_username(user_name):
    user_tweets = User.query.filter(User.username == user_name.lower().title()).first().to_dict()
    return render_template('tweets.html', tweets=user_tweets['tweets'])

@app.route('/tweets/<int:tweet_id>/user')
def find_user_by_tweet(tweet_id):
    tweet = Tweet.query.filter(Tweet.id == tweet_id).first().to_dict()
    user = User.query.filter(User.id == tweet['user_id']).first().to_dict()
    return render_template('user_show.html', user=user)


if __name__ == "__main__":
    app.run()
