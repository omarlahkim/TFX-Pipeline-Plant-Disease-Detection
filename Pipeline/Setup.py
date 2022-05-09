import os
import tensorflow as tf
from tfx.components import ImportExampleGen
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import io

base_dir = os.getcwd()
data_dir = os.path.join(base_dir, "New Plant Diseases Dataset")

DataDirectory = os.listdir(data_dir)
tfrecord_filename = 'Data/Dataset.tfrecord'
DataDirectory.sort()
print(DataDirectory)
Data_Labels = {}
count = 0
Labels = []
for f in DataDirectory:
    if f != ".DS_Store":
        Data_Labels[f] = count
        Labels.append(f)
        count += 1


print(len(Data_Labels))
print(Labels)

#Data_Labels = {"Strawberry___healthy": 0, "Grape___Black_rot": 1, "Potato___Early_blight": 2, "Blueberry___healthy": 3, "Corn_(maize)___healthy": 4, "Tomato___Target_Spot": 5, ".DS_Store": 6, "Peach___healthy": 7, "Potato___Late_blight": 8, "Tomato___Late_blight": 9, "Tomato___Tomato_mosaic_virus": 10, "Pepper,_bell___healthy": 11, "Orange___Haunglongbing_(Citrus_greening)": 12, "Tomato___Leaf_Mold": 13, "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": 14, "Cherry_(including_sour)___Powdery_mildew": 15, "Apple___Cedar_apple_rust": 16, "Tomato___Bacterial_spot": 17, "Grape___healthy": 18, "Tomato___Early_blight": 19, "Corn_(maize)___Common_rust_": 20, "Grape___Esca_(Black_Measles)": 21, "Raspberry___healthy": 22, "Tomato___healthy": 23, "Cherry_(including_sour)___healthy": 24, "Tomato___Tomato_Yellow_Leaf_Curl_Virus": 25, "Apple___Apple_scab": 26, "Corn_(maize)___Northern_Leaf_Blight": 27, "Tomato___Spider_mites Two-spotted_spider_mite": 28, "Peach___Bacterial_spot": 29, "Pepper,_bell___Bacterial_spot": 30, "Tomato___Septoria_leaf_spot": 31, "Squash___Powdery_mildew": 32, "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": 33, "Apple___Black_rot": 34, "Apple___healthy": 35, "Strawberry___Leaf_scorch": 36, "Potato___healthy": 37, "Soybean___healthy": 38}

def generate_label_from_path(image_path):
    return Data_Labels[image_path]
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
def Dataset_to_TFRECORD():
    with tf.io.TFRecordWriter(tfrecord_filename) as writer:
        for folder in DataDirectory:
            if folder != ".DS_Store":
                DataFolderDirectory = os.listdir(os.path.join(data_dir, folder))
                counter = 0
                print(folder)
                print("Label: "+ str(_int64_feature(generate_label_from_path(folder))))
                for img_file in DataFolderDirectory:
                    image_path = os.path.join(os.path.join(data_dir, folder), img_file)
                    try:
                        if counter == 10:
                            break
                        raw_file = tf.io.read_file(image_path)
                    except FileNotFoundError:
                        print("File {} could not be found".format(image_path))
                        continue
                    example = tf.train.Example(features=tf.train.Features(feature={
                        'image_raw': _bytes_feature(raw_file.numpy()),
                        'label': _int64_feature(generate_label_from_path(folder))
                    }))
                    if len(str(_bytes_feature(raw_file.numpy()))) > 27:
                        writer.write(example.SerializeToString())
                        print(counter)
                        counter +=1
                        print(len(str(_bytes_feature(raw_file.numpy()))))
                    else:
                        print(len(str(_bytes_feature(raw_file.numpy()))))


Dataset_to_TFRECORD()

