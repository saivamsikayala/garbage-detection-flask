import caffe
import os, datetime
from flask import Flask, render_template, request
#from .forms import ImageForm
from .classifier import getPredictionsFor
from PIL import Image
from flask import jsonify
from . import settings
from flask_restful import Resource, Api, reqparse
from base64 import b64decode
from flask_cors import CORS
from flask_restful.utils.cors import crossdomain

app = Flask(__name__)
CORS(app)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#CORS(app, resources={r"/api/*":{"origins":["localhost", 'smart-bins-vitb.web.app']}})
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def prepareNet():
	proto_data = open(settings.MEAN_FILE, "rb").read()
	a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
	mean  = caffe.io.blobproto_to_array(a)[0]
	net = caffe.Net(settings.DEPLOY_FILE,settings.CAFFE_MODEL,caffe.TEST)
	return (mean, net)

mean, net = prepareNet()


class home(Resource):
	#form = ImageForm()
	#def options (self):
	#	return {'Allow' : 'POST' }, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : 'POST',  "Access-Control-Allow-Headers": "Content-Type" }

	@crossdomain(['*'], ['POST'])
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('data')
		parser.add_argument('width', type=int)
		parser.add_argument('height', type=int)
		parser.add_argument('mode', type=str)


		mode = parser['mode']
		width = parser['width']
		height = parser['height']
		image_data = b64decode(parser['data'])

		# extension = os.path.splitext(image_file.filename)[1]
		# filepath = os.path.join(settings.UPLOAD_FOLDER, \
		# 		datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')) + extension
		# image_file.save(filepath)
		#pre_process(filepath).save(filepath)
		#sample = Image.open(filepath)
		#image_files = []
		sample = Image.frombytes(mode, (width,height), image_data, 'raw')
		image_files.append([sample])
		#print(image_files)
		response = getPredictionsFor(image_files,net, mean)

		
		#print(filepath)
		print(response)
		return jsonify(response)

api.add_resource(home, '/')

# if __name__== "__main__":
# 	app.run(host="0.0.0.0")
