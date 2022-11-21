## Project

This repository hosts the code for the demo app



<p>&nbsp;</p>


## Branch naming

The codebase is hosted in the following branch:


- `dev-python/main` — this branch contains the Python pre-production code


<p>&nbsp;</p>

## Python branch setup

Create an isolated Python environment:
```python
python3 -m venv env
source env/bin/activate
```

Then install dependencies:

```python
pip install --upgrade pip
pip install -r requirements.txt
```

If you do get an [error](https://stackoverflow.com/questions/73512185/error-could-not-build-wheels-for-backports-zoneinfo-error-while-installing-dja) `Could not build wheels for backports.zoneinfo`
while installing `streamlit`, run the following command:

```bash
export C_INCLUDE_PATH=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/Headers
```

or add it to your `.zshrc` file, which contains the shell configurations and commands, and source it:

```bash
vim ~/.zshrc
export C_INCLUDE_PATH=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/Headers
source ~/.zshrc
```