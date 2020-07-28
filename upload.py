#!/usr/bin/env python3

import pyrebase
import os

# On Pi...
record_path='/home/pi/work-dir/journal-entry/entries/'
#On Mac
# record_path = '/Users/williambennett/Documents/Github/good-listener/recordings/'
upload_path = 'journal/'
file_extension = '.txt'

config = {
    'apiKey': "AIzaSyCA2KM8dr6cEMCjGo36sVXSwkh4xccU1nA",
    'authDomain': "good-listener-e2f7b.firebaseapp.com",
    'databaseURL': "https://good-listener-e2f7b.firebaseio.com",
    'projectId': "good-listener-e2f7b",
    'storageBucket': "good-listener-e2f7b.appspot.com",
    'messagingSenderId': "475441924589",
    'appId': "1:475441924589:web:ad3e5b2a52171b738dffe4",
    'measurementId': "G-6JX74D18HK"
  };

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

print("found %d files to upload" % len(os.listdir(record_path)))
# exit(0)

# print("Database?")
# print(storage.list_files())
# exit(0)

for file in os.listdir(record_path):
    if file.endswith(file_extension):
        local_file = os.path.join(record_path, file)
        remote_file = os.path.join(upload_path, file)
        try:
            storage.child(remote_file).put(local_file)
            print("\n>>> uploaded local: \n%s\n>>> to remote:\n%s" % (local_file, remote_file))
            os.remove(local_file)
            print("file removed")
        except:
            print("error uploading >> %s\n" % file)

# print("the dir looks like this now: \n")
# for file in os.listdir(record_path):
    # print(file)

exit(0)
