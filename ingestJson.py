import requests
import json
import sys


def help():
    print
    print "ingestJson ingests API data from mantid production to local server."
    print "To use, provide a mantid API name as an argument."
    print "usage: python ingestJson.py <apiName>"
    print "example: python ingestJson.py feature"
    print "would pull from mantidproject.org/api/feature and post @ localhost."
    exit(0)


def receive_json():
    print "Pulling data from " + get_url
    r = requests.get(get_url, params={'format': 'json'})
    return r.content


def send(data):
    print "Posting to " + post_url + "\n"
    r = requests.post(post_url, headers={
                      "Content-Type": "application/json"}, data=data)
    if str(r) == "<Response [201]>":
        print "OK. Returned an HTTP 201 for Created."
    else:
        print "Response:"
        print r


def main():
    apiData = receive_json()
    true_json = json.loads(apiData)
    for element in true_json["results"]:  # iterates over inner objects
        send(json.dumps(element))  # removes unicode


argNum = len(sys.argv)
if argNum == 1:
    help()
elif argNum == 2:
    arg = str.lower(sys.argv[1])
    if arg == 'help' or arg == '--help' or arg == '-help':
        help()
    else:
        apiName = arg
        get_url = "http://reports.mantidproject.org/api/" + apiName
        post_url = "http://127.0.0.1:8000/api/" + apiName
        main()
