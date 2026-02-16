FROM python:3.9-slim
WORKDIR /app
COPY tempSim.py .
ENV PYTHONUNBUFFERED=1
CMD ["python", "tempSim.py"]