import caffe
import os, datetime
from flask import Flask, render_template, request
from .forms import ImageForm
from .classifier import getPredictionsFor
from PIL import Image
from flask import jsonify
from . import settings


app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def prepareNet():
	proto_data = open(settings.MEAN_FILE, "rb").read()
	a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
	mean  = caffe.io.blobproto_to_array(a)[0]
	net = caffe.Net(settings.DEPLOY_FILE,settings.CAFFE_MODEL,caffe.TEST)
	return (mean, net)

#mean, net = prepareNet()

@app.route('/', methods=['GET', 'POST'])
def home():
	form = ImageForm()
	if request.method == 'POST':
		image_file = form.image.data
		extension = os.path.splitext(image_file.filename)[1]
		filepath = os.path.join(settings.UPLOAD_FOLDER, \
                datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')) + extension
		image_file.save(filepath)
		#pre_process(filepath).save(filepath)
		sample = Image.open(filepath)
		image_files = []
		image_files.append(sample)
		#print(image_files)
		response = getPredictionsFor(image_files,net, mean)

		
		#print(filepath)
		print(response)
		return jsonify(response)
	else:
		return render_template('home.html')


if __name__== "__main__":
	app.run(host="0.0.0.0")
