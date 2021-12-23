import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


'''
help predict how successful a kickstarter campaign will be based
on the monetary goal, description, campaign length, or catagories.
'''

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_kickstart.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB = SQLAlchemy()
    DB.init_app(app)
    class Start_Up(DB.Model):
        id = DB.Column(DB.BigInteger, primary_key=True)
        name = DB.Column(DB.String(30), nullable=False)
        goal = DB.Column(DB.BigInteger, nullable=False)

        def __repr__(self):
            return f'ID: {self.id} | Name: {self.name} | Goal: {self.goal}'
    @app.before_first_request
    def create_tables():
        DB.create_all()
    @app.route('/')
    def root():
        return str([(b.name, b.goal) for b in Start_Up.query.all()])
    @app.route('/refresh')
    def refresh():
        DB.drop_all()
        DB.create_all()
        return 'Data has been refreshed.'
    @app.route('/add')
    def add_one():
        # have to put everything into lists or dicts and 
        # return at end else just print to terminal

        q = Start_Up.query.all()
        names = [f'biz{x}' for x in range(1,91)]
        for i, name in enumerate(names):
            biz = Start_Up(id=i, name=name, goal=i*2+1)
            if not Start_Up.query.get(biz.id):
                DB.session.add(biz)
                        
        DB.session.commit()
        return 'Names have been added'
    return app

# if __name__ =='__main__':
# create_app()


