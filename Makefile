PYTHON=python3.11

.PHONY: black
black:
	${PYTHON} -m black .

.PHONY: ruff
ruff:
	${PYTHON} -m ruff check . --fix

.PHONY: lint
lint:
	@$(MAKE) -s black ruff

.PHONY: reload
reload:
	uvicorn main:app --reload