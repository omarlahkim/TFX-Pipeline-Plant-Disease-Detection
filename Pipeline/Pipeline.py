import os
from typing import List
import absl
import tensorflow_model_analysis as tfma
from tfx.components import Evaluator
from tfx.components import ExampleValidator
from tfx.components import ImportExampleGen
from tfx.components import Pusher
from tfx.components import SchemaGen
from tfx.components import StatisticsGen
from tfx.components import Trainer
from tfx.components import Transform
from tfx.dsl.components.common import resolver
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.orchestration import metadata
from tfx.orchestration import pipeline
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner
from tfx.proto import example_gen_pb2
from tfx.proto import pusher_pb2
from tfx.proto import trainer_pb2
from tfx.types import Channel
from tfx.types.standard_artifacts import Model
from tfx.types.standard_artifacts import ModelBlessing
import tensorflow as tf

tf.config.experimental.enable_mlir_graph_optimization()
_pipeline_name = 'plant_disease_detection_pipeline'


_plant_pipeline_root = os.getcwd()
_data_root = os.path.join(_plant_pipeline_root, 'Data')

_module_file = os.path.join(_plant_pipeline_root, 'utils.py')

_serving_model_dir = os.path.join(_plant_pipeline_root, 'serving_model',
                                       _pipeline_name)


_tfx_root = os.path.join(os.environ['HOME'], 'tfx')
_pipeline_root = os.path.join(_tfx_root, 'pipelines', _pipeline_name)
_metadata_path = os.path.join(_tfx_root, 'metadata', _pipeline_name,
                              'metadata.db')

_beam_pipeline_args = [
    '--direct_running_mode=multi_processing',
    '--direct_num_workers=0',
]

def _create_pipeline(pipeline_name: str, pipeline_root: str, data_root: str,
                     module_file: str, serving_model_dir: str,
                     metadata_path: str,
                     beam_pipeline_args: List[str]) -> pipeline.Pipeline:

  output_config = example_gen_pb2.Output(
      split_config=example_gen_pb2.SplitConfig(splits=[
          example_gen_pb2.SplitConfig.Split(name='train', hash_buckets=6),
          example_gen_pb2.SplitConfig.Split(name='test', hash_buckets=2),
          example_gen_pb2.SplitConfig.Split(name='eval', hash_buckets=2)]))

  example_gen = ImportExampleGen(
      input_base=data_root, output_config=output_config)

  statistics_gen = StatisticsGen(examples=example_gen.outputs['examples'])

  schema_gen = SchemaGen(
      statistics=statistics_gen.outputs['statistics'], infer_feature_shape=True)

  example_validator = ExampleValidator(
      statistics=statistics_gen.outputs['statistics'],
      schema=schema_gen.outputs['schema'])

  transform = Transform(
      examples=example_gen.outputs['examples'],
      schema=schema_gen.outputs['schema'],
      module_file=module_file)


  trainer = Trainer(
      module_file=module_file,
      examples=transform.outputs['transformed_examples'],
      transform_graph=transform.outputs['transform_graph'],
      schema=schema_gen.outputs['schema'],
      train_args=trainer_pb2.TrainArgs(num_steps=10),
      eval_args=trainer_pb2.EvalArgs(num_steps=4))

  model_resolver = resolver.Resolver(
      strategy_class=latest_blessed_model_resolver.LatestBlessedModelResolver,
      model=Channel(type=Model),
      model_blessing=Channel(
          type=ModelBlessing)).with_id('latest_blessed_model_resolver')


  eval_config = tfma.EvalConfig(
      model_specs=[tfma.ModelSpec(label_key='label_xf',signature_name='serving_default')],
      slicing_specs=[tfma.SlicingSpec()],
      metrics_specs=[
          tfma.MetricsSpec(metrics=[
              tfma.MetricConfig(
                  class_name='SparseCategoricalAccuracy',
                  threshold=tfma.MetricThreshold(
                      value_threshold=tfma.GenericValueThreshold(
                          lower_bound={'value': 0.55}),
                      # Change threshold will be ignored if there is no
                      # baseline model resolved from MLMD (first run).
                      change_threshold=tfma.GenericChangeThreshold(
                          direction=tfma.MetricDirection.HIGHER_IS_BETTER,
                          absolute={'value': -1e-3})))
          ])
      ])


  evaluator = Evaluator(
      examples=transform.outputs['transformed_examples'],
      model=trainer.outputs['model'],
      baseline_model=model_resolver.outputs['model'],
      eval_config=eval_config)


  pusher = Pusher(
      model=trainer.outputs['model'],
      model_blessing=evaluator.outputs['blessing'],
      push_destination=pusher_pb2.PushDestination(
          filesystem=pusher_pb2.PushDestination.Filesystem(
              base_directory=serving_model_dir)))

  components = [
      example_gen, statistics_gen, schema_gen, example_validator, transform,
      trainer, model_resolver, evaluator, pusher
  ]

  return pipeline.Pipeline(
      pipeline_name=pipeline_name,
      pipeline_root=pipeline_root,
      components=components,
      enable_cache=True,
      metadata_connection_config=metadata.sqlite_metadata_connection_config(
          metadata_path),
      beam_pipeline_args=beam_pipeline_args)


# To run this pipeline from the python CLI:
if __name__ == '__main__':
  absl.logging.set_verbosity(absl.logging.INFO)
  BeamDagRunner().run(
      _create_pipeline(
          pipeline_name=_pipeline_name,
          pipeline_root=_pipeline_root,
          data_root=_data_root,
          module_file=_module_file,
          serving_model_dir=_serving_model_dir,
          metadata_path=_metadata_path,
          beam_pipeline_args=_beam_pipeline_args))