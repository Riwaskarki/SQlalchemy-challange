# Import the dependencies.
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()
Base.prepare(engine, reflect=True)
# Use the Base class to reflect the database tables
# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Station = Base.classes.station

Measurement = Base.classes.measurement


# Create a session

session = Session(engine)
#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify

app = Flask(__name__)

# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#Route to the precep
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Quering precipitation data for last year
    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    
    # Creating a dictionary from the data
    precip_dict = {date: prcp for date, prcp in precip_data}
    
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Quering all stations
    stations = session.query(Station.station).all()
    
    # Convert list of tuples into a normal list
    stations_list = list(np.ravel(stations))
    
    return jsonify(stations_list)


# route for the most active station.
@app.route("/api/v1.0/tobs")
def tobs():
    # Quering the dates and temperature observations of the most active station for the last year
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    
    # Convert list of tuples into a normal list
    tobs_list = list(np.ravel(tobs_data))
    
    return jsonify(tobs_list)


# route for the start and end.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    # Query to calculate TMIN, TAVG, and TMAX for dates
    if not end:
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    else:
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Converting list of tuples into a normal list
    temp_stats_list = list(np.ravel(temp_stats))
    
    return jsonify(temp_stats_list)




if __name__ =="__main__":
    app.run(debug=False)