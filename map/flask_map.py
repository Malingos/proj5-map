"""
Flask server to run map project
"""
import flask
from flask import request
import config
import logging
import pre
###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
#linesInLocation = 5
data = pre.process(open(CONFIG.LOCATIONS))
#data = pre.process(open(configuration.LOCATIONS))

#Data is a 2 dimensional array, containing name,lat,lon
###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    """Loads map"""
    app.logger.debug("Main page entry")
    flask.g.twoDArray = data
    return flask.render_template('map.html')

@app.route("/refresh")
def refresh():
    """ Use to reload schedule"""
    global data
    data = pre.process(open(configuration.LOCATIONS))
    return flask.redirect(flask.url_for("index"))

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def i_am_busted(error):
    return flask.render_template('500.html'), 500
###
# AJAX request handlers
###
#@app.route("/_mapJS")
#def _mapJS():
#    app.logger.debug("Got JSON request")
#    return flask.jsonify()#FIXME empty retval for now

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
