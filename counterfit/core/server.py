from counterfit.core.state import CFState
from counterfit.core.run_scan_utils import get_printable_batch, printable_numpy

import threading
import numpy as np
from flask import Flask
from flask import request, jsonify
from werkzeug.serving import make_server
from typing import Any, List

class ServerThread(threading.Thread):
    """ Run the Flask app in a separate thread in the background"""
    # From https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
    def __init__(self, app, port=None):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown_thread(self):
        self.srv.shutdown()


class Server():
   """ Singleton server instance"""
   __instance = None
   
   class ServerRunningException(Exception):
       # Constructor
       def __init__(self, port):
           self.port = port

       # __str__ is to print() the port
       def __str__(self):
           return(repr(self.port))

   class ServerNotRunningException(Exception):
       #Placeholder exception
       pass 

   def __init__(self, port):
       if Server.__instance != None:
           raise Server.ServerRunningException(Server.get_instance().port)
       else:
           self.port=port
           self.app=self.__app_factory()
           self.thread=ServerThread(self.app, port=self.port)
           Server.__instance = self
   
   def __app_factory(self):
       """ Create the flask app that exposes the api"""
       app = Flask(__name__)
       
       @app.route("/predict")
       def predict_endpoint():
           index = request.args.get('index')
           args = {'index':index}
           json = self.__predict(args)
           return jsonify(json)
       return app

   @staticmethod 
   def get_instance(port=None):
       # Return the server if requested
       if port is None:
           if Server.__instance == None:
               raise Server.ServerNotRunningException()
           else:
               return Server.__instance
       # Create the instance if necessary
       try:
           Server(port)
       except:
           raise
       return Server.__instance

   def shutdown(self):
       self.thread.shutdown_thread()
       Server.__instance=None

   def serve(self):
       self.thread.start()
       
   def __run_flask(self, port):
       self.app.run(port=self.port)
   def __predict(self, args):
       """ Clone of the command do_predict function which could not be called directly"""
       if CFState.get_instance().active_target is None:
           print("\n [!] must first `interact` with a target.\n")
           return
       else:
           target = CFState.get_instance().active_target
       if 'index' in args:  # default behavior
           sample_index = int(args['index'])
           samples = set_attack_samples(target, sample_index)
       elif target.active_attack is not None and target.active_attack.sample_index is not None:
           sample_index = target.active_attack.sample_index
           samples = set_attack_samples(target, sample_index)        
       else:
           sample_index = random.randint(0, len(target.X) - 1)
           samples = set_attack_samples(target, sample_index)

       result = target._submit(samples)
       str(target.model_output_classes).replace(',', '')

       if not hasattr(sample_index, "__iter__"):
           sample_index = [sample_index]
       samples_str = get_printable_batch(target, samples)
       results_str = printable_numpy(result)
       
       return {"sample_index": sample_index,"results": results_str,"samples": samples_str}


def set_attack_samples(target, sample_index=0):
    # Duplicated as commands could not be imported as a module
    if hasattr(sample_index, "__iter__"):
        # (unused) multiple index
        out = np.array([target.X[i] for i in sample_index])
        batch_shape = (-1,) + target.model_input_shape
    elif type(target.X[sample_index]) is str:
        # array of strings (textattack)
        out = np.array(target.X[sample_index])
        batch_shape = (-1,)
    else:
        # array of arrays (art)
        out = np.atleast_2d(target.X[sample_index])
        batch_shape = (-1,) + target.model_input_shape

    return out.reshape(batch_shape)
