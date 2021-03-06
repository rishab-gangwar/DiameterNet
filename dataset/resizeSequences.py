########################################################
## Nicolo Savioli, PhD student King's Collage London ##
########################################################

import h5py, os
import numpy as np
import cv2 
from   matplotlib import pyplot as plt
import copy 
import csv
import math




def resize_img(image,size):
    return cv2.resize(image, (size, size), interpolation = cv2.INTER_CUBIC)

def open_hdf5(filename):
     f         = h5py.File(filename, 'r')
     data      = np.asarray(f['data'])
     label     = np.asarray(f['label'])
     return  data,label 

def resizeImages(data,SizeImage):
    NewData = np.zeros((data.shape[0],data.shape[1],1,SizeImage,SizeImage))
    for patient in xrange(data.shape[0]):
        for seqs in xrange(data.shape[1]):
            NewData[patient][seqs][0] = resize_img(data[patient][seqs][0],SizeImage)
    return NewData 

def make_dir(path):
    if not os.path.exists(path):
       os.makedirs(path)

def saveDatasetHDF5(filename,data,label):
    f    = h5py.File(filename, 'w')
    dt   = h5py.special_dtype(vlen=bytes)
    dset = f.create_dataset('data', shape =data.shape,  dtype ='f4', data=data)
    dset = f.create_dataset('label',shape=label.shape, dtype ='f4', data=label)
    f.close() 


def ResizeData(dataPath,savePath,SizeImage):
    Data,Label        = open_hdf5(dataPath)
    ResizeData        = resizeImages(Data,SizeImage)
    saveDatasetHDF5(savePath,ResizeData,Label)

if __name__ == "__main__":

    ROOT       = "/home/ns14/Desktop/workspace/Projects/DATASETS/ultrasound/split"
    SizeImage  = 256
    # New dataset path. 
    resizePath = os.path.join(ROOT,"resize_dataset")
    # Risize dataset.
    make_dir(resizePath)
    # old paths 
    trianPath        = os.path.join(ROOT,"train.h5")
    testPath         = os.path.join(ROOT,"test.h5")
    validPath        = os.path.join(ROOT,"valid.h5")
    # new paths 
    ResizetrianPath  = os.path.join(resizePath,"train.h5")
    ResizetestPath   = os.path.join(resizePath,"test.h5")
    ResizevalidPath  = os.path.join(resizePath,"valid.h5")
    
    print("Open Train files ...")
   
    TrainData,TrainLabel = open_hdf5(trianPath)
    ResizeTrainData      = resizeImages(TrainData,SizeImage)
    
    print("Train Resize ...")
    ResizeData(trianPath,ResizetrianPath,SizeImage)

    print("Test Resize ...")
    ResizeData(testPath,ResizetestPath,SizeImage)
       
    print("Valid Reize ...")
    ResizeData(validPath,ResizevalidPath,SizeImage)

    print("\n Done!")
    




 
