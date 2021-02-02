# -*- coding: utf-8 -*-
"""tflite model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17853me_KkRWMfbTzr8LnbE0RK71P25vO
"""

from sklearn.metrics import recall_score,precision_score,f1_score,accuracy_score

from sklearn.metrics import classification_report, confusion_matrix

from sklearn import metrics

import time
import tflite_runtime.interpreter as tflite
import numpy as np

#import tensorflow_model_optimization as tfmot

def evaluate_model(interpreter):
  input_index0 = interpreter.get_input_details()[0]["index"]
  input_index1 = interpreter.get_input_details()[1]["index"]
  input_index2 = interpreter.get_input_details()[2]["index"]
  output_index = interpreter.get_output_details()[0]["index"]

  # Run predictions on ever y image in the "test" dataset.
  prediction_digits = []
  X_test3=np.load("X_test3.npy")
  X_test2=np.load("X_test2.npy")
  X_test=np.load("X_test.npy")
  y_test3=np.load("y_test3.npy")
  for i, test_image in enumerate(X_test3):
    if i % 1000 == 0:
      print('Evaluated on {n} results so far.'.format(n=i))

    test_image = np.expand_dims(test_image, axis=0).astype(np.float32)
    #print(test_image.shape)
    
    interpreter.set_tensor(input_index0, test_image)
    
    test_image1= X_test[i]

    test_image1 = np.expand_dims(test_image1, axis=0).astype(np.float32)
    #print(test_image1.shape)
    interpreter.set_tensor(input_index1, test_image1)

    #for k, test_image2 in enumerate(X_test2):
    test_image2 = X_test2[i]
    test_image2 = np.expand_dims(test_image2, axis=0).astype(np.float32)
    #print(test_image2.shape)
    interpreter.set_tensor(input_index2, test_image2)



    # Run inference.
    interpreter.invoke()

    # Post-processing: remove batch dimension and find the digit with highest
    # probability.
    output = interpreter.get_tensor(output_index)
    #a=output.to_numpy()
    # print(len(output))
    
    #digit = np.argmax(output()[0])
    
    #print(output)
    
    prediction_digits.append(output)
    

  print('\n')
  #print(prediction_digits)
  for i in range(0,len(prediction_digits)):
    if prediction_digits[i]>=0.50:
        prediction_digits[i]=1
    else:
        prediction_digits[i]=0
  #print(prediction_digits)
  print(confusion_matrix(y_test3, prediction_digits))
  print(classification_report(y_test3, prediction_digits))
  # Compare prediction results with ground truth labels to calculate accuracy.
  prediction_digits = np.array(prediction_digits)
  accuracy = (prediction_digits == y_test3).mean()
  return accuracy

start_time= time.time()
interpreter = tflite.Interpreter("tfliteModel.tflite")
interpreter.allocate_tensors()

test_accuracy = evaluate_model(interpreter)
end_time= time.time()
print('Pruned and quantized TFLite test_accuracy:', test_accuracy)

print("time needed:", end_time-start_time)
