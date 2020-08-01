from boto3 import session
import uuid
import io

class S3utils():
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

    def __init__(self):
        self._session = session.Session()
        self._client = self._session.client('s3',
            region_name=S3utils.AWS_S3_REGION_NAME,
            endpoint_url=S3utils.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=S3utils.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=S3utils.AWS_SECRET_ACCESS_KEY)

    def getfilename(self):
        return f"smartbins/{str(uuid.uuid4())}.jpg"

    def toByteArray(self, image):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format='JPG')
        return imgByteArr.getvalue()

    def upload(self, pilimage):
        filename = self.getfilename()
        data = self.toByteArray(pilimage)
        self._client.put_object(ACL='public_read', Bucket='SIH2020', Key=filename, Body=data)
        return f'{S3utils.AWS_S3_ENDPOINT_URL}/{S3utils.AWS_STORAGE_BUCKET_NAME}/{filename}'


    def delete(self, filename):
        return self._client.delete_object(Bucket='SIH2020', Key=filename)


S3Connection = S3utils()