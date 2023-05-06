from flask import Flask, Response, request
from flask_cors import CORS
import logging
import json
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)




class API:
    '''
    Handles communications between the frontend
    '''
    def __init__(
            self,
            runner = None,
            port : int = 8080
        ):
        self.runner = runner
        self.app = Flask(__name__)
        self.cors = CORS(self.app)
        self.port = port
        self.add_endpoint('/monitor/add', 'add_monitor', self.add_monitor, methods=['POST'])
        self.add_endpoint('/monitor/edit', 'edit_monitor', self.edit_monitor, methods=['PUT'])
        self.add_endpoint('/monitor/remove', 'remove_monitor', self.remove_monitor, methods=['DELETE'])
        self.add_endpoint('/monitor/info', 'info_monitor', self.info_monitor, methods=['GET'])

    def spawn_process(self):
        '''
        Creates a new thread for the api to run in.

        Returns:
        - thread : threading.Thread - the thread that is created
        '''
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
        return thread

    def run(self):
        '''
        Runs the api
        '''
        self.app.run(
                host='0.0.0.0',
                port=self.port,
                debug=False,
                use_reloader=False
        )

    def add_endpoint(
                self,
                endpoint=None,
                endpoint_name=None,
                handler=None,
                methods=['GET']
        ):
        '''
        Adds the specified endpoint to the api
        '''
        self.app.add_url_rule(
                    endpoint,
                    endpoint_name,
                    EndpointAction(handler),
                    methods=methods
        )

    def add_monitor(self):
        '''
        INSERT LOGIC TO ADD MONITOR OBJECT
        '''
        return {}

    def edit_monitor(self):
        '''
        INSERT LOGIC TO EDIT MONITOR OBJECT
        '''
        return {}

    def remove_monitor(self):
        '''
        INSERT LOGIC TO REMOVE MONITOR OBJECT
        '''
        return {}

    def info_monitor(self):
        '''
        INSERT LOGIC TO GET MONITOR OBJECT
        '''
        return {}
