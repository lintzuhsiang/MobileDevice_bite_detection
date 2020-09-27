# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow.compat.v1 as tf
# import tf.compat.v1.keras.utils.CustomObjectScope
# from tensorflow.keras import backend as K

# tf.disable_eager_execution()
import argparse
parser = argparse.ArgumentParser(description='set input arguments')
parser.add_argument(
    '-model',
    dest='model',
    required=True,
    help='Model to convert')

args = parser.parse_args()
keras_model = args.model

converter = tf.lite.TFLiteConverter
converter = converter.from_keras_model_file(keras_model)
# converter.allow_custom_ops=True
tflite_model = converter.convert()
open(keras_model.split(".")[0]+".tflite", "wb").write(tflite_model)


# def relu6(x):
#         return K.relu(x, max_value=6)

# with CustomObjectScope({'relu6': relu6}):
#     tflite_model = tf.contrib.lite.TFLiteConverter.from_keras_model_file(keras_model).convert()
#     with open('./model/model_customerScope.tflite', 'wb') as f:
#         f.write(tflite_model)