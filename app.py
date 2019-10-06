from sqlalchemy import func
from flask_pymongo import PyMongo
from forms import SearchForm
import pymongo

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

import os
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

engine = create_engine("sqlite:///new_flights.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Flights = Base.classes.flights

# Create an instance of Flask
app = Flask(__name__)


@app.route("/")
def home():
    # Return template and data
    return render_template("indexwithmap.html")

# Route that will trigger the scrape function

@app.route("/flights", methods=["GET", "POST"])
def flight():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    destino = " Amsterdam"
    fecha = "01/10/2019"
    results = session.query(Flights.airline, Flights.arrival, Flights.date, Flights.departure, Flights.flight_duration, Flights.plane, Flights.stops, Flights.ticket_price, Flights.IATA).filter(
        Flights.arrival.like(destino),
        Flights.date.like(fecha)
        )

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_flights = []
    for airline, arrival, date, departure, flight_duration, plane, stops, ticket_price, IATA in results:
        flight_dict = {}
        flight_dict["airline"] = airline
        flight_dict["arrival"] = arrival
        flight_dict["date"] = date
        flight_dict["departure"] = departure
        flight_dict["flight_duration"] = flight_duration
        flight_dict["plane"] = plane
        flight_dict["stops"] = stops
        flight_dict["ticket_price"] = ticket_price
        flight_dict["IATA"] = IATA
        all_flights.append(flight_dict)

    return jsonify(all_flights)

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        p_from = request.form["desde"]
        p_to = request.form["hasta"]
        p_date = request.form["fecha"]

    return render_template("results.html", p_from=p_from, p_to=p_to, p_date=p_date)

if __name__ == "__main__":
    app.run(debug=True)
