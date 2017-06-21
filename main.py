
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from artifactoryreqs import reqsget, getfuncs, reqspost, postfuncs
import requests
from kivy.uix.togglebutton import ToggleButton as TB
import json

class Croak(Screen):

    def build(self):
        self.f_request = StringProperty()
        self.f_params = StringProperty()
        self.f_username = StringProperty()
        self.f_password = StringProperty()
        self.f_host = StringProperty()
        self.f_output = StringProperty()
        self.callType = None

    def runreq(self):
        tb = next( (t for t in TB.get_widgets('callType') if t.state=='down'), None)
        self.callType = tb.text if tb else None

        print "Call type", self.callType
        print "Host", self.f_host.text
        print "Username", self.f_username.text
        print "Password", self.f_password.text
        print "Request", self.f_request.text

        self.f_output.text = "Output goes here"
        try:
            print "Params", self.f_params.text
            self.f_params = json.loads(self.f_params.text)
        except Exception as e:
            print "params err"
            print e
        req = self.f_request.text.lower().split(' ')
        req.append(' ')
        url = self.f_host.text
        headers = {'content-type':'application/json'}

        if self.callType == "GET":
            try:
                url_req = url + reqsget[req[0]]

                if url_req[-3:]=='INC':
                    url_req = url + getfuncs[req[0]](req, 'INC')

                #print "New url_req", url_req
                print "Requesting to URL:", url_req
                myResp = requests.get(url_req,auth=(self.f_username.text, self.f_password.text), headers=headers)

                self.f_output.text = getfuncs[req[0]](myResp.json(), req[1:])
            except Exception as e:
                print "Request", req[0], "could not be comprehended"
                print e

        elif self.callType == "POST":

            try:
                url_req = url + reqspost[req[0]]

                if url_req[-3:]=='INC':
                    url_req = url + postfuncs[req[0]](req, 'INC')

                #print "New url_req", url_req
                print "Requesting to URL:", url_req
                myResp = requests.post(url_req,auth=(self.f_username.text, self.f_password.text), headers=headers, json=self.f_params)

                self.f_output.text = postfuncs[req[0]](myResp.json(), req[1:])
            except Exception as e:
                self.f_output.text = "Request", req[0], "could not be comprehended"
                print e


        else:
            self.f_output.text =  "Select Call type GET/POST"


class CroakApp(App):

    def build(self):


        croak = Croak()

        #text_input = TextInput(text="Enter request:")

        #croak.add_widget(text_input)
        return croak




if __name__ == '__main__':
    CroakApp().run()
