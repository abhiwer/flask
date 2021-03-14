
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np
import warnings
import cv2
from cv2 import *
import os

warnings.filterwarnings('ignore')

import tensorflow as tf

from tensorflow.python.tools import module_util as _module_util
from tensorflow.python.eager import context
from tensorflow.core.framework import function_pb2

from google.protobuf import descriptor as _descriptor

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def customvision():

    graph_def = tf.compat.v1.GraphDef()
    filename = "model.pb"
    with tf.compat.v2.io.gfile.GFile(filename, 'rb') as f:
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


    sess = tf.compat.v1.Session()

    input_ = sess.graph.get_tensor_by_name('image_tensor:0')

    output_1 = sess.graph.get_tensor_by_name('detected_scores:0')
    output_2 = sess.graph.get_tensor_by_name('detected_classes:0')
    output_3 = sess.graph.get_tensor_by_name('detected_boxes:0')

    folder = "static\download"

    img = load_images_from_folder(folder)

    plt.figure(figsize=(10,10))

    label_dict = {0: "Biological_element",
                 1: "Blockage",
                 2:"crack"}


    folder_name = "static\predicted"


    font = cv2.FONT_HERSHEY_SIMPLEX
    #fig, ax = plt.subplots(figsize=(20,20))
    i=1
    for x in img:
        x = cv2.resize(x, (320,320))
        ans_1, ans_2, ans_3 = sess.run([output_1,output_2, output_3], feed_dict={input_ : [x]})
        x1,y1,x2,y2 = ans_3[np.argmax(ans_1)]*320
        lx,ly = x1,y1
        if x1 < 50 :
            lx = 50
        if y1 < 100 : 
            ly = 100 
        if x1 > 300 :
            lx = 300
        if y1 > 300 :
            ly = 300
        bbox = cv2.rectangle(x, (x1, y1), (x2, y2), (255,0,0), 2)
        label = label_dict[int(ans_2[np.argmax(ans_1)])]
        cv2.putText(bbox,str(label), (lx,ly), font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
        #fig.add_subplot(len(img)/2,len(img)/2,i)
        #plt.subplot(len(img)/4,len(img)/4,i)
        i=i+1
        #plt.imshow(bbox)
        cv2.imwrite( folder_name + "/" + str(i-1) + ".jpg", bbox)
    #plt.show()


customvision()

