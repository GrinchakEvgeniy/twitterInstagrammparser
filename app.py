from flask import Flask, render_template, request, jsonify, send_file
from spider import parser, test, twitter
import time 
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
	return "OK"

@app.route("/.well-known/pki-validation/DBA3062610F402ACB1677D8F682BF43A.txt")
def ssl():
	return send_file("/mnt/.well-known/pki-validation/DBA3062610F402ACB1677D8F682BF43A.txt", attachment_filename="DBA3062610F402ACB1677D8F682BF43A.txt")


@app.route("/force", methods=['GET'])
def force_():
	parser()
	# print(type())
	twitter()
	return {}


@app.route("/get_hastags", methods=['POST'])
def get_hashtags():
	req = request.get_json()
	with open("data.json", "r") as jsonFile:
		jsonObject = json.load(jsonFile)
		jsonObject['hashtags'] = req['hashtags']
		jsonString = json.dumps(jsonObject)
		jsonFile.close()
	with open("data.json", "w") as file:
		file.write(jsonString)
		file.close()

	if req['force']:
		parser()

	with open("data.json", "r") as jsonFile2:
		jsonObject2 = json.load(jsonFile2)
		jsonFile.close()
	return jsonify(jsonObject2)


@app.route("/access", methods=["GET"])
def access():
	with open("file_access.json", "r") as jsonFile:
		jsonObject = json.load(jsonFile)
		jsonFile.close()
	return render_template('access.html', data=jsonObject)


@app.route("/new_access", methods=['POST'])
def new_access():
	req = request.get_json()
	with open("file_access.json", "r") as jsonFile:
		jsonObject = json.load(jsonFile)
		jsonFile.close()
	if req['type'] == 'instagram':
		jsonObject['instagram']['login'] = req['login']
		jsonObject['instagram']['password'] = req['password']
	jsonString = json.dumps(jsonObject)
	with open("file_access.json", "w") as file:
		file.write(jsonString)
		file.close()
	return jsonify({"result":True})


@app.route("/test_access", methods=['POST'])
def test_access():
	req = request.get_json()
	result = test(req['type'], req['login'], req['password'])
	return jsonify({'result':result})


