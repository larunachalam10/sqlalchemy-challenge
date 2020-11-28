import pandas as pd
import numpy as np
import datetime as dt

# %matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect


engine=create_engine("sqlite:///Resources/hawaii.sqlite")
# engine=create_engine("sqlite:///Users/priya.a/Documents/UO-DAcourse/sqlalchemy-challenge/Resources")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station=Base.classes.station
Measurement=Base.classes.measurement

inspector = inspect(engine)
station1 = inspector.get_columns('station')

measurement1=inspector.get_columns('measurement')


session=Session(engine)

df=pd.read_csv("date_prcp.csv")
# print(df)
# results=df.to_dict()
# print(results)
app=Flask(__name__)

@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[star_date format:yyyy-mm-yy]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).\
            filter(Measurement.date > "2016-08-23").\
            order_by(Measurement.date).all()

    date_prcp=[]
    for date, prcp in results:
        new_dict={}
        new_dict[date]=prcp
        date_prcp.append(new_dict)

    session.close()
    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    results=session.query(Station.station,Station.name).all()
    station_list={}
    for s,name in results:
        station_list[s]=name

    session.close()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    results=session.query()
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year_date=(dt.datetime.strptime(last_date[0],"%Y-%m-%d")-dt.timedelta(days=365)).strftime('%Y-%m-%d')
    temp=session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date >= last_year_date).\
        order_by(Measurement.date).all()
    
    tobs_list=[]
    for date, tobs in temp:
        new_dict={}
        new_dict[date]=tobs
        tobs_list.append(new_dict)
    session.close()
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    
    # start_date=dt.datetime.strptime(start,"%Y-%m-%d")
    # last_year=dt.timedelta(days=365)
    # start=start_date-last_year
    
    results=session.query(Measurement.date,func.min(Measurement.tobs),\
                          func.max(Measurement.tobs),\
                          func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
   
    result_list=[]
    for date,min,avg,max in results:
        new_dict={}
        new_dict["Date"]=date
        new_dict["TMIN"]=min
        new_dict["TAVG"]=avg
        new_dict["TMAX"]=max
        result_list.append(new_dict)
    session.close()

    return jsonify(result_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    # start_date=dt.datetime.strptime(start,"%Y-%m-%d")
    # last_year=dt.timedelta(days=365)
    # start=start_date-last_year
    
    results=session.query(Measurement.date,func.min(Measurement.tobs),\
                          func.max(Measurement.tobs),\
                          func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start,Measurement.date <= end).all()
   
    result_list=[]
    for date,min,avg,max in results:
        new_dict={}
        new_dict["Date"]=date
        new_dict["TMIN"]=min
        new_dict["TAVG"]=avg
        new_dict["TMAX"]=max
        result_list.append(new_dict)
    session.close()

    return jsonify(result_list)
if __name__ == '__main__':
    app.run(debug=True)


    


