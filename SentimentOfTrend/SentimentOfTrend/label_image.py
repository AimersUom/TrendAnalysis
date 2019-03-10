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

def imagescore(key):

    words=key

    sentiscorenew=[]
    for keyword in words:
        param1='%'+keyword+'%'

        #create the directory from the keword name
        def createFolde(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print("Error creating directory :",directory)

        folderpath='/Users/kaumadisamarathunga/PycharmProjects/sentimentOfTrend/sentimentAnalysis/images/'+keyword+'/'
        print("Folder path : ",folderpath)
        createFolde(folderpath)

        # open a database connection
        connection = mysql.connector.connect (host = "localhost", user = "root", passwd = "root1234", db = "trend_analysis")
        # prepare a cursor object using cursor() method
        cursor = connection.cursor ()
        # execute the SQL query using execute() method.
        cursor.execute("select * from senti_database where tweetText like %s",(param1,))
        # fetch all of the rows from the query
        data = cursor.fetchall ()

        for row in data :

            if(row[3]!='no'):
                xo=row[3]
                #print(row[3])
                file_path = folderpath
                #download all the images realated to the keyword to file_path
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
            #print(file_name)
            noOfimages=noOfimages+1

            model_file = "/Users/kaumadisamarathunga/PycharmProjects/sentimentOfTrend/sentimentAnalysis/tf_files/retrained_graph.pb"
            label_file = "/Users/kaumadisamarathunga/PycharmProjects/sentimentOfTrend/sentimentAnalysis/tf_files/retrained_labels.txt"
            input_height = 224
            input_width = 224
            input_mean = 128
            input_std = 128
            input_layer = "input"
            output_layer = "final_result"


            def load_graph(model_file):
                #graph create your own computation and pass to tensorflow
                graph = tf.Graph()
                #A Graph contains a set of tf.Operation objects, which represent units of computation
                graph_def = tf.GraphDef()

                with open(model_file, "rb") as f:
                    #read the modelfile
                    graph_def.ParseFromString(f.read())
                with graph.as_default():
                    #The serialized GraphDef can be imported into another Graph
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

                #convert to operation support datatype tf.float32: 32-bit single-precision floating-point.
                float_caster = tf.cast(image_reader, tf.float32)
                #print(float_caster)
                #The dimension index axis starts at zero
                dims_expander = tf.expand_dims(float_caster, 0);

                #Resize image to size using bilinear interpolation
                resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
                normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])

                # Launch the graph in a session.
                sess = tf.Session()
                ## Evaluate the tensor
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

            #Returns the Operation with the given name
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
            posresult=0
            negresult=0
            neuresult=0

            for i in top_k:
                print("Please Wait......")
                if labels[i]=='happy' or labels[i]=='love':
                    posresult=posresult + results[i]
                elif labels[i]=='sad' or labels[i]=='angry':
                    negresult=negresult + results[i]
                elif labels[i]=='neutral':
                    neuresult=results[i]

            #calculate the overall sentiment score of the image
            negresult=( -1 * negresult)
            Totalscore=posresult + negresult

            if Totalscore>0:
                possentiScore=possentiScore+Totalscore
                postweetCount=postweetCount+1
            elif Totalscore ==0:
                neusentiScore=neusentiScore+Totalscore
                neutweetCount=neutweetCount+1
            elif Totalscore < 0:
                negsentiScore=negsentiScore+Totalscore
                negtweetCount = negtweetCount + 1


        def printAllImage():
            print(noOfimages)
            print("Total positive Image Sentiment Score: ", possentiScore)
            print("Total neutral Image Sentiment Score: ", neusentiScore)
            print("Total negative Image Sentiment Score: ", negsentiScore)
            print()

            print("Positive Image Tweet count: ", postweetCount)
            print("Neutral Image Tweet count: ", neutweetCount)
            print("Negative Image Tweet count: ", negtweetCount)
            print()
            return 'Successful'

        if(noOfimages>0):
            overallnew = (possentiScore + neusentiScore + negsentiScore) / (postweetCount + neutweetCount + negtweetCount)
            overall = round(overallnew, 3)
            sentiscorenew.append(overall)
        else:
            print("No tweets available with images.")


        #print(printAllImage())
    items=len(sentiscorenew)

    overall2=0
    for score in sentiscorenew:
        overall2=overall2+score

    #calculate the overall image sentiment score of the trend
    if(noOfimages>0):
        overall2=(overall2/items)
        overall2=round(overall2,4)
        print("Overall Image sentiment score of the Trend:", overall2)
    return overall2




