from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bootstrap import Bootstrap
import postreqs, putreqs, getreqs
import requests

app = Flask(__name__)

@app.route('/')
def hello_world(result="Waiting for submit"):
    name = "test"
    return render_template("index.html", result=result, request_get=getreqs.reqsget.keys(),\
                           request_post=postreqs.reqspost.keys(), request_put=putreqs.reqsput.keys())


@app.route('/action', methods=['POST', 'GET'])
def action():

    # If the request to the flask server is of POST nature
    # It should always be the case, but if it's a GET request, something's gone wrong
    if request.method == 'POST':

        # Result holds the value of the form fields
        result = request.form

        url = request.form['host']
        req = request.form['request'].lower().split(' ')
        headers = {'content-type':'application/json'}
        print "Variables set"

        if request.form['reqtype'] == "POST":
            print "It is post"
            result = "Test"
        elif request.form['reqtype'] == "GET":

            try:
                url_req = url + getreqs.reqsget[req[0]]

                if url_req[-3:]=='INC':
                    url_req = url + getreqs.getfuncs[req[0]](req, 'INC')

                #print "New url_req", url_req
                print "Requesting to URL:", url_req
                myResp = requests.get(url_req,auth=(request.form['username'], request.form['password']), headers=headers)
                print myResp
                result = getreqs.getfuncs[req[0]](myResp.json(), req[1:])
            except Exception as e:
                print "Request " + req[0] + " could not be comprehended"
                print e

        elif request.form['reqtype'] == "PUT":
            pass
        elif request.form['reqtype'] == "DEL":
            pass

        return render_template("index.html", result=result, request_get=getreqs.reqsget.keys(),\
                           request_post=postreqs.reqspost.keys(), request_put=putreqs.reqsput.keys())



if __name__ == '__main__':
    app.run()
