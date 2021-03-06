from __future__ import division
import os
import time
import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras import backend
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import mnist

from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from tensorflow.keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D
from keras.layers.advanced_activations import LeakyReLU 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.utils.generic_utils import get_custom_objects

from ops import *
from utils import *
#            ___________
#           /           \
#          / MAIN  MODEL \
#         /_______________\        

# MNIST Models ######################################################################
        
def mnist_model_no1(x,batch_size, is_training=True, reuse=False):

    with tf.compat.v1.variable_scope("main_model", reuse=reuse):    

        net = lrelu(coinv2d(x, 64, 4, 4, 2, 2, name='mm_conv1'))
        net = lrelu(bn(coinv2d(net, 128, 4, 4, 2, 2, name='mm_conv2'), is_training=is_training, scope='mm_bn2'))
        net = tf.reshape(net, [batch_size, -1])
        net = lrelu(bn(linear(net, 1024, scope='mm_fc3'), is_training=is_training, scope='mm_bn3'))
        out_logit = linear(net, 10, scope='mm_fc4')
        out = tf.nn.softmax(out_logit)

        return out, out_logit

# CIFAR-10 Models ####################################################################

def cifar10_model_no1(x,batch_size, is_training=True, reuse=False):
# Source: https://www.kaggle.com/faressayah/cifar-10-image-classification-using-cnns-88
    with tf.compat.v1.variable_scope("main_model", reuse=reuse):    

        net = relu(bn(coinv2d(x, 32, 3, 3, name='mm_conv1'), is_training=is_training, scope='mm_bn1'))
        net = relu(bn(coinv2d(x, 32, 3, 3, name='mm_conv2'), is_training=is_training, scope='mm_bn2'))
        net = tf.compat.v1.nn.max_pool(net, 2, 2, padding='SAME')
        net = tf.compat.v1.nn.dropout(net, rate=0.25)
        net = relu(bn(coinv2d(x, 64, 3, 3, name='mm_conv3'), is_training=is_training, scope='mm_bn3'))
        net = relu(bn(coinv2d(x, 64, 3, 3, name='mm_conv4'), is_training=is_training, scope='mm_bn4'))
        net = tf.compat.v1.nn.max_pool(net, 2, 2, padding='SAME')
        net = tf.compat.v1.nn.dropout(net, rate=0.25)
        net = relu(bn(coinv2d(x, 128, 3, 3, name='mm_conv5'), is_training=is_training, scope='mm_bn5'))
        net = relu(bn(coinv2d(x, 128, 3, 3, name='mm_conv6'), is_training=is_training, scope='mm_bn6'))
        net = tf.compat.v1.nn.max_pool(net, 2, 2, padding='SAME')
        net = tf.compat.v1.nn.dropout(net, rate=0.25)

        net = tf.reshape(net, [batch_size, -1])
        net = tf.compat.v1.nn.dropout(net, rate=0.20)
        net = relu(linear(net, 128, scope='mm_fc2'))
        out_logit = linear(net, 10, scope='mm_fc3')
        net = tf.compat.v1.nn.dropout(net, rate=0.25)
        out = tf.nn.softmax(out_logit)

        return out, out_logit

