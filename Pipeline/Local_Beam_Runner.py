from Pipeline import _pipeline_name,_pipeline_root,_data_root,_module_file,_serving_model_dir,_metadata_path,_beam_pipeline_args,_create_pipeline
import absl
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner

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