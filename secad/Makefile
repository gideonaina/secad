setup:
	uv venv && uv sync && uv pip install -e .

rag-ingest:
	uv run python rag_management/data_prep.py -c $(COLLECTION) -f $(FILE)

start-gradio:
	uv run gradio main.py

start:
	uv run streamlit run ui/streamlit_ui/launch.py