""" TREVOR JONES CS399se
Recreation of the Brevet Calculator from the www.rusa.org website
project 3 - ajax

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from miles, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles. 
  """
  app.logger.debug("Got a JSON request");

  #requests objects from user: distance, date, time
  distance = request.args.get('distance', 0, type=float)
  date = request.args.get('startDate')
  time = request.args.get('startTime')

  #Typical if/else table reflecting the algorithm used by rusa.org
  #to calculate open/close times at controle points
  if (distance == 0):
      #for the oddity rule that the closing time is one hour if the   control point is 0km
      min = distance
  if (distance == 0):
      ot = str(time);
      ct = str(time);
      return jsonify(cresult=ct, oresult=ot)
  if (distance < 200 and distance > 0):
      min = 15;
      max = 34;
  if (distance < 400 and distance > 200):
      min = 15;
      max = 32;
  if (distance < 600 and distance > 400):
      min = 15;
      max = 30;
  if (distance < 1000 and distance > 600):
      min = 11.428;
      max = 28;
  if (distance < 1300 and distance > 1000):
      min = 13.333;
      max = 26;
  #avg hours spent = distance / time
  open = distance / max;
  close = distance / min;

  #adjust date/time objects and reformat for display
  start = arrow.get(date + ' ' + time, 'MM/DD/YYYY HH:mm')
  openT = start.replace(hours=+open);
  ot = (str(openT.hour) + ":" + str(openT.minute));
  closeT = start.replace(hours=+close);
  ct = (str(closeT.hour) + ":" + str(closeT.minute));

  return jsonify(cresult=ct, oresult=ot)
 
#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad date)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
