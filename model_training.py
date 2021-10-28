import tensorflow as tf

filenames = ['test.tfrecords']
raw_dataset = tf.data.TFRecordDataset(filenames)

# Description of the features to be passed onto the parser

feature_description = {
    'height': tf.io.FixedLenFeature([], tf.int64, default_value=0),
    'width': tf.io.FixedLenFeature([], tf.int64, default_value=0),
    'depth': tf.io.FixedLenFeature([], tf.int64, default_value=0),
    'label': tf.io.FixedLenFeature([], tf.int64, default_value=0),
    'image_raw': tf.io.FixedLenFeature([], tf.string),
}

def _parse_function(example_proto):
    return tf.io.parse_single_example(example_proto, feature_description)

parsed_dataset = raw_dataset.map(_parse_function)

sample = parsed_dataset.take(1).as_numpy_iterator()

print(list(sample))

