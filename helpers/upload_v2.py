﻿import logging
import os
import random
import string
import sys
import urllib2
import httplib

#https://stackoverflow.com/questions/68477/send-file-using-post-from-a-python-script

def random_string (length):
    return ''.join (random.choice (string.letters) for ii in range (length + 1))

def encode_multipart_data (files):
    boundary = random_string (30)

    def get_content_type (filename):
        return 'application/octet-stream'

    def encode_field (field_name):
        return ('--' + boundary,
                'Content-Disposition: form-data; name="%s"' % field_name,
                '', str (data [field_name]))

    def encode_file (field_name):
        filename = files [field_name]
        return ('--' + boundary,
                'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
                'Content-Type: %s' % get_content_type(filename),
                '', open (filename, 'rb').read ())

    lines = []
    for name in files:
        lines.extend (encode_file (name))
    lines.extend (('--%s--' % boundary, ''))
    body = '\r\n'.join (lines)

    headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
               'content-length': str (len (body))}

    return body, headers

def send_post (url, files):
    req = urllib2.Request (url)
    connection = httplib.HTTPConnection (req.get_host ())
    connection.request ('POST', req.get_selector (),
                        *encode_multipart_data (files))
    response = connection.getresponse ()
    logging.debug ('response = %s', response.read ())
    logging.debug ('Code: %s %s', response.status, response.reason)

for x in sys.argv[2:]:
    send_post ('http://' + sys.argv[1] + ':5000/upload', {'myFile':x})