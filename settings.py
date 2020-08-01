BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CAFFE_MODEL = BASE_DIR + "/garbnet_fcn.caffemodel"
DEPLOY_FILE = BASE_DIR + "/deploy_garbnet.prototxt"
#MEAN = BASE_DIR + "/mean.binaryproto"
MEAN_FILE = BASE_DIR + "/garbnet_mean.binaryproto"
#LABELS_FILE = BASE_DIR + "/labels.txt"
LABELS_FILE = None
UPLOAD_FOLDER = BASE_DIR + "/uploads/"
