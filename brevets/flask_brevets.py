"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()


###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', "", type=float)
    distance = request.args.get("distance", "", type=float)
    date = request.args.get("sdate","", type = str)
    time = request.args.get("stime","", type = str)

    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    
    mtime = arrow.get(date + " " + time,'YYYY-MM-DD HH:mm').isoformat()

    open_time = acp_times.open_time(km, distance, mtime)
    close_time = acp_times.close_time(km, distance, mtime)
    result = {"open": open_time, "close": close_time, "time": time , "date": date, "mtime":mtime}
    return flask.jsonify(result=result)


############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
