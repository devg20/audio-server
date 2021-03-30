"""
Name: Dev Guha
link to connect to mongoDB database:
mongodb+srv://dev2000:<password>@cluster0.lbm60.mongodb.net/myFirstDatabase?retryWrites=true&w=majority

Before running the script, please edit line number 57 and add password.
I have sent the password on chat.

Please go through the below documentation for better understanding of the endpoints.

Defining all endpoints:

1. Create (Line Number 186)
To successfully create a new song/podcast/audiobook data entry on the database
use the following api call and json formats:

Api Call: http://127.0.0.1:5000/create-audio OR Using Heroku: https://audio-server-mongo.herokuapp.com/create-audio
	1.  For sending song data:
		Data to be sent in JSON format
		{
		    "audioFileType": "Song",
		    "audioFileMetadata": {
		    	"Id": 2,
		    	"Name": "We Don't Talk Anymore",
		    	"Duration": 231
		    }
		}

	2.  For sending podcast data:
		Data to be sent in JSON format
		{
		    "audioFileType": "Podcast",
		    "audioFileMetadata": {
				"Id": 3,
			    "Name": "The Data Skeptic",
			    "Duration": 1800,
			    "Host": "Kyle Polich",
			    "Participants": ["Prasanth Pulavarthi", "Kyle Polich"]
		    }
		}

	3.  For sending audiobook data:
		Data to be sent in JSON format
		{
		    "audioFileType": "Audiobook",
		    "audioFileMetadata": {
				"Id": 8,
			    "Title": "The Better Angels of Our Nature ",
			    "Author": "Steven Pinker",
			    "Narrator": "Arthur Murrey",
			    "Duration": 131940
		    }
		}

2. Delete (Line Number 259)
To successfully delete a song/podcast/audiobook data on the database,
use the following api calls:

	1.  For deleting song data:
		Api Call: http://127.0.0.1:5000/delete-audio/Song/<audioFileID> OR Using Heroku: https://audio-server-mongo.herokuapp.com/delete-audio/Song/<audioFileID>

	2.  For deleting podcast data:
		Api Call: http://127.0.0.1:5000/delete-audio/Podcast/<audioFileID> OR Using Heroku: https://audio-server-mongo.herokuapp.com/delete-audio/Podcast/<audioFileID>

	3.  For deleting audiobook data:
		Api Call: http://127.0.0.1:5000/delete-audio/Audiobook/<audioFileID> OR Using Heroku: https://audio-server-mongo.herokuapp.com/delete-audio/Audiobook/<audioFileID>

3. Update (Line Number 268)
To successfully update a song/podcast/audiobook data on the database,
use the following api call and json formats:
NOTE: New ID cannot be assigned.

	1.  For updating song data:
		Api Call: http://127.0.0.1:5000/update-audio/Song/<audioFileID> OR Using Heroku: https://audio-server-mongo.herokuapp.com/update-audio/Song/<audioFileID>
		Data to be sent in JSON format
		{
			"audioFileType": "Song", #Only if audioFileType is to updated
		    "audioFileMetadata": {
		    	"Name": "Titanium",
		    	"Duration": 245
		    }
		}

	2.  For updating podcast data:
		Api Call: http://127.0.0.1:5000/update-audio/Podcast/<audioFileID> OR Using Heroku: https://audio-server-mongo.herokuapp.com/update-audio/Podcast/<audioFileID>
		Data to be sent in JSON format
		{
		    "audioFileType": "Podcast", #Only if audioFileType is to updated
		    "audioFileMetadata": {
			    "Name": "xyz",
			    "Duration": 2000,
			    "Host": "AAA BBB",
			    "Participants": ["Dev", "Aman"]
		    }
		}

	3.  For updating audiobook data:
		Api Call: http://127.0.0.1:5000/update-audio/Audiobook/<audioFileID> OR Using Heroku: https://audio-server-mongo.herokuapp.com/update-audio/Audiobook/<audioFileID>
		Data to be sent in JSON format
		{
		    "audioFileType": "Audiobook", #Only if audioFileType is to updated
		    "audioFileMetadata": {
			    "Title": "Any ",
			    "Author": "Adam",
			    "Narrator": "Siri",
			    "Duration": 20000
		    }
		}

4. Get (Line Number 282)
To successfully get details of a song/podcast/audiobook data on the database,
use the following api calls:

	1.  For getting song data:
		Api Call: http://127.0.0.1:5000/Song/<audioFileID> OR Using Heroku: https://audio-server-mongo.herokuapp.com/Song/<audioFileID>
		For getting all songs data:
		Api Call: http://127.0.0.1:5000/Song OR Using Heroku: https://audio-server-mongo.herokuapp.com/Song
	2.  For getting podcast data:
		Api Call: http://127.0.0.1:5000/Podcast/<audioFileID> OR Using Heroku: https://audio-server-mongo.herokuapp.com/Podcast/<audioFileID>
		For getting all podcasts data:
		Api Call: http://127.0.0.1:5000/Podcast OR Using Heroku: https://audio-server-mongo.herokuapp.com/Podcast

	3.  For getting audiobook data:
		Api Call: http://127.0.0.1:5000/Audiobook/<audioFileID> OR Using Heroku: https://audio-server-mongo.herokuapp.com/Audiobook/<audioFileID>
		For getting all audiobooks data:
		Api Call: http://127.0.0.1:5000/Audiobook OR Using Heroku: https://audio-server-mongo.herokuapp.com/Audiobook

"""

#Importing required packages
import pymongo
from pymongo import MongoClient
import urllib
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import json
import os

#Defining class songFile to create objects of song files
class songFile:
	def __init__(self, songId, songName, songDuration):
		self.songId = int(songId)
		self.songName = str(songName)
		self.songDuration = int(songDuration)
		self.songUploadTime = str(datetime.now())
	def getUploadTime(self):
		self.songUploadTime = str(datetime.now())

#Defining class podcastFile to create objects of podcast files
class podcastFile:
	def __init__(self, podcastId, podcastName, podcastDuration, podcastHost, podcastParticipants):
		self.podcastId = int(podcastId)
		self.podcastName = str(podcastName)
		self.podcastDuration = int(podcastDuration)
		self.podcastHost = str(podcastHost)
		self.podcastParticipants = podcastParticipants
		self.podcastUploadTime = str(datetime.now())
	def getUploadTime(self):
		self.podcastUploadTime = str(datetime.now())

#Defining class audiobookFile to create objects of audiobook files
class audiobookFile:
	def __init__(self, audiobookId, audiobookTitle, audiobookAuthor, audiobookNarrator, audiobookDuration):
		self.audiobookId = audiobookId
		self.audiobookTitle = audiobookTitle
		self.audiobookAuthor = audiobookAuthor
		self.audiobookNarrator = audiobookNarrator
		self.audiobookDuration = audiobookDuration
		self.audiobookUploadTime = str(datetime.now())
	def getUploadTime(self):
		self.audiobookUploadTime = str(datetime.now())

#Connecting to MongoDB 
password = "dev@2000"
cluster = MongoClient("mongodb+srv://dev2000:" + urllib.parse.quote_plus(password) + "@cluster0.lbm60.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["audio"]
collection = db["audio"]

#Defining flask app name and enabling cors
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/create-audio', methods=['POST']) # Create Endpoint
def createAudio():
	data = request.get_json()
	fileType = str(data["audioFileType"])
	if fileType.lower() == "song":
		if all(item in data["audioFileMetadata"].keys() for item in ["Id", "Name", "Duration"]):
			if len(str(data["audioFileMetadata"]["Name"])) <= 100:
				songId = int(data["audioFileMetadata"]["Id"])
				songName = str(data["audioFileMetadata"]["Name"])
				songDuration = int(data["audioFileMetadata"]["Duration"])
				sf = songFile(songId, songName, songDuration)
				sf.getUploadTime()
				document = {"_id": sf.songId, "FileType": "Song", "Name": sf.songName , "Duration": sf.songDuration, "Upload Time": sf.songUploadTime}
				try:
					result = collection.insert_one(document)
					return "Action is successful: 200 OK\n\n**Song Data uploaded to Database!**"
				except pymongo.errors.DuplicateKeyError:
					return "The request is invalid: 400 bad request\n\n**File with same ID already exists!**"
			else:
				return "**NOTE: The length of field Name should be less than 100 characters.**"
		else:
			return "**Please enter all mandatory data fields!**"
	elif fileType.lower() == "podcast":
		if all(item in data["audioFileMetadata"].keys() for item in ["Id", "Name", "Duration", "Host"]):
			if len(max([data["audioFileMetadata"]["Name"], data["audioFileMetadata"]["Host"]], key=len)) <= 100:
				podcastId = int(data["audioFileMetadata"]["Id"])
				podcastName = str(data["audioFileMetadata"]["Name"])
				podcastDuration = int(data["audioFileMetadata"]["Duration"])
				podcastHost = str(data["audioFileMetadata"]["Host"])
				if "Participants" in data["audioFileMetadata"].keys():
					if len(data["audioFileMetadata"]["Participants"]) <= 10 and len(max(data["audioFileMetadata"]["Participants"], key=len)) <= 100:
						podcastParticipants = data["audioFileMetadata"]["Participants"]
						pf = podcastFile(podcastId, podcastName, podcastDuration, podcastHost, podcastParticipants)
					else:
						return "**NOTE: Only 10 Participants allowed with length of names less than 100 characters.**"
				else:
					podcastParticipants = []
					pf = podcastFile(podcastId, podcastName, podcastDuration, podcastHost, podcastParticipants)
				pf.getUploadTime()
				document = {"_id": pf.podcastId, "FileType": "Podcast", "Name": pf.podcastName , "Duration": pf.podcastDuration, "Host": pf.podcastHost, "Participants": pf.podcastParticipants, "Upload Time": pf.podcastUploadTime}
				try:
					collection.insert_one(document)
					return "Action is successful: 200 OK\n\n**Podcast Data uploaded to Database!**"
				except pymongo.errors.DuplicateKeyError:
					return "The request is invalid: 400 bad request\n\n**File with same ID already exists!**"
			else:
				return "**NOTE: The length of fields Name and Host should be less than 100 characters.**"
		else:
			return "**Please enter all mandatory data fields!**"

	elif fileType.lower() == "audiobook":
		if all(item in data["audioFileMetadata"].keys() for item in ["Id", "Title", "Author", "Narrator", "Duration"]):
			if len(max([data["audioFileMetadata"]["Title"], data["audioFileMetadata"]["Author"], data["audioFileMetadata"]["Narrator"]], key=len)) <= 100:
				audiobookId = int(data["audioFileMetadata"]["Id"])
				audiobookTitle = str(data["audioFileMetadata"]["Title"])
				audiobookAuthor = str(data["audioFileMetadata"]["Author"])
				audiobookNarrator = str(data["audioFileMetadata"]["Narrator"])
				audiobookDuration = int(data["audioFileMetadata"]["Duration"])
				abf = audiobookFile(audiobookId, audiobookTitle, audiobookAuthor, audiobookNarrator, audiobookDuration)
				abf.getUploadTime()
				document = {"_id": abf.audiobookId, "FileType": "Audiobook", "Title": abf.audiobookTitle , "Author": abf.audiobookAuthor, "Narrator": abf.audiobookNarrator, "Duration": abf.audiobookDuration, "Upload Time": abf.audiobookUploadTime}
				try:
					collection.insert_one(document)
					return "Action is successful: 200 OK\n\n**Audiobook Data uploaded to Database!**"
				except pymongo.errors.DuplicateKeyError:
					return "The request is invalid: 400 bad request\n\n**File with same ID already exists!**"
			else:
				return "**NOTE: The length of fields Title, Author and Narrator should be less than 100 characters.**"
		else:
			return "**Please enter all mandatory data fields!**"


@app.route('/delete-audio/<audioFileType>/<audioFileID>', methods=['POST']) # Delete Endpoint
def deleteAudio(audioFileType, audioFileID):
	parameters = {"FileType": str(audioFileType), "_id": int(audioFileID)}
	results = collection.delete_many(parameters)
	if results.deleted_count > 0:
		return "Action is successful: 200 OK\n\n**Deleted relevant audio file data!**"
	else:
		return "The request is invalid: 400 bad request\n\n**File not found!**"


@app.route('/update-audio/<audioFileType>/<audioFileID>', methods=['POST']) # Update Endpoint
def updateAudio(audioFileType, audioFileID):
	data = request.get_json()
	parameters = {"FileType": str(audioFileType), "_id": int(audioFileID)}
	if "audioFileType" in data.keys():
		collection.update_one(parameters, {"$set": {"FileType": str(data["audioFileType"])}})
	for key, val in data["audioFileMetadata"].items():
		results = collection.update_one(parameters, {"$set": {key: val}})
	if results.modified_count > 0:
		return "Action is successful: 200 OK\n\n**Updated relevant audio file data!**"
	else:
		return "The request is invalid: 400 bad request\n\n**File not found!**"


@app.route('/<audioFileType>', defaults={'audioFileID': None}, methods=['POST']) # Get Endpoint
@app.route('/<audioFileType>/<audioFileID>', methods=['POST'])
def getAudio(audioFileType, audioFileID):
	if audioFileID:
		parameters = {"FileType": str(audioFileType), "_id": int(audioFileID)}
		result = collection.find_one(parameters)
		if result:
			return result
		else:
			return "The request is invalid: 400 bad request\n\n**File not found!**"
	else:
		parameters = {"FileType": str(audioFileType)}
		results = collection.find(parameters)
		if results.count() > 0:
			r = {}
			for i, result in enumerate(results):
				r["File " + str(i+1)] = result
			return r
		else:
			return "The request is invalid: 400 bad request\n\n**File not found!**"

#Running Flask server below.
if __name__=='__main__':
    app.run(port=int(os.environ.get('PORT', 5000)), debug=True)

