from flask import Flask, render_template, request, redirect, url_for, session
<<<<<<< HEAD
import postreqs, putreqs, getreqs, DeleteReqs
=======
from flask_bootstrap import Bootstrap

import postreqs, putreqs, getreqs
>>>>>>> 76b01065a7a69717425ae0071b1178bff41521bf
import requests

app = Flask(__name__)

@app.route('/')
def hello_world(result="Waiting for submit"):
    name = "test"
    return render_template("index.html", result=result)


@app.route('/action', methods=['POST', 'GET'])
def action():

    if request.method == 'POST':
        print "Post method"

        result = request.form
        print "Result:", 
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
            try:
                url_req = url + DeleteReqs.deletefuncs[req[0]]
                print 'inside try block'
                if url_req[-3:] == 'INC':
                    url_req = url + DeleteReqs.deletefuncs[req[0]](req, 'INC')

                print "New url_req", url_req
                print "Requesting to URL:", url_req
                myResp = requests.delete(url_req, auth=(request.form['username'], request.form['password']), headers=headers)
                print myResp
                result = DeleteReqs.deletefuncs[req[0]](myResp.json(), req[1:])
            except Exception as e:
                print "Request " + req[0] + " could not be comprehended"
                print e

        return render_template("index.html", result=result)



if __name__ == '__main__':
    app.run()
