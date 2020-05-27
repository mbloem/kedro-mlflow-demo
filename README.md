# Kedro + MLflow Demo

This is a demo of how Kedro & MLflow can be used together, based on the instructions provided in [this article](https://medium.com/@QuantumBlack/deploying-and-versioning-data-pipelines-at-scale-942b1d81b5f5#).
The demo is based on the example Iris project that Kedro optionally provides during creation of a new Kedro project.

This project was created to serve as a demo for [a meetup talk](https://www.meetup.com/Data-Science-and-Analytics-West-Michigan/events/270553236/).

## Overview

This is a Kedro+MLflow project.
It was generated using `Kedro 0.16.1` by running:

```
kedro new
```

Then, a couple of MLflow files (`MLproject` and `conda.yml`) and the `mlruns` directory were added to the project per the example [here](https://medium.com/@QuantumBlack/deploying-and-versioning-data-pipelines-at-scale-942b1d81b5f5#).
Some MLflow code was also added in `src/kedro_mlflow_demo/pipelines/data_science/nodes.py` to log models, results, etc.

Take a look at the [Kedro documentation](https://kedro.readthedocs.io) and the [MLflow documentation](https://mlflow.org/docs/latest/index.html) for more help getting started.

The remainder of the readme is mostly what Kedro provides when creating a new project, with a few small changes regarding MLflow integration.

## Rules and guidelines

In order to get the best out of the template:

 * Please don't remove any lines from the `.gitignore` file we provide
 * Make sure your results can be reproduced by following a data engineering convention, e.g. the one we suggest [here](https://kedro.readthedocs.io/en/stable/06_resources/01_faq.html#what-is-data-engineering-convention)
 * Don't commit any data to your repository
 * Don't commit any credentials or local configuration to your repository
 * Keep all credentials or local configuration in `conf/local/`

## Setting up environment and installing dependencies

Create a new Anaconda environment for this project with a command like:

```
conda create -n kedro-mlflow-demo-env python=3.7
```

Then activate the environment and install Kedro:

```
conda activate kedro-mlflow-demo-env
pip install kedro
```

Dependencies are declared in `src/requirements.txt` for `pip` installation within the conda environment.

To install them, run:

```
kedro install
```

Ensure that MLflow 1.8 or greater was installed with:

```
mlflow --version
```

## Running Kedro+MLflow projects

Some MLflow environmental variables (`MLFLOW_CONDA_HOME`, `MLFLOW_TRACKING_URI`, `MLFLOW_EXPERIMENT_NAME`) must be set prior to running the project.
To set these, update `config-mlflow-template.sh` based on your environment, move it to `conf/local` (to keep the version based on your particular set up out of version control), and run it.
Depending on what shell you are using you may need to set your environmental variables differently than is specified in this shell script.

Create an MLflow experiment with the name specified in `MLFLOW_EXPERIMENT_NAME`:

```
mlflow experiments create -n <experiment_name>
```

where `<experiment_name>` is replaced with the name set in `MLFLOW_EXPERIMENT_NAME` (e.g., `iris-example`).

You can run the Kedro+MLflow project by executing (from the base `kedro-mlflow-demo` directory):

```
mlflow run . -e <entry_point_name>
```

Where `<entry_point_name>` is replaced by an entry point in the `MLproject` file.
These entry points should all specify Kedro pipelines to run via `kedro run` commands.

Note that when running on Windows, it is recommendted to use the `--no-conda` option for this command, as the MLflow automatic generation and usage of anaconda environments does not yet seem to work very well on Windows.

## Testing Kedro

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests with the following command:

```
kedro test
```

To configure the coverage threshold, please have a look at the file `.coveragerc`.


## Working with Kedro from notebooks

In order to use notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

For using Jupyter Lab, you need to install it:

```
pip install jupyterlab
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

You can also start Jupyter Lab:

```
kedro jupyter lab
```

And if you want to run an IPython session:

```
kedro ipython
```

Running Jupyter or IPython this way provides the following variables in
scope: `proj_dir`, `proj_name`, `conf`, `io`, `parameters` and `startup_error`.

### Converting notebook cells to nodes in a Kedro project

Once you are happy with a notebook, you may want to move your code over into the Kedro project structure for the next stage in your development. This is done through a mixture of [cell tagging](https://jupyter-notebook.readthedocs.io/en/stable/changelog.html#cell-tags) and Kedro CLI commands.

By adding the `node` tag to a cell and running the command below, the cell's source code will be copied over to a Python file within `src/<package_name>/nodes/`.
```
kedro jupyter convert <filepath_to_my_notebook>
```
> *Note:* The name of the Python file matches the name of the original notebook.

Alternatively, you may want to transform all your notebooks in one go. To this end, you can run the following command to convert all notebook files found in the project root directory and under any of its sub-folders.
```
kedro jupyter convert --all
```

### Ignoring notebook output cells in `git`

In order to automatically strip out all output cell contents before committing to `git`, you can run `kedro activate-nbstripout`. This will add a hook in `.git/config` which will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be left intact locally.

## Package the project

In order to package the project's Python code in `.egg` and / or a `.wheel` file, you can run:

```
kedro package
```

After running that, you can find the two packages in `src/dist/`.

## Building API documentation

To build API docs for your code using Sphinx, run:

```
kedro build-docs
```

See your documentation by opening `docs/build/html/index.html`.

## Building the project requirements

To generate or update the dependency requirements for your project, run:

```
kedro build-reqs
```

This will copy the contents of `src/requirements.txt` into a new file `src/requirements.in` which will be used as the source for `pip-compile`. You can see the output of the resolution by opening `src/requirements.txt`.

After this, if you'd like to update your project requirements, please update `src/requirements.in` and re-run `kedro build-reqs`.
