import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/'start'<br/>"
        f"/api/v1.0/'start'/'end'<br/>"
        f"------------------------------"
        f"Please be sure to put the dates in between the two ' symbols. format of example looks like ... /api/v1.0/'2015-01-01'/'2016-03-05' "
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    all_dates = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).all()
    all_dates_list = list(np.ravel(all_dates))
    max_date = all_dates_list[0]

    max_date_year = int(max_date[0:4])
    max_date_month = int(max_date[5:7])
    max_date_day = int(max_date[8:10])

    year_ago_from_max = dt.date(max_date_year, max_date_month, max_date_day) - dt.timedelta(days=366)
    year_ago_from_max_data = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date > year_ago_from_max).all()\
    # Query all passengers
    session.close()

    # Convert list of tuples into normal list
    all_list = list(np.ravel(year_ago_from_max_data))
    res_dct = {all_list[i+1]: all_list[i] for i in range(0, len(all_list), 2)} 
    return(res_dct)

  
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    all_dates1 = session.query(Measurement.date, Measurement.station).\
    order_by(Measurement.date.desc()).all()
    all_dates_list1 = list(np.ravel(all_dates1))
    max_date1 = all_dates_list1[0]

    max_date_year1 = int(max_date1[0:4])
    max_date_month1 = int(max_date1[5:7])
    max_date_day1 = int(max_date1[8:10])

    year_ago_from_max1 = dt.date(max_date_year1, max_date_month1, max_date_day1) - dt.timedelta(days=365)

    year_ago_from_max_data1 = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > year_ago_from_max1).all()

    session.close()
    return jsonify(year_ago_from_max_data1)
  
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    stations = session.query(Station.name).all()
    
    session.close()
    for station in stations:
        return jsonify(stations)

@app.route("/api/v1.0/justice-league/real_name/<real_name>")
def justice_league_by_real_name(real_name):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = real_name.replace(" ", "").lower()
    for character in justice_league_members:
        search_term = character["real_name"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404




@app.route("/api/v1.0/'<start>'")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    all_dates2 = session.query(Measurement.date, Measurement.tobs).\
    order_by(Measurement.date.desc()).all()
    all_dates_df = pd.DataFrame(all_dates2)
    all_dates_df_inc = all_dates_df.loc[all_dates_df["date"] >= f"{start}"]
    counter = int(all_dates_df_inc["tobs"].count())
    max_temp = all_dates_df_inc["tobs"].max()
    min_temp = all_dates_df_inc["tobs"].min()
    avg_temp = all_dates_df_inc["tobs"].mean()
    dct = {"Max temp": max_temp,
            "Min Temp": min_temp,
            "Avg Temp": avg_temp,
            "counter": counter}
    return jsonify(dct)
    session.close()
    
@app.route("/api/v1.0/'<start>'/'<end>'")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    all_dates3 = session.query(Measurement.date, Measurement.tobs).\
    order_by(Measurement.date.desc()).all()
    all_dates_df2 = pd.DataFrame(all_dates3)
    all_dates_df_inc2 = all_dates_df2.loc[(all_dates_df2["date"] >= f"{start}") & (all_dates_df2["date"] <= f"{end}")]
    counter2 = int(all_dates_df_inc2["tobs"].count())
    max_temp = all_dates_df_inc2["tobs"].max()
    min_temp = all_dates_df_inc2["tobs"].min()
    avg_temp = all_dates_df_inc2["tobs"].mean()
    dct = {"Max temp": max_temp,
            "Min Temp": min_temp,
            "Avg Temp": avg_temp,
            "counter": counter2}
    return jsonify(dct)
    session.close()
    


if __name__ == '__main__':
    app.run(debug=True)
