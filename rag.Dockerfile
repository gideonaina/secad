FROM langflowai/langflow:latest

CMD ["python", "-m", "langflow", "run", "--host", "0.0.0.0", "--port", "7860"]

# FROM python:3.12.4-bookworm

# # Make port 7860 available to the world outside this container
# EXPOSE 7860

# # Define environment variable to prevent tracking
# ENV DO_NOT_TRACK=true

# RUN pip install langflow -U
# ENTRYPOINT [ "langflow", "run", "--port", "7860" ]