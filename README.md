# Encyclopedia

This repo contains articles about python. They stored in `articles` directory in mardown format.

To make it easier for users - there is a `generate.py` script, which converts articles to html.

Script relies on external packages, you can install them with 

```python
pip3 install -r requirements.txt
```

Script allow 2 modes `build` / `watch`

```python
# just update articles in public/
python3 generate.py 

# starts server with livereload
python3 generate.py --livereload
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
