# ######Dependencies########
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import postreqs, putreqs, getreqs, deletereqs
import requests
# ##########################

# Create flask instance
app = Flask(__name__)


# To run on main page
@app.route('/')
def hello_world(result="Waiting for submit"):
    name = "test"
    return render_template("index.html", result=result, request_get=getreqs.get_requests.keys(), \
                           request_post=postreqs.post_requests.keys(), request_put=putreqs.reqsput.keys())


# To run on form submit
@app.route('/action', methods=['POST', 'GET'])
def action():

    # If the request to the flask server is of POST nature
    # It should always be the case, but if it's a GET request, something's gone wrong
    if request.method == 'POST':

        # Result holds the value of the form fields
        # in case of error, this is what will be returned
        try:
            result = request.form

            # Let's gather some of the variables from the form
            url = request.form['host']
            req = request.form['request'].lower().split(' ')
            params = request.form['parameters']
            filename = request.form['file']
        except Exception as e:
            print "Error trying to gather value from form"
            print "Error:", e

        # Headers indicate we are dealing with json data
        headers = {'content-type': 'application/json'}

        # This checks for the request type selected in the form
        if request.form['reqtype'] == "POST":

            try:

                url_req = url + postreqs.post_requests[req[0]]

                if url_req[-3:] == 'INC':
                    url_req = url + postreqs.post_functions[req[0]](req, params)

                request_response = requests.post(url_req,auth=(request.form['username'], request.form['password']), headers=headers)
                result = request_response.json()

            except Exception as e:
                print "Error has been raised:"
                print e

        # If request type selected is GET
        elif request.form['reqtype'] == "GET":

            url_req = url + getreqs.get_requests[req[0]]

            if url_req[-3:] == 'INC':

                try:
                    url_req = url + getreqs.get_functions[req[0]](req, params)
                except Exception as e:
                    print "Error during URL formatting function"
                    print "Error:", e

            try:
                request_response = requests.get(url_req,auth=(request.form['username'], request.form['password']), headers=headers)
            except Exception as e:
                print "Error while making API request"
                print "Error:", e

            try:
                result = request_response.json()
            except Exception as e:
                print "Error while trying to make response into json, returning full response in most likely text"
                result = request_response

        elif request.form['reqtype'] == "PUT":

            try:
                url_req = url + putreqs.reqsput[req[0]]

            except Exception as e:
                print "Request could not be found."
                print "Error:", e

            try:
                if url_req[-3:]=='INC':
                    url_req = url + putreqs.putfuncs[req[0]](req, params)

            except Exception as e:
                print "Error during URL formatting function"
                print "Error: ", e

            if filename != '':
                try:
                    files = {'file': open(filename, 'rb')}
                except Exception as e:
                    print "Error while trying to open file, perhaps wrong name or incomplete path"
                    print "Error:", e
            else:
                files = {}

            try:
                request_response = requests.put(url_req,auth=(request.form['username'], request.form['password']), headers=headers, files=files)
            except Exception as e:
                print "Error while making API request"
                print "Error:", e
                request_response = ''

            try:
                result = request_response.json()

            except Exception as e:
                print "Error while trying to make response into json. It's probably in text. Returning full response."
                result = request_response

        elif request.form['reqtype'] == "DEL":

            try:
                url_req = url + deletereqs.delete_requests[req[0]]

            except Exception as e:
                print "Request could not be found."
                print "Error:", e

            try:
                if url_req[-3:] == 'INC':
                    url_req = url + deletereqs.delete_functions[req[0]](req, params)
            except Exception as e:
                print "Error during URL formatting function."
                print "Error:", e

            try:
                request_response = requests.delete(url_req, auth=(request.form['username'], request.form['password']), headers=headers)
            except Exception as e:
                print "Error during API request."
                print "Error:", e
                request_response = ''

            try:
                result = request_response.json()

            except Exception as e:
                print "Error while trying to make response into json. Returning full response."
                result = request_response

        return render_template("index.html", result=result, request_get=getreqs.get_requests.keys(), \
                               request_post=postreqs.post_requests.keys(), request_put=putreqs.reqsput.keys())


if __name__ == '__main__':
    app.run()
