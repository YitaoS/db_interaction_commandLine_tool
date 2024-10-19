install:
	pip install --upgrade pip && pip install -r requirements.txt
	pip install .[dev]

format:
	black *.py
	
lint:
	flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 *.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

test:
	python3 -m pytest -vv test*.py
	
all: install format lint test