from kivy.app import App
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from getreqs import get_requests, get_functions
from postreqs import post_requests, post_functions
from putreqs import reqsput, putfuncs
import requests
from kivy.uix.togglebutton import ToggleButton as TB
import json
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

class Croak(Screen):

    def build(self):



        self.f_request = StringProperty()
        self.f_params = StringProperty()
        self.f_username = StringProperty()
        self.f_password = StringProperty()
        self.f_host = StringProperty()
        self.f_output = StringProperty()
        self.f_file = StringProperty()
        self.callType = None
        self.newParams = {}
        self.spinnerbox = ObjectProperty()

        spinner = Spinner(
            # default value shown
            text='Home',
            # available values
            values=('Home', 'Work', 'Other', 'Custom'),
            # just for positioning in our example
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': .5, 'center_y': .5})

        def show_selected_value(spinner, text):
            print('The spinner', spinner, 'have text', text)

        spinner.bind(text=show_selected_value)

        self.spinnerbox.add_widget(spinner)


    def runreq(self):
        tb = next( (t for t in TB.get_widgets('callType') if t.state=='down'), None)
        self.callType = tb.text if tb else None

        print "Call type", self.callType
        print "Host", self.f_host.text
        print "Username", self.f_username.text
        print "Password", self.f_password.text
        print "Request", self.f_request.text
        print "File Selected", self.f_file.text

        try:
            print "Params", self.f_params.text
            self.newParams = json.loads(self.f_params.text)
        except Exception as e:
            print "params err"
            print e
        req = self.f_request.text.lower().split(' ')
        req.append(' ')
        url = self.f_host.text
        headers = {'content-type':'application/json'}


        print "Everything ready"

        if self.callType == "GET":
            try:
                url_req = url + get_requests[req[0]]

                if url_req[-3:]=='INC':
                    url_req = url + get_functions[req[0]](req, 'INC')

                #print "New url_req", url_req
                print "Requesting to URL:", url_req
                myResp = requests.get(url_req,auth=(self.f_username.text, self.f_password.text), headers=headers)
                print myResp
                self.f_output.text = get_functions[req[0]](myResp.json(), req[1:])
            except Exception as e:
                print "Request " + req[0] + " could not be comprehended"
                print e

        elif self.callType == "POST":

            try:
                url_req = url + post_requests[req[0]]

                if url_req[-3:]=='INC':
                    url_req = url + post_functions[req[0]](req, 'INC')
                if self.f_file.text != '':
                    try:
                        files={'file': open(self.f_file.text, 'rb')}
                    except:
                        files={}
                else:
                    files=None

                #print "New url_req", url_req
                print "Requesting to URL:", url_req

                myResp = requests.post(url_req,auth=(self.f_username.text, self.f_password.text), headers=headers, json=self.newParams, files=files)

                self.f_output.text = post_functions[req[0]](myResp.json(), req[1:])
            except Exception as e:
                self.f_output.text = "Request " + req[0] + " could not be comprehended"
                print e


        elif self.callType == "PUT":
            print "Call type selected is PUT"
            try:
                url_req = url + reqsput[req[0]]
                print url_req

                if url_req[-3:]=='INC':
                    print "URL is INC"
                    url_req = url + putfuncs[req[0]](req, 'INC')



                try:
                    files={'file': open(self.f_file.text, 'rb')}
                except:
                    files={}
                if self.newParams == {}:
                    self.newParams = None
                print "New url_req", url_req
                print "Requesting to URL:", url_req
                myResp = requests.put(url_req, auth=(self.f_username.text, self.f_password.text), headers=headers, json=self.newParams, files=files)

                self.f_output.text = putfuncs[req[0]](myResp.json(), req[1:])

            except Exception as e:
                self.f_output.text = "Request " + req[0] + " could not be comprehended - " + str(e)



        else:
            self.f_output.text =  "Select Call type GET/POST/PUT/DEL"


class CroakApp(App):

    def build(self):

        croak = Croak()

        return croak

class CustomDropDown(DropDown):
    pass



if __name__ == '__main__':
    CroakApp().run()
