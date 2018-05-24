from os import getpid#, path
import inspect
import logging
import tornado.ioloop
from tornado_json.routes import get_routes
from tornado_json.application import Application

#from google.protobuf import timestamp_pb2
#from gcloud import storage

import TFWorker

#CACHE_BUCKET = 'cache-files'


#def lookup_bucket(cli, prefix):
#    for bucket in cli.list_buckets():
#        if bucket.name.startswith(prefix):
#            return bucket.name
#    logging.error("Cache Bucket not found")


def save_pid():
    """Save pid into a file: filename.pid."""
    pidfilename = inspect.getfile(inspect.currentframe()) + ".pid"
    f = open(pidfilename, 'w')
    f.write(str(getpid()))
    f.close()

if __name__ == '__main__':

    logfilename = inspect.getfile(inspect.currentframe()) + ".log"
    logging.basicConfig(filename=logfilename, level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info("Started")

    save_pid()

    #for filename in ['retrained_graph.pb', 'retrained_labels.txt', 'breakhis_retrained_graph.pb',
    #                 'breakhis_retrained_labels.txt']:
    #    filepath = path.join(path.dirname(path.realpath(__file__)), filename)
    #    if not path.exists(filepath):
    #        client = storage.Client()
    #        blob = client.get_bucket(lookup_bucket(client, CACHE_BUCKET)).get_blob(filename)
    #        fp = open(filepath, 'wb')
    #        blob.download_to_file(fp)
    #        fp.close()

    routes = get_routes(TFWorker)

    application = Application(routes=routes, settings={})

    application.listen(88)

    tornado.ioloop.IOLoop.instance().start()
