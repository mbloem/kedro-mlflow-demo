# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""
# pylint: disable=invalid-name

import sys
import os
import logging
from typing import Any, Dict

import numpy as np
import pandas as pd
import mlflow
from mlflow import sklearn as mlflow_sklearn
from datetime import datetime
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline as sklearn_Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer, make_column_transformer

from mlinsights.plotting import pipeline2str, pipeline2dot
from pyquickhelper.loghelper import run_cmd


def train_model(
    train_x: pd.DataFrame,
    train_y: pd.DataFrame,
    parameters: Dict[str, Any]
) -> sklearn_Pipeline:
    """Node for training a simple multi-class logistic regression model. The
    number of training iterations as well as the learning rate are taken from
    conf/project/parameters.yml. All of the data as well as the parameters
    will be provided to this function at the time of execution.
    """
    # Build a multi-class logistic regression model
    model_params = parameters['model_params']
    model = LogisticRegression(**model_params)

    if parameters['model_standard_scaler']:
        # Prepare column transformer to do scaling
        col_transformer = ColumnTransformer(
            [
                (
                    'standard_scaler',
                    StandardScaler(copy=False),
                    [
                        "sepal_length",
                        "sepal_width",
                        "petal_length",
                        "petal_width",
                    ],
                ),
            ],
            remainder='drop',
        )

        # Make pipeline w/ scaler
        model_pipeline = sklearn_Pipeline(
            steps=[
                ('col_transformer', col_transformer),
                ('model', model),
            ]
        )
    else:
        # Make pipeline w/o scaler
        model_pipeline = sklearn_Pipeline(
            steps=[
                ('model', model),
            ]
        )

    # Fit
    model_pipeline.fit(train_x, train_y)

    mlflow.set_experiment('iris-example')
    mlflow_sklearn.log_model(sk_model=model_pipeline, artifact_path="model")
    mlflow.log_params(model_params)

    # Print out the model pipeline
    dot = pipeline2dot(model_pipeline, train_x)
    dot_filename = 'pipeline_dot.dot'
    with open(dot_filename, 'w', encoding='utf-8') as f:
        f.write(dot)
    if sys.platform.startswith("win") and "Graphviz" not in os.environ["PATH"]:
        os.environ['PATH'] = os.environ['PATH'] + r';C:\Program Files (x86)\Graphviz2.38\bin'
    cmd = "dot -G=300 -Tpng {0} -o{0}.png".format(dot_filename)
    run_cmd(cmd, wait=True, fLOG=print)
    mlflow.log_artifact('{0}.png'.format(dot_filename), 'model')

    return model_pipeline


def predict(
    model: sklearn_Pipeline, 
    test_x: pd.DataFrame
) -> pd.DataFrame:
    """Node for making predictions given a pre-trained model and a test set.
    """
    # Return predictions
    return model.predict(test_x)


def report_accuracy(
    predictions: pd.DataFrame, 
    test_y: pd.DataFrame
) -> None:
    """Node for reporting the accuracy of the predictions performed by the
    previous node. Notice that this function has no outputs, except logging.
    """
    # Calculate accuracy of predictions
    accuracy = (predictions == test_y).mean()
    
    # Log the accuracy of the model
    log = logging.getLogger(__name__)
    log.info("Model accuracy on test set: %0.2f%%", accuracy * 100)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.set_tag("Model Version", 1)
