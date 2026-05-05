PYTHON ?= python
NPM ?= npm

.PHONY: pipeline simulate clean features eda train predict export app-install app-dev app-build

pipeline:
	$(PYTHON) -m src.pipeline

simulate:
	$(PYTHON) -m src.simulate_data

clean:
	$(PYTHON) -m src.clean_data

features:
	$(PYTHON) -m src.create_features

eda:
	$(PYTHON) -m src.exploratory_analysis

train:
	$(PYTHON) -m src.train_model

predict:
	$(PYTHON) -m src.predict_churn

export:
	$(PYTHON) -m src.export_frontend_data

app-install:
	cd app && $(NPM) install

app-dev:
	cd app && $(NPM) run dev

app-build:
	cd app && $(NPM) run build
