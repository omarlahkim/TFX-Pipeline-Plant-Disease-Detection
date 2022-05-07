import os
from typing import List
import absl
import tensorflow as tf
import tensorflow_transform as tft
from tensorflow import keras
from tfx.components.trainer.fn_args_utils import DataAccessor
from tfx.components.trainer.fn_args_utils import FnArgs
from tfx.components.trainer.rewriting import converters
from tfx.components.trainer.rewriting import rewriter
from tfx.components.trainer.rewriting import rewriter_factory
from tfx.dsl.io import fileio
from tfx_bsl.tfxio import dataset_options

import flatbuffers
from tflite_support import metadata_schema_py_generated as _metadata_fb
from tflite_support import metadata as _metadata
# When training on the whole dataset use following constants instead.
# This setting should give ~91% accuracy on the whole test set
# _TRAIN_DATA_SIZE = 50000
# _EVAL_DATA_SIZE = 10000
# _TRAIN_BATCH_SIZE = 64
# _EVAL_BATCH_SIZE = 64
# _CLASSIFIER_LEARNING_RATE = 3e-4s
# _FINETUNE_LEARNING_RATE = 5e-5
# _CLASSIFIER_EPOCHS = 12

_TRAIN_DATA_SIZE = 10 #128
_EVAL_DATA_SIZE = 10 #128
_TRAIN_BATCH_SIZE = 32
_EVAL_BATCH_SIZE = 32
_CLASSIFIER_LEARNING_RATE = 1e-3
_FINETUNE_LEARNING_RATE = 7e-6
_CLASSIFIER_EPOCHS = 1
_IMAGE_SIZE = 224
_IMAGE_KEY = 'image_raw'
_LABEL_KEY = 'label'

_TFLITE_MODEL_NAME = 'tflite'

_INPUT_SHAPE = (_IMAGE_SIZE, _IMAGE_SIZE, 3)

def _transformed_name(key):
  return key + '_xf'


def _get_serve_image_fn(model):
  @tf.function
  def serve_image_fn(image_tensor):

    return model(image_tensor)


  return serve_image_fn


def _image_augmentation(image_features):

  batch_size = tf.shape(image_features)[0]
  image_features = tf.image.random_flip_left_right(image_features)
  image_features = tf.image.resize_with_crop_or_pad(image_features, 250, 250)
  image_features = tf.image.random_crop(image_features,
                                        (batch_size, 224, 224, 3))
  return image_features


def _data_augmentation(feature_dict):

  image_features = feature_dict[_transformed_name(_IMAGE_KEY)]
  image_features = _image_augmentation(image_features)
  feature_dict[_transformed_name(_IMAGE_KEY)] = image_features
  return feature_dict


def _input_fn(file_pattern: List[str],
              data_accessor: DataAccessor,
              tf_transform_output: tft.TFTransformOutput,
              is_train: bool = False,
              batch_size: int = 200) -> tf.data.Dataset:

  dataset = data_accessor.tf_dataset_factory(
      file_pattern,
      dataset_options.TensorFlowDatasetOptions(
          batch_size=batch_size, label_key=_transformed_name(_LABEL_KEY)),
      tf_transform_output.transformed_metadata.schema)

  if is_train:
    dataset = dataset.map(lambda x, y: (_data_augmentation(x), y))

  return dataset


def _freeze_model_by_percentage(model: tf.keras.Model, percentage: float):

  if percentage < 0 or percentage > 1:
    raise ValueError('Freeze percentage should between 0.0 and 1.0')

  if not model.trainable:
    raise ValueError(
        'The model is not trainable, please set model.trainable to True')

  num_layers = len(model.layers)
  num_layers_to_freeze = int(num_layers * percentage)
  for idx, layer in enumerate(model.layers):
    if idx < num_layers_to_freeze:
      layer.trainable = False
    else:
      layer.trainable = True


def _build_keras_model() -> tf.keras.Model:
  base_model = keras.models.load_model("plant_disease_detection.h5")
  base_model.summary()
  base_model.layers.pop(0)
  new_input_layer = tf.keras.Input(shape=_INPUT_SHAPE,name=_transformed_name(_IMAGE_KEY))
  new_output_layer = base_model(new_input_layer)
  new_model = tf.keras.Model(new_input_layer, new_output_layer)
  new_model.summary()

  #base_model.input_specs = None #tf.keras.layers.InputSpec(shape=_INPUT_SHAPE,name=_transformed_name(_IMAGE_KEY)) #, name=_transformed_name(_IMAGE_KEY)
  #model = tf.keras.Sequential([
   #   base_model
  #])

  new_model.compile(
      loss='sparse_categorical_crossentropy',
      optimizer='adam',
      metrics=['accuracy'])
  '''
  

  _freeze_model_by_percentage(base_model, 0.0)

  '''
  return new_model

def decode_PNG(x):
    if len(str(x[0])) >= 50:
        return tf.io.decode_jpeg(x[0], channels=3)

# TFX Transform will call this function.
def preprocessing_fn(inputs):

  absl.logging.info('Preprocessing Started')

  outputs = {}

  image_features = tf.map_fn(
      lambda x: decode_PNG(x),
      inputs[_IMAGE_KEY],
      dtype=tf.uint8)
  # image_features = tf.cast(image_features, tf.float32)
  image_features = tf.image.resize(image_features, [224, 224])
  image_features = tf.keras.applications.efficientnet.preprocess_input(image_features)
  outputs[_transformed_name(_IMAGE_KEY)] = image_features
  # Do not apply label transformation as it will result in wrong evaluation.
  outputs[_transformed_name(_LABEL_KEY)] = inputs[_LABEL_KEY]
  return outputs


def _write_metadata(model_path: str, label_map_path: str, mean: List[float],
                    std: List[float]):


  model_meta = _metadata_fb.ModelMetadataT()

  input_meta = _metadata_fb.TensorMetadataT()
  input_normalization = _metadata_fb.ProcessUnitT()
  input_normalization.optionsType = (
      _metadata_fb.ProcessUnitOptions.NormalizationOptions)
  input_normalization.options = _metadata_fb.NormalizationOptionsT()
  input_normalization.options.mean = mean
  input_normalization.options.std = std
  input_meta.processUnits = [input_normalization]

  output_meta = _metadata_fb.TensorMetadataT()
  label_file = _metadata_fb.AssociatedFileT()
  label_file.name = os.path.basename(label_map_path)
  label_file.type = _metadata_fb.AssociatedFileType.TENSOR_AXIS_LABELS
  output_meta.associatedFiles = [label_file]
  subgraph = _metadata_fb.SubGraphMetadataT()
  subgraph.inputTensorMetadata = [input_meta]
  subgraph.outputTensorMetadata = [output_meta]
  model_meta.subgraphMetadata = [subgraph]

  b = flatbuffers.Builder(0)
  b.Finish(
      model_meta.Pack(b), _metadata.MetadataPopulator.METADATA_FILE_IDENTIFIER)
  metadata_buf = b.Output()

  populator = _metadata.MetadataPopulator.with_model_file(model_path)
  populator.load_metadata_buffer(metadata_buf)
  populator.load_associated_files([label_map_path])
  populator.populate()


# TFX Trainer will call this function.
def run_fn(fn_args: FnArgs):

  absl.logging.info('Trainning Started')
  tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)

  train_dataset = _input_fn(
      fn_args.train_files,
      fn_args.data_accessor,
      tf_transform_output,
      is_train=True,
      batch_size=_TRAIN_BATCH_SIZE)
  eval_dataset = _input_fn(
      fn_args.eval_files,
      fn_args.data_accessor,
      tf_transform_output,
      is_train=False,
      batch_size=_EVAL_BATCH_SIZE)
  model= _build_keras_model()

  absl.logging.info('Tensorboard logging to {}'.format(fn_args.model_run_dir))
  # Write logs to path
  tensorboard_callback = tf.keras.callbacks.TensorBoard(
      log_dir=fn_args.model_run_dir, update_freq='batch')


  steps_per_epoch = 10 #  int(_TRAIN_DATA_SIZE / _TRAIN_BATCH_SIZE)
  total_epochs = 2  #int(fn_args.train_steps / steps_per_epoch)
  if _CLASSIFIER_EPOCHS > total_epochs:
    raise ValueError('Classifier epochs is greater than the total epochs')

  absl.logging.info('c')
  model.fit(
      train_dataset,
      epochs=_CLASSIFIER_EPOCHS,
      steps_per_epoch=steps_per_epoch,
      validation_data=eval_dataset,
      validation_steps=fn_args.eval_steps,
      callbacks=[tensorboard_callback], verbose=1)
  '''
  model.compile(
      loss='sparse_categorical_crossentropy',
      optimizer='adam',
      metrics=['accuracy'])

  model.summary(print_fn=absl.logging.info)

  model.fit(
      train_dataset,
      initial_epoch=_CLASSIFIER_EPOCHS,
      epochs=total_epochs,
      steps_per_epoch=steps_per_epoch,
      validation_data=eval_dataset,
      validation_steps=fn_args.eval_steps,
      callbacks=[tensorboard_callback])
      '''
  signatures = {
      'serving_default':
          _get_serve_image_fn(model).get_concrete_function(
              tf.TensorSpec(
                  shape=[None, _IMAGE_SIZE, _IMAGE_SIZE, 3],
                  dtype=tf.float32,
                  name=_transformed_name(_IMAGE_KEY)))
  }
  absl.logging.info('Model Saved Successfully to: ')
  absl.logging.info(fn_args.serving_model_dir)
  model.save(fn_args.serving_model_dir,save_format='tf',signatures=signatures)