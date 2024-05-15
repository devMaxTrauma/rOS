class Kernel:
    rKeyEngine = None
    model = None
    model = None
    import tensorflow as tf
    import cv2 as cv
    from rCore.rKey import rKeyEngine
    import numpy as np


    def __init__(self):
        self._boot()

    def _boot(self):
        print("Booting rKernel...")
        self.load_rKeyEngine()
        self.load_model()


    def load_rKeyEngine(self):
        self.rKeyEngine = self.rKeyEngine.Manager()


    def load_model(self):
        print("Loading model...")
        import os
        os.chdir(os.path.dirname(__file__))
        self.model = self.tf.lite.Interpreter(model_path='model.tflite')
        self.model.allocate_tensors()
        # test model
        input_details = self.model.get_input_details()
        output_details = self.model.get_output_details()
        print(input_details)
        print(output_details)
        print("Model loaded")
