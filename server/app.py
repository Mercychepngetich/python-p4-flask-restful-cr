#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
   def get(self):
       newsletter_list=[]
       newsletters = Newsletter.query.all()
       for newsletter in newsletters:
           newsletterObj={
               "id":newsletter.id,
               "title":newsletter.title,
               "body":newsletter.body,
               "published_at":newsletter.published_at,
               "edited_at":newsletter.edited_at

           }
           newsletter_list.append(newsletterObj)
       return jsonify(newsletter_list)
   
   def post(self):
       new_newsletter = Newsletter(
           title = request.form['title'],
           body = request.form['body']
       )

       db.session.add(new_newsletter)
       db.session.commit()
       response_dict = new_newsletter.to_dict()
       response_body = {
          'Message': "Newslettter created successfully",
          'status':201, 
          'dict': response_dict
       }
       response = make_response(response_body,200)
       return response
       
api.add_resource(Home, '/newsletters') 

class NewsletterByID(Resource):
    def get(self,id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        newsletter_dict = newsletter.to_dict()

        response_body ={
            "dict":newsletter_dict,
            "status":200
        }

        response = make_response(
            response_body,
            200
        )
        return response

        
api.add_resource(NewsletterByID, '/newsletters/<int:id>')
    
   


if __name__ == '__main__':
    app.run(port=5555, debug=True)
