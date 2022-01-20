import os
import tensorflow as tf
from tensorflow import keras as K
import numpy as np

from counterfit.core.targets import Target

# for ART
tf.compat.v1.disable_eager_execution()


class DigitKeras(Target):
    target_data_type = "image"
    target_name = "digits_keras"
    target_endpoint = "mnist_model.h5"
    target_input_shape = (28, 28, 1)
    target_output_classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    target_classifier = "keras"
    X = []

    def load(self):
        if not os.path.isfile(self.fullpath(self.target_endpoint)):
            print("[!] Model file not found!")
            self.create_model()
        else:
            self.model = K.models.load_model(
                self.fullpath(self.target_endpoint))
        (train_x, train_y), (test_x, test_y) = K.datasets.mnist.load_data()

        self.X = test_x.astype(np.float32) / 255.  # float type [0,1]
        # self.X = self.X.reshape(10_000, 28, 28, 1)

    def create_model(self):
        # 0. get started
        print(
            f"    - Training new modeil. Begin MNIST using Keras {K.__version__}")
        np.random.seed(1)
        tf.random.set_seed(1)

        # 1. load data
        print("     - Loading train and test data ")
        (train_x, train_y), \
            (test_x, test_y) = K.datasets.mnist.load_data()
        train_x = train_x.reshape(60_000, 28, 28, 1)
        test_x = test_x.reshape(10_000, 28, 28, 1)
        train_x = train_x.astype(np.float32)
        test_x = test_x.astype(np.float32)
        train_x /= 255
        test_x /= 255
        train_y = K.utils.to_categorical(train_y, 10)
        test_y = K.utils.to_categorical(test_y, 10)

        # self.X = [test_x]
        self.test_x = test_x

        # 2. define model
        print(
            "   - Creating network with two Convolution, two Dropout, two Dense layers ")
        g_init = K.initializers.glorot_uniform(seed=1)
        opt = K.optimizers.Adam(learning_rate=0.01)
        x = K.layers.Input(shape=(28, 28, 1))
        con1 = K.layers.Conv2D(
            filters=32,
            kernel_size=(3, 3),
            kernel_initializer=g_init,
            activation='relu',
            padding='valid')(x)

        con2 = K.layers.Conv2D(
            filters=64,
            kernel_size=(3, 3),
            kernel_initializer=g_init,
            activation='relu',
            padding='valid')(con1)

        mp1 = K.layers.MaxPooling2D(pool_size=(2, 2))(con2)
        do1 = K.layers.Dropout(0.25)(mp1)
        z = K.layers.Flatten()(do1)
        fc1 = K.layers.Dense(
            units=128,
            kernel_initializer=g_init,
            activation='relu')(z)

        do2 = K.layers.Dropout(0.5)(fc1)
        fc2 = K.layers.Dense(
            units=10,
            kernel_initializer=g_init,
            activation='softmax')(do2)

        model = K.models.Model(x, fc2)
        model.compile(
            loss='categorical_crossentropy',
            optimizer=opt,
            metrics=['accuracy'],
            run_eagerly=False)

        # 3. train model
        batch_size = 100
        max_epochs = 2
        print(f"    - Starting training with batch size {batch_size}")
        model.fit(
            train_x,
            train_y,
            batch_size=batch_size,
            epochs=max_epochs,
            verbose=1)
        print("     - Training finished ")

        # 4. evaluate model
        evaluation = model.evaluate(
            test_x,
            test_y,
            verbose=0)

        loss = evaluation[0]
        acc = evaluation[1] * 100
        print(f"    - Test data: loss = {loss}, accuracy = {acc}")

        # 5. save model
        print("     - Saving MNIST model to disk ")
        model.save(self.fullpath("mnist_model.h5"))
        self.model = model

        print("[+] Done!")

    def predict(self, x):
        x = (x.reshape(-1, 28, 28, 1) * 255).astype(np.uint8).astype('float32')/255.  # accept as an image
        pred_probs = self.model.predict(x)
        return(pred_probs)
