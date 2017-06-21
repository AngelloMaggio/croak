
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from artifactoryreqs import reqs, reqfuncs
import requests

class Croak(Screen):

    def build(self):
        self.f_request = StringProperty()
        self.f_params = StringProperty()
        self.f_username = StringProperty()
        self.f_password = StringProperty()
        self.f_host = StringProperty()
        self.f_output = StringProperty()

    def runreq(self):
        print "Host", self.f_host.text
        print "Username", self.f_username.text
        print "Password", self.f_password.text
        print "Request", self.f_request.text
        print "Params", self.f_params.text
        self.f_output.text = "TESTTT"

        req = self.f_request.text.lower().split(' ')
        req.append(' ')
        url = self.f_host.text
        headers = {'content-type':'application/json'}

        try:
            url_req = url + reqs[req[0]]

            if url_req[-3:]=='INC':
                url_req = url + reqfuncs[req[0]](req, 'INC')

            #print "New url_req", url_req
            print "Requesting to URL:", url_req
            myResp = requests.get(url_req,auth=(self.f_username.text, self.f_password.text), headers=headers)

            self.f_output.text = reqfuncs[req[0]](myResp.json(), req[1:])
        except Exception as e:
            print "Request", req[0], "could not be comprehended"
            print e

class CroakApp(App):

    def build(self):


        croak = Croak()

        #text_input = TextInput(text="Enter request:")

        #croak.add_widget(text_input)
        return croak




if __name__ == '__main__':
    CroakApp().run()
