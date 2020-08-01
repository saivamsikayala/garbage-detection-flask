import os, classifier, datetime
from flask import Flask, render_template, request
from forms import ImageForm
from PIL import Image

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CAFFE_MODEL = BASE_DIR + "/garbnet_fcn.caffemodel"
DEPLOY_FILE = BASE_DIR + "/deploy_garbnet.prototxt"
#MEAN = BASE_DIR + "/mean.binaryproto"
MEAN_FILE = BASE_DIR + "/garbnet_mean.binaryproto"
#LABELS_FILE = BASE_DIR + "/labels.txt"
LABELS_FILE = None
UPLOAD_FOLDER = BASE_DIR + "/uploads/"


app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/', methods=['GET', 'POST'])
def home():
	form = ImageForm()
	if request.method == 'POST':
		image_file = form.image.data
		extension = os.path.splitext(image_file.filename)[1]
		filepath = os.path.join(UPLOAD_FOLDER, \
                datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')) + extension
		image_file.save(filepath)
		#pre_process(filepath).save(filepath)
		sample = Image.open(filepath)
		image_files = []
		image_files.append(sample)
		#print(image_files)
		classifications = classifier.getPredictionsFor(
			caffemodel=CAFFE_MODEL, 
			deploy_file=DEPLOY_FILE, 
			image_files=image_files, 
			labels_file=LABELS_FILE,
			mean_file=MEAN_FILE, 
		)
		print(filepath)
		return render_template('show.html', classifications=classifications)
	else:
		return render_template('home.html')

if __name__== "__main__":
        app.run(host="0.0.0.0")
