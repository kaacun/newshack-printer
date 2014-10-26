# -*- coding: utf-8 -*-
import sys
import os
import boto.sqs
from boto.sqs.message import Message
from datetime import datetime
import json
from stl_tools import numpy2stl, text2png, text2array
from pylab import imread
from scipy.ndimage import gaussian_filter

AWS_ACCESS_KEY=''
AWS_SECRET_KEY=''

queue_name = 'newshack'

# connection
conn = boto.sqs.connect_to_region(
     "ap-northeast-1",
     aws_access_key_id=AWS_ACCESS_KEY,
     aws_secret_access_key=AWS_SECRET_KEY)

# Create or Get queue
queue = conn.create_queue(queue_name)
# Long Polling Setting
queue.set_attribute('ReceiveMessageWaitTimeSeconds', 20)

i=0
while 1:
    # fetch 10 messages
    msgs = queue.get_messages(10)
    for msg in msgs:
        pythoned_json = json.loads(msg.get_body().encode('utf_8'), encoding='utf-8')
        for corp,resp in pythoned_json.items():
          # sys.stderr.write("recv%s: %s\n" % (str(i), resp['title'].encode('utf_8')))
          text = resp['title'].encode('utf_8')

          # text convert to stl
          # text2png(text, "images/test", fontsize=1) #save png
          shell = "sh convert.sh '" + text + "'"
          os.system(shell)
          A = imread("images/convert.png") # read from rendered png
          A = A.mean(axis=2) #grayscale projection
          #A = gaussian_filter(A.max() - A, 1.)
          filename = "images/" + corp + ".stl"
          numpy2stl(A, filename)

        i = i+1
        # delete message
        queue.delete_message(msg)

    dt = datetime.today().strftime('%Y/%m/%d %H:%M:%S')
    sys.stderr.write("%s loop...\n" % (dt))
