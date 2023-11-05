# FFI Lab

This is a lab project for an upcoming workshop on FFI

# Requirements
1. cargo
    1. prost
    2. pyo3
    3. tokio
    4. tonic
2. rustc
3. python3.11
4. pip: https://pip.pypa.io/en/stable/installation/
    1. grpcio
    2. grpcio-tools
    3. maturin
    4. protobuf
5. protoc: https://github.com/hyperium/tonic#dependencies

TODO: Can we use Docker to handle this for the users?

# Usage
## Setup
From the project root:
1. Create a virtualenv to work in: `python -m venv .venv`
2. Install the necessary python packages: `pip install --require-virtualenv -r requirements.txt`
NOTE: vscode doesn't seem to handle virtualenvs very well. You can either skip making a virtualenv entirely (and the --require-virtualenv), add the new python path (located at .venv/Scripts/python(.exe)) to vscode (ctrl-shift-p -> Python: Select Interpreter), or use a different terminal for running the commands below.

## Running the code
There are 2 folders, workshop and solution. As the names imply, workshop will contain partially completed code to be completed during the workshop itself while solution holds a working final version of the code at the end of the workshop. There are 3 main binaries to run (in either the workshop or solution folder):

1. cli.py: cli for executing some python code against a json database
    1. Usage: `python cli.py pymk 0` (see `--help` for more)
1. database_server.py: a "remote" database server implemented in python to replace the in-memory database
    1. Usage: `python database_server.py`
1. database_server: a "remote" database server implemented in rust to replace the in-memory database
    1. Usage: `cd database; cargo run --release`

There is also an FFI library (the main point of the workshop) that needs to be built with `cd database_ffi; maturin develop`. Then you should be able to run `python -c import database_ffi`