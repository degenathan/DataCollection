from os import name
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField 
from datetime import datetime
import pandas as pd
import folium
from datacollectionapp import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)

#Creating the SQL database from CSV file if TRUE (Unfinished)
citycsv = pd.read_csv('city_api_list.csv', index_col=False)
citycsv = citycsv.drop(citycsv[(citycsv.Working != "Yes")].index)





class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    state = db.Column(db.String(2))
    name = db.Column(db.String(50))
    #cityurl = db.Column(db.String(1000))

    def __repr__(self):
        return '{}'.format(self.state)

def choice_query():
    return City.query

class Form(FlaskForm):
    #state = QuerySelectField(query_factory=choice_query,allow_blank=True)
    state = SelectField('state', choices=[('CA','California'),('TX',"Texas")])
    city = SelectField('city',choices=[])

@app.route('/', methods = ['POST','GET'])

def index():
    form = Form()
    form.city.choices = [(city.id, city.name) for city in City.query.filter_by(state = 'CA').all()]

    if request.method == 'POST':
        city = City.query.filter_by(id=form.city.data).first()
        #topic = City.query.filter_by(id=city.topic).first()
        m = folium.Map(location=[30.2672,-97.7431],zoom_start=14)
        m.save('templates/map.html')
        returnlist = mainprogram(city.name,form.state.data, request.form['content_topic'])
        
        return render_template('dataresults.html', form = form, city = city.name, state = form.state.data, topic = request.form['content_topic'], tables=[returnlist.to_html(classes='data', index = False, header = True, justify='center', render_links=True)], titles=returnlist.columns.values)
                                                                                                                                                    
    #tables=[returnlist.to_html(classes='data')], titles=returnlist.columns.values

    return render_template('index.html',form=form)
    
@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/city/<state>')
def city(state):
    cities = City.query.filter_by(state=state).all()
    cityArray = []
    for city in cities:
        cityObj = {}
        cityObj['id'] = city.id
        cityObj['name'] = city.name
        cityArray.append(cityObj)

    return jsonify({'cities':cityArray})



if __name__ == "__main__":
    #db.create_all()
    '''
    city1 = City(id = 1, state = "CA", name = "Los Angeles")
    city2 = City(id = 2, state = "TX", name = "Dallas")
    city3 = City(id = 3, state = "TX", name = "Austin")
    city4 = City(id = 4, state = "WA", name = "Seattle")
    city5 = City(id = 5, state = "IL",name = "Chicago")
    '''
    db.session.commit()
    #print(citycsv)
    app.run(debug = True)