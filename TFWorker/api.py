from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
from schemas import schemas

import re
import sys

import TFWorker


def abstractGet(self):
    args = ArgHandler(self.retrieveArgs())
    return getattr(sys.modules['TFWorker.TFWorker'], re.sub(r'^(.*)Handler', r'\1Main', self.__class__.__name__))(
        args)  # alignMain(args)


class ArgHandler():
    """Handler for Argument Retrieval and Formatting"""

    def __init__(self, *dictArg, **kwArgs):
        for dictionary in dictArg:
            for key, value in dictionary.items():
                setattr(self, key, value)
        for key, value in kwArgs.items():
            setattr(self, key, value)


class BaseHandler(APIHandler):
    """Base Handler for API function implementation"""

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.schema = schemas.get(self.__class__.__name__, {})

    def retrieveArgs(self):
        return {n: self.body.get(n, v.get('default', None)) for (n, v) in \
                self.schema['properties'].items()}

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header('Access-Control-Allow-Methods', 'POST')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')


class InferHandler(BaseHandler):
    """Handler for Align Function"""
    pass


setattr(InferHandler, 'post', schema.validate(input_schema=schemas['InferHandler'])(abstractGet))
