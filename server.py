#######Dependencies########
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import postreqs, putreqs, getreqs, deletereqs
import requests
###########################

# Create flask instance
app = Flask(__name__)

# To run on main page
@app.route('/')
def hello_world(result="Waiting for submit"):
    name = "test"
    return render_template("index.html", result=result, request_get=getreqs.reqsget.keys(),\
                           request_post=postreqs.reqspost.keys(), request_put=putreqs.reqsput.keys())

# To run on form submit
@app.route('/action', methods=['POST', 'GET'])
def action():

    # If the request to the flask server is of POST nature
    # It should always be the case, but if it's a GET request, something's gone wrong
    if request.method == 'POST':

        # Result holds the value of the form fields
        result = request.form

        # Let's gather some of the variables from the form
        url = request.form['host']
        req = request.form['request'].lower().split(' ')
        params = request.form['parameters']
        filename = request.form['file']

        # Headers indicate we are dealing with json data
        headers = {'content-type':'application/json'}

        # This checks for the request type selected in the form
        if request.form['reqtype'] == "POST":
            print "It's a post function"
            print params
            try:

                url_req = url + postreqs.reqspost[req[0]]
                print "got url", url_req

                if url_req[-3:]=='INC':
                    print "url is incomplete"
                    url_req = url + postreqs.postfuncs[req[0]](req, params, True)
                    print "new url is", url_req

                print "Requesting to URL:", url_req
                myResp = requests.post(url_req,auth=(request.form['username'], request.form['password']), headers=headers)
                print myResp
                result = postreqs.postfuncs[req[0]](myResp.json(), req[1:], False)
            except Exception as e:
                print "Request " + req[0] + " could not be comprehended"
                print e

        # If request type selected is GET
        elif request.form['reqtype'] == "GET":

            try:
                url_req = url + getreqs.reqsget[req[0]]

                if url_req[-3:]=='INC':
                    url_req = url + getreqs.getfuncs[req[0]](req, params, True)

                print "Requesting to URL:", url_req
                myResp = requests.get(url_req,auth=(request.form['username'], request.form['password']), headers=headers)
                print myResp
                result = getreqs.getfuncs[req[0]](myResp.json(), req[1:], False)
            except Exception as e:
                print "Request " + req[0] + " could not be comprehended"
                print e

        elif request.form['reqtype'] == "PUT":
            print "It's a put function"
            print params
            try:

                url_req = url + putreqs.reqsput[req[0]]
                print "got url", url_req

                if url_req[-3:]=='INC':
                    print "url is incomplete"
                    url_req = url + putreqs.putfuncs[req[0]](req, params, True)
                    print "new url is", url_req

                print "Requesting to URL:", url_req

                if filename != '':
                    files = {'file': open(filename, 'rb')}
                else:
                    files={}
                myResp = requests.put(url_req,auth=(request.form['username'], request.form['password']), headers=headers, files=files)
                print myResp
                result = putreqs.putfuncs[req[0]](myResp.json(), req[1:], False)
            except Exception as e:
                print "Request " + req[0] + " could not be comprehended"
                print e

        elif request.form['reqtype'] == "DEL":
            try:
                url_req = url + deletereqs.deletefuncs[req[0]]
                print 'inside try block'
                if url_req[-3:] == 'INC':
                    url_req = url + deletereqs.deletefuncs[req[0]](req, params, True)

                print "New url_req", url_req
                print "Requesting to URL:", url_req
                myResp = requests.delete(url_req, auth=(request.form['username'], request.form['password']), headers=headers)
                print myResp
                result = deletereqs.deletefuncs[req[0]](myResp.json(), params, False)
            except Exception as e:
                print "Request " + req[0] + " could not be comprehended"
                print e

        return render_template("index.html", result=result, request_get=getreqs.reqsget.keys(),\
                           request_post=postreqs.reqspost.keys(), request_put=putreqs.reqsput.keys())



if __name__ == '__main__':
    app.run()
