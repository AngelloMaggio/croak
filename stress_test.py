import requests


for i in range(1324):
    print i
    my_req = requests.delete("http://my-machine.com/docker-local/"+str(i), auth=("admin", "Jfrog0ffice"), json={'val':i})
    print my_req
