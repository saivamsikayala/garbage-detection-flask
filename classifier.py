
import os
from pylab import *
import sys
from PIL import Image
import numpy as np
import cv2
import argparse
import time
from google.protobuf import text_format
import numpy as np
from S3utils import S3Connection
import caffe
# def gatherImages(folder,imageNames=None):
#     images = []
#     names = []
#     files = os.listdir(folder)
#     total = len(files)
#     print('Total %d images in folder %s' % (total,folder))
#     for i in os.listdir(folder):
#         try:
#             if imageNames is None or i in imageNames:
#                 example_image = folder+'/'+i
#                 input_image = Image.open(example_image)
#                 images.append(input_image)
#                 names.append(i)
#         except:
#             pass

#     return images,names

def resizeForFCN(image,size):
    #image = Image.open(image)
    w,h = image.size
    #print(w,h)
    if w<h:
        return image.resize((int(227*size),int((227*h*size)/w)))
    else:
        return image.resize((int((227*w*size)/h),int(227*size)))
    
def getSegmentedImage(test_image, probMap,thresh):
    kernel = np.ones((6,6),np.uint8)
    wt,ht = test_image.size
    out_bn = np.zeros((ht,wt),dtype=uint8)
    
    for h in range(probMap.shape[0]):
                for k in range(probMap.shape[1]):
                    if probMap[h,k] > thresh:
                        x1 = h*62 #stride 2 at fc6_gb_conv equivalent to 62 pixels stride in input
                        y1 = k*62
                        for hoff in range(x1,227+x1):
                            if hoff < out_bn.shape[0]:
                                for koff in range(y1,227+y1):
                                    if koff < out_bn.shape[1]:
                                        out_bn[hoff,koff] = 255
    edge = cv2.Canny(out_bn,200,250)
    box = cv2.dilate(edge,kernel,iterations = 3)
    
    or_im_ar = np.array(test_image)
    or_im_ar[:,:,1] = (or_im_ar[:,:,1] | box)
    or_im_ar[:,:,2] = or_im_ar[:,:,2] * box + or_im_ar[:,:,2]
    or_im_ar[:,:,0] = or_im_ar[:,:,0] * box + or_im_ar[:,:,0]
    
    return Image.fromarray(or_im_ar)
    
    
def getPredictionsFor(image_files,net, mean):
    size = 4
    thresh = 0.999
    output_folder = 'static'

    classifications = []
    #print(len(image_files))
    for i in range(len(image_files)):
            test_image = resizeForFCN(image_files[i],size)
            #print(test_image)
            in_ = np.array(test_image,dtype = np.float32)
            #print(in_)
            in_ = in_[:,:,::-1]
            in_ -= np.array(mean.mean(1).mean(1))
            in_ = in_.transpose((2,0,1))

            net.blobs['data'].reshape(1,*in_.shape)
            net.blobs['data'].data[...] = in_
            net.forward()
            
            probMap =net.blobs['prob'].data[0,1]
            #print(names[i]+'...',)
            if len(np.where(probMap>thresh)[0]) > 0:
                classifications.append("Garbage!")
                #print('Garbage!')
            else:
                classifications.append("Not Garbage!")
                #print('Not Garbage!')
            
            out_ = getSegmentedImage(test_image, probMap,thresh)
            filepath = os.path.join(output_folder,
                                    datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')) + '.jpg'
            out_.save(output_folder + '/output_image.jpg')
            
    return {'classification': classifications, 'image': S3Connection.upload(filepath)}

def toByteArray(self, image):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format='JPEG')
        return imgByteArr.getvalue()

def main():
    parser = argparse.ArgumentParser(description="Garbage det model")
    parser.add_argument('caffemodel', help="Path to .caffemodel")
    parser.add_argument('deploy_file', help="Path to deploy file")
    parser.add_argument('-m','--mean', help="Path to mean file")
    parser.add_argument('-i','--image', help="Path to image")
    parser.add_argument('-l','--labels',help="Path to labels")
    args = vars(parser.parse_args())
    images = []
    #print(args['image'])
    sample = Image.open(args['image'])
    #print(500000000000000)
    images.append(sample)
    getPredictionsFor(args['caffemodel'],args['deploy_file'],images,args['labels'],args['mean'])

#main()
#specify 'input' folder containing images for prediction
#images,names = gatherImages('input')
#specify 'output' folder to store segmented predictions
#getPredictionsFor(images,names,4,0.999,'output')
