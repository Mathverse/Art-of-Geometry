python -m pip install PEP517 PIP SetUpTools Wheel --upgrade --break-system-packages

python -m pip install -e ".[build, dev, doc, lint, jupyter, manim, publish, test, viz]" --upgrade --user --break-system-packages
