# ######Dependencies########
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import postreqs, putreqs, getreqs, deletereqs
import requests
from flask_socketio import SocketIO, send, emit
# ##########################

# Create flask instance
app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('my_event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    result = get_result(json)
    out_dir = {}

    if isinstance(result, str):
        print "It's a string"
        out_dir['value'] = result
    elif isinstance(result, list):
        print "It's a list"

        for i in range(len(result)):
            out_dir[str(i+1)] = result[i]
    else:
        print "It's a dictionary"
        out_dir = result

    print out_dir
    send_result(out_dir)

# To run on main page
@app.route('/', methods=['POST', 'GET'])
def hello_world(result="Waiting for submit"):
    name = "test"
    return render_template("index.html", result=result, request_get=getreqs.get_requests.keys(), \
                           request_post=postreqs.post_requests.keys(), request_put=putreqs.reqsput.keys())


def send_result(result):
    socketio.emit('receive data', result)

def get_result(form_values):

    print "Inside the get_result function"


    # Result holds the value of the form fields
    # in case of error, this is what will be returned
    try:
        result = form_values

        # Let's gather some of the variables from the form
        url = form_values['host']
        req = form_values['request'].lower().split(' ')
        params = form_values['parameters']
        filename = form_values['file']
    except Exception as e:
        print "Error trying to gather value from form"
        print "Error:", e

    # Headers indicate we are dealing with json data
    headers = {'content-type': 'application/json'}

    # This checks for the request type selected in the form
    if form_values['type'] == "POST":

        try:
            url_req = url + postreqs.post_requests[req[0]]
        except Exception as e:
            print "Error during URL formatting function"
            print "Error:", e
        try:
            if url_req[-3:] == 'INC':
                url_req = url + postreqs.post_functions[req[0]](req, params)
        except Exception as e:
            print "Error during URL formatting function"
            print "Error:", e
        try:
            request_response = requests.post(url_req,auth=(form_values['username'], form_values['password']), headers=headers)
        except Exception as e:
            print "Error during post request"
            print "Error:", e

    # If request type selected is GET
    elif form_values['type'] == "GET":

        url_req = url + getreqs.get_requests[req[0]]

        if url_req[-3:] == 'INC':

            try:
                url_req = url + getreqs.get_functions[req[0]](req, params)
            except Exception as e:
                print "Error during URL formatting function"
                print "Error:", e

        try:
            request_response = requests.get(url_req,auth=(form_values['username'], form_values['password']), headers=headers)
        except Exception as e:
            print "Error while making API request"
            print "Error:", e
            request_response = ''


    elif form_values['type'] == "PUT":

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
            request_response = requests.put(url_req,auth=(form_values['username'], form_values['password']), headers=headers, files=files)
        except Exception as e:
            print "Error while making API request"
            print "Error:", e
            request_response = ''

    elif form_values['type'] == "DEL":

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
            request_response = requests.delete(url_req, auth=(form_values['username'], form_values['password']), headers=headers)
        except Exception as e:
            print "Error during API request."
            print "Error:", e
            request_response = ''

    else:
        request_response = "No Request Type Selected"

    try:
        result = request_response.json()

    except Exception as e:
        print "Error while trying to make response into json. Returning full response."
        result = request_response

    return result

if __name__ == '__main__':
    socketio.run(app)
