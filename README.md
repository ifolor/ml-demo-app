## Project

This repository hosts the code for the demo app



<p>&nbsp;</p>


## Branch naming

The codebase is hosted in the following branch:


- `dev/main` — this branch contains the code to host the demo app on the local Streamlit server
- `dev/gcp_crop_hints` — this branch contains the code to use the GCP crop hints service



<p>&nbsp;</p>

## Branch setup

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

**Installing Streamlit:** If you do get an [error](https://stackoverflow.com/questions/73512185/error-could-not-build-wheels-for-backports-zoneinfo-error-while-installing-dja) `Could not build wheels for backports.zoneinfo`
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

## Run the Streamlit app

1. **Run** `streamlit run main.py` from your terminal to deploy the app on local Streamlit server 
2. **Navigate** to http://localhost:8501/ in your browser

## Customize the Streamlit UI
Create a **.streamlit** folder in your repository and add the theme specifications:
    
```bash
vim .streamlit/config.toml
```
![Alt text](public_assets/image_1.png?raw=true "Title")

Many configurations options are available [here](https://docs.streamlit.io/library/advanced-features/configuration).