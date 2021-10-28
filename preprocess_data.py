import tensorflow as tf
import glob

#images_ds = tf.data.Dataset.list_files('images/*/*', shuffle=True)

images = glob.glob('images/*/*.jpg')

image_count = len(images)
print(f"{image_count} images found")

#type(images_ds)

filepath = "test.tfrecords"

#class_names = ["cube", "cone", "sphere"]

# The following functions can be used to convert a value to a type compatible
# with tf.train.Example.

def _bytes_feature(value):
  """Returns a bytes_list from a string / byte."""
  if isinstance(value, type(tf.constant(0))):
    value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
  """Returns a float_list from a float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _int64_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def image_example(image_string, label):

    image_shape = tf.io.decode_jpeg(image_string).shape

    feature = {
            'height': _int64_feature(image_shape[0]),
            'width': _int64_feature(image_shape[1]),
            'depth': _int64_feature(image_shape[2]),
            'label': _int64_feature(label),
            'image_raw': _bytes_feature(image_string),
        }
    
    return tf.train.Example(features=tf.train.Features(feature=feature))

with tf.io.TFRecordWriter(filepath) as writer:
    for img in images:

        label = 0 if 'cube' in img else 1 if 'cone' in img else 2
        image_string = open(img, 'rb').read()

        tf_example = image_example(image_string, label)

        writer.write(tf_example.SerializeToString())


#TODO parse and check that all is well