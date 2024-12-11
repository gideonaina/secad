init:
	python -m venv .venv &&\
	(. ./.venv/bin/activate &&\
	pip install -r requirements.txt &&\
	pip install -e . &&\
	. ./.venv/bin/activate)

setup:
	. ./.venv/bin/activate && \
	pip install -e .	

vm:
	(cd . && . ./.venv/bin/activate)

rag-ingest-file:
	uv run python rag_management/data_prep.py -c $(COLLECTION) -f $(FILE)

ui-gr:
	uv run gradio main.py

ui-st:
	uv run streamlit run ui/streamlit_ui/launch.py

# rag-ingest-file:
# 	python knowledge_extraction/rag_management/data_prep.py -c $(COLLECTION) -f $(FILE)

# ui-gr:
# 	gradio main.py

# ui-st:
# 	streamlit run ui/streamlit_ui/launch.py