# imports
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from counterfit import Counterfit
from counterfit.core import optimize

from targets import CreditFraud
from targets import DigitKeras
from targets import Digits

import numpy as np

import matplotlib.pyplot as plt

attacks = ["mi_face"]
target = Digits()
target.load()

for attack in attacks: 
    cfattack = Counterfit.build_attack(target, attack)
    Counterfit.run_attack(cfattack)


plt.figure(figsize=(15,15))
for i in range(10):
    plt.subplot(5, 5, i + 1)
    plt.imshow( (np.reshape(cfattack.results[0+i,], (28, 28))), cmap=plt.cm.gray_r)

plt.show()
print()

# import tensorflow as tf
# tf.compat.v1.disable_eager_execution()
# import warnings
# warnings.filterwarnings('ignore')
# import keras.backend as k
# from keras.models import Sequential
# from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
# import numpy as np
# from numpy.random import seed
# seed(123)

# from art.estimators.classification import KerasClassifier
# from art.attacks.inference.model_inversion.mi_face import MIFace
# from art.utils import load_dataset



# # Read MNIST dataset
# (x_train, y_train), (x_test, y_test), min_, max_ = load_dataset(str('mnist'))

# # create standard CNN in Keras and wrap with ART KerasClassifier:
# def cnn_mnist(input_shape, min_val, max_val):
  
#     model = Sequential()
#     model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Conv2D(64, (3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.25))
#     model.add(Flatten())
#     model.add(Dense(128, activation='relu'))
#     model.add(Dense(10, activation='softmax'))

#     model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#     classifier = KerasClassifier(clip_values=(min_val, max_val), 
#                                 model=model, use_logits=False)
#     return classifier

# num_epochs = 1

# # Construct and train a convolutional neural network
# classifier = cnn_mnist(x_train.shape[1:], min_, max_)
# classifier.fit(x_train, y_train, nb_epochs=num_epochs, batch_size=128)

# attack = MIFace(classifier, max_iter=10000, threshold=1.) 

# y = np.arange(10)

# x_init_white = np.zeros((10, 28, 28, 1))
# x_init_grey = np.zeros((10, 28, 28, 1)) + 0.5
# x_init_black = np.ones((10, 28, 28, 1))
# x_init_random = np.random.uniform(0, 1, (10, 28, 28, 1))
# x_init_average = np.zeros((10, 28, 28, 1)) + np.mean(x_test, axis=0)

# class_gradient = classifier.class_gradient(x_init_grey, y)
# class_gradient = np.reshape(class_gradient, (10, 28*28))
# class_gradient_max = np.max(class_gradient, axis=1)

# # Now we run the attack:
# x_infer_from_average = attack.infer(x_init_average, y)