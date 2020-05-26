#!/usr/bin/env bash
# result of ‘which conda’ ending in “anaconda3”
export MLFLOW_CONDA_HOME="/Users/user/your/path/to/anaconda3"
# result of ‘pwd’ in project root plus “mlruns”
export MLFLOW_TRACKING_URI="/Users/user/your/project/mlruns"
export MLFLOW_EXPERIMENT_NAME="iris-example"