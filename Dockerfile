# Base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /trip_planner

# Copy project code
COPY . /trip_planner

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Make sure Python always sees the project root
ENV PYTHONPATH="/trip_planner:${PYTHONPATH}"


# Run Streamlit
CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
