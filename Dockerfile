FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set workdir
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Salin semua kode ke dalam container
COPY . .

#expose port 8000
EXPOSE 8000

# Jalankan migration & server (jika production, gunakan gunicorn)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]