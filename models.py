import os, sys
sys.path.insert(0, os.path.abspath(".."))
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from uccworks  import db, login_manager,app
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User (db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(17), unique = True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)
    posts = db.relationship('Post', backref= 'author', lazy = True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)




    def __repr__(self): # how our object is printed when we print it out
        return f"User('{self.username}',{self.email})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)
    content = db.Column(db.Text ,nullable=False)
    # post can have only one user so up in User class we add(check last line)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)

    def __repr__(self):  # how our object is printed when we print it out
        return f"Post('{self.title}',{self.date_posted})"


