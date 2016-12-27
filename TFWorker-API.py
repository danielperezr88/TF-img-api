import tornado.ioloop
from tornado_json.routes import get_routes
from tornado_json.application import Application

from google.protobuf import timestamp_pb2
from gcloud import storage

import TFWorker

CACHE_BUCKET = 'cache-files-hf'

if __name__ == '__main__':

    client = storage.Client()
    for filename in ['retrained_graph.pb', 'retrained_labels.txt', 'breakhis_retrained_graph.pb', 'breakhis_retrained_labels.txt']:
        blob = client.get_bucket(CACHE_BUCKET).get_blob(filename)
        fp = open(filename, 'wb')
        blob.download_to_file(fp)
        fp.close()

    routes = get_routes(TFWorker)

    application = Application(routes=routes, settings={})

    application.listen(88)

    tornado.ioloop.IOLoop.instance().start()
