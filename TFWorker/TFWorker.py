import argparse
import urllib
import os
import tensorflow as tf

def InferMain(args):

    img_url = urllib.urlopen(args.image)
    image_data = img_url.read()

    lbl_file_path = 'retrained_labels.txt' if args.model == 'flowers' else 'breakhis_retrained_labels.txt'
    label_lines = [line.rstrip() for line in tf.gfile.GFile(lbl_file_path)]

    graph_file_path = 'retrained_graph.pb' if args.model == 'flowers' else 'breakhis_retrained_graph.pb'
    with tf.gfile.FastGFile(graph_file_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        return dict([(label_lines[i], "%.5f"%predictions[0][i]) for i in top_k])

if __name__ == '__main__':
    commonParser = argparse.ArgumentParser()
    subparsers = commonParser.add_subparsers(dest='mode', help="Mode")

    inferParser = argparse.ArgumentParser(add_help=False)
    inferParser.add_argument(
        'image',
        type=str,
        help='Image to process (URL)'
    )

    inferParser.add_argument(
        '--model',
        type=str,
        default='flowers',
        help='Inference model to apply (flowers OR breast_cancer)'
    )

    subparsers.add_parser(
        'infer',
        parents=[inferParser],
        help='Apply a classification model with a given image'
    )

    args = commonParser.parse_args()

    if args.mode == 'infer':
        InferMain(args)
    else:
        raise Exception("Unknown Mode Value...")
