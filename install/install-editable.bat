python -m pip install PEP517 PIP SetUpTools Wheel --upgrade

python -m pip install -e ".[build, dev, doc, lint, manim, publish, test, viz]" --upgrade --user
