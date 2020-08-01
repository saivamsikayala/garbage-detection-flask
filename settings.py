import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CAFFE_MODEL = BASE_DIR + "/garbnet_fcn.caffemodel"
DEPLOY_FILE = BASE_DIR + "/deploy_garbnet.prototxt"
#MEAN = BASE_DIR + "/mean.binaryproto"
MEAN_FILE = BASE_DIR + "/garbnet_mean.binaryproto"
#LABELS_FILE = BASE_DIR + "/labels.txt"
LABELS_FILE = None
UPLOAD_FOLDER = BASE_DIR + "/uploads/"

AWS_ACCESS_KEY_ID = 'XUGWG5ASJKCLWYSP6FKJ'
AWS_SECRET_ACCESS_KEY = 'T6iOjcZdINwV0mDFlOd3rOcb8asYedLxml5qlORvJPI'
AWS_STORAGE_BUCKET_NAME = 'SIH2020'
AWS_S3_ENDPOINT_URL = 'https://vitb.sgp1.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_REGION_NAME = 'sgp1'
SPACES_IMAGE_FOLDER = 'smartbins'
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False  # since we have public read



