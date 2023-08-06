---
layout: post
title:  "Understanding TFRecords in Tensorflow 2.x"
date:   2023-08-06 12:32:45 +0330
categories:
---

# Understanding TFRecords in Tensorflow 2.x
I used to feed my Tensorflow (tf) models with Numpy (np) `ndarrays`. Although quite convenient, this approach could not be used for large datasets without complications, as the entirety (or parts) of the dataset should be loaded into the system memory. To solve these shortcomings, Tensorflow offers the `TFRecord` class, a disk-based streaming solution that uses `Protobufs`. Long story short, to use TFRecords in our projects, we should first convert the dataset into TFRecords and store them on disk. Then, before launching the training process, load them back from the disk and set the configurations such as batch size, epoch, and pre-fetch. To have a clear overview, these are the steps required to use TFRecords:

* Convert dataset to TFRecords:
  - Iterate over the raw dataset and convert each pair of an example (image or anything else) and its label to `tf.train.Example`.
  - Serialize each `tf.train.Example` and write it into the opened TFRecord file with `TFRecord.write()`.
* Use the TFRecord that is created:
  - Open the file with `tf.data.TFRecordDataset()`.
  - Parse the serialized entries of the dataset in a single pass with `dataset.map()`.
  - Set the bach size and epoch with `dataset.batch()` and `dataset.repeat()`. 
  - Feed the dataset (the configured and parsed TFRecord instance) directly to the model.

## Notes
1. TFRecord is graph-based, meaning that to access the value of an entry, the returned tensors should be evaluated. See the example below:
```python
tmp = dataset.take(1) # a new subset of the dataset that holds only one entry of the batch size.
np_val = tf.keras.backend.eval( list(tmp.as_numpy_iterator()) )
```

2. TFRecord is a streaming solution, meaning that random access to the entries is not possible.
3. A configured TFRecord to a particular batch size (`B`) holds `B` data entries concatenated into a single tensor.
4. TFRecord compression is supported (using `GZIP` or `ZLIB`):
```python
options = tf.io.TFRecordOptions(compression_type='ZLIB')
with tf.io.TFRecordWriter(filename, options=options) as tfr_train:
  pass
```

## Examples 
TODO.

## Links
1. [TF Documentation](https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset)
1. [Feeding-TensorFlow-from-drive-MNIST-Example](https://github.com/datamadness/Feeding-TensorFlow-from-drive-MNIST-Example)
1. [Mnist-Tfrecord](https://github.com/TanyaChutani/Mnist-Tfrecord/blob/master/notebook/TF2_0_ImageClassificationTFRecord.ipynb)











