from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

@app.route('/')
def hello_world(result="Waiting for submit"):
    name = "test"
    return render_template("index.html", result=result)

@app.route('/<result>',methods=['POST'])
def hello_world2(result=None):
    #print request.form['host']
    return render_template("index.html", result=result)


@app.route('/action', methods=['POST', 'GET'])
def action():
    if request.method == 'POST':
        print "Post method"
        result = request.form
        return render_template("index.html", result=result)


if __name__ == '__main__':
    app.run()
