from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import sys
import time
import wget
import numpy as np
import mysql.connector
import argparse
import tensorflow as tf
import os


keyword="love"
param1='%'+keyword+'%'

def createFolde(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error creating directory :",directory)

folderpath='/Users/kaumadisamarathunga/PycharmProjects/GetTWEETSnew/sentimentAnalysis/images/'+keyword+'/'
print("Folder path : ",folderpath)
createFolde(folderpath)

# open a database connection
connection = mysql.connector.connect (host = "localhost", user = "root", passwd = "root1234", db = "trend_analysis")
# prepare a cursor object using cursor() method
cursor = connection.cursor ()
# execute the SQL query using execute() method.
cursor.execute("select * from testData where tweetText like %s",(param1,))
# fetch all of the rows from the query
data = cursor.fetchall ()

for row in data :
    if(row[3]!='none'):
        xo=row[3]
        file_path = folderpath
        wget.download(xo,file_path)

# close the cursor object
cursor.close ()
# close the connection
connection.close ()
# exit the program
negsentiScore = 0
neusentiScore = 0
possentiScore = 0
negtweetCount = 0
neutweetCount = 0
postweetCount = 0
noOfimages=0
path = folderpath
files = os.listdir(path)
for name in files:
    #print(name)
    file_name = folderpath + "/" + name
    print(file_name)
    noOfimages=noOfimages+1
    # file_name="/Users/kaumadisamarathunga/PycharmProjects/imagescore/tensorflow-for-poets-2/images/test43.jpg"
    model_file = "/Users/kaumadisamarathunga/PycharmProjects/GetTWEETSnew/sentimentAnalysis/tf_files/retrained_graph.pb"
    label_file = "/Users/kaumadisamarathunga/PycharmProjects/GetTWEETSnew/sentimentAnalysis/tf_files/retrained_labels.txt"
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
    input_layer = "input"
    output_layer = "final_result"


    def load_graph(model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)

        return graph


    def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
                                    input_mean=0, input_std=255):
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)
        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(file_reader, channels=3,
                                               name='png_reader')
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                          name='gif_reader'))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
        else:
            image_reader = tf.image.decode_jpeg(file_reader, channels=3,
                                                name='jpeg_reader')
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0);
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)

        return result


    def load_labels(label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label


    graph = load_graph(model_file)
    t = read_tensor_from_image_file(file_name,
                                    input_height=input_height,
                                    input_width=input_width,
                                    input_mean=input_mean,
                                    input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);

    # print(t)
    with tf.Session(graph=graph) as sess:
        start = time.time()
        results = sess.run(output_operation.outputs[0],
                           {input_operation.outputs[0]: t})
        end = time.time()
    results = np.squeeze(results)
    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)

    #print('\nEvaluation time (1-image): {:.3f}s\n'.format(end - start))
    template = "{} (score={:0.5f})"

    max = 0
    maxCategory = ""
    for i in top_k:
        #print(template.format(labels[i], results[i]))
        # print (results[i])
        if results[i] > max:
            max = results[i]
            maxCategory = labels[i]

    print("Image category: ", maxCategory, "And sentiment score : ", max)

    if maxCategory == "happy" or maxCategory == "love":
        possentiScore=possentiScore+max
        postweetCount=postweetCount+1
    elif maxCategory == "sad" or maxCategory == "angry":
        imagesentiScore = (-1 * max)
        negtweetCount=negtweetCount+1
        #print(imagesentiScore)
        negsentiScore=negsentiScore+imagesentiScore
    elif maxCategory == "neutral":
        neusentiScore=neusentiScore+0
        neutweetCount=neutweetCount+1

print(noOfimages)
print("Total positive Text Sentiment Score: ", possentiScore)
print("Total neutral Text Sentiment Score: ", neusentiScore)
print("Total negative Text Sentiment Score: ", negsentiScore)
print()

print("Positive Tweet count: ", postweetCount)
print("Neutral Tweet count: ", neutweetCount)
print("Negative Tweet count: ", negtweetCount)
print()

if(noOfimages>0):
    overallnew = (possentiScore + neusentiScore + negsentiScore) / (postweetCount + neutweetCount + negtweetCount)
    overall = round(overallnew, 3)
    print("Overall Text sentiment score of the Trend:", overall)
else:
    print("No tweets available with images.")
    overall=0
    print("Overall Text sentiment score of the Trend:", overall)

