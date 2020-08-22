import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine(r'sqlite:///Resources\hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List of all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(distinct(Measurement.station)).all()

    session.close()

    # Create a list from the row data of all unique stations
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data"""
    # Query temperature at most active station over the last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all temperatures
    temps = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        temps.append(tobs_dict)

    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def start_only_temps(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data"""
    # Query temperature min, max, and avg from a start date
    temp_min = func.min(Measurement.tobs)
    temp_max = func.max(Measurement.tobs)
    temp_avg = func.avg(Measurement.tobs)
    sel = [temp_min, temp_max, temp_avg]
    results = session.query(*sel).filter(Measurement.date >= start).all()

    # Create a dictionary from the row data and append to a list of all temperatures
    temp_data_results = []
    for temp_min, temp_max, temp_avg in results:
        tdr_dict = {}
        tdr_dict["Lowest Temp"] = temp_min
        tdr_dict["Highest Temp"] = temp_max
        tdr_dict["Average Temp"] = temp_avg
        temp_data_results.append(tdr_dict)

    return jsonify(temp_data_results)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temps(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data"""
    # Query temperature min, max, and avg between a start and end date
    temp_min = func.min(Measurement.tobs)
    temp_max = func.max(Measurement.tobs)
    temp_avg = func.avg(Measurement.tobs)
    sel = [temp_min, temp_max, temp_avg]
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a dictionary from the row data and append to a list of all temperatures
    temp_data_results = []
    for temp_min, temp_max, temp_avg in results:
        tdr_dict = {}
        tdr_dict["Lowest Temp"] = temp_min
        tdr_dict["Highest Temp"] = temp_max
        tdr_dict["Average Temp"] = temp_avg
        temp_data_results.append(tdr_dict)

    return jsonify(temp_data_results)

if __name__ == '__main__':
    app.run(debug=True)
