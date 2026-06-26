# 1. Official lightweight python image as the base of the operating system
FROM python:3.10-slim

# 2. Set the working directory in the container
WORKDIR /usr/src/app

# 3. Copy only the requirements file first (It caches the dependencies to speed up future builds.)
COPY requirements.txt ./

# 4. Install python dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy rest of the code into the container
COPY . .

# 6. Expose the port on which the Flask app runs on
EXPOSE 5000

# 7. Define the command to run the application when the container starts
CMD ["python", "app.py"]