.PHONY: all backend frontend

all: backend frontend

backend:
	@echo "Starting backend..."
	@python backend.py &

frontend:
	@echo "Starting frontend..."
	@streamlit run streamlit_app.py