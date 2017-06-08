#!/usr/bin/env python

import argparse
import requests
import json


def receive_json(source, page_num):
    if args.verbose:
        print "Pulling data from " + source
    r = requests.get(source, params={'page': str(page_num), 'format': 'json'})
    if args.verbose:
        print "Received", r.content.__sizeof__(), "bytes from source."
    return r.content


def post_json(data, destination):
    r = requests.post(destination, headers={
                      "Content-Type": "application/json"}, data=data)
    errors = 0
    if r.status_code == 201:
        # if args.verbose:
        #    print "OK. Returned an HTTP 201 for Created."
        pass
    else:
        # if args.verbose:
        #    print "Error. Response:", r.status_code
        errors += 1
    return errors


def iterate_and_post(jsonData, destination):
    try:
        true_json = json.loads(jsonData)
    except:
        print "Failed to load JSON data."
        print "Have you tried removing slashes from the end of the URL?"
        return 1
    if args.verbose:
        print "Posting objects to", destination
    i = 0
    errors = 0
    for element in true_json["results"]:  # iterates over inner objects
        # json.dumps removes unicode
        errors += post_json(json.dumps(element), destination)
        i += 1
    if errors == 0:
        if args.verbose:
            print "Posted", i, "JSON objects to destination."
    else:
        if args.verbose:
            print "Attempted", i, "JSON posts, resulted with", errors, "errors."
    return errors


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output")
parser.add_argument("source", type=str,
                    help="source URL of api from which to extract (GET) JSON")
parser.add_argument("destination", type=str,
                    help="destination URL for insertion (PUSH) of JSON data")
parser.add_argument("-c", "--count", type=int, default=1,
                    help="number of pages to copy data from (defaults to 1)")
args = parser.parse_args()

if __name__ == "__main__":
    errors = 0
    get_url = args.source
    post_url = args.destination
    if args.count >> 0:
        page_count = args.count
    else:
        page_count = 1
    for page in range(1, page_count + 1):
        if args.verbose:
            print
            print "Copying page", page
        data = receive_json(get_url, page)
        errors += iterate_and_post(data, post_url)
    if errors == 0:
        print "Done."
    else:
        print "The script exited with", errors,"errors."
