init:
	pip install -r requirements.txt

test:
	pytest --color=yes --tb=short
