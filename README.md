# DevOps-Portfolio

## Branch day1_and_day2:

### Day 1:
We have created a sample Flask application with in memory database that executes locally using python and docker.

### Day 2:
We updated the application by containerzing it and adding the requirements.txt for installing the required dependencies in the app antomatically.

## Branch day3

### Day 3:

Multi-Container Orchestration with Docker Compose.

In the real world, applications rarely live inside a single container. A web app needs a database, and those two components need to talk to each other securely over a private network.In this branch we have thrown away our temporary "in-memory" task list and connected our Flask API to a real PostgreSQL database.

Instead of typing long docker run commands for each container, we will write a docker-compose.yml file. This is an infrastructure-as-code file that spins up your entire environment with a single command.

## Branch Week_2_CI_Pipeline_Introduction

### Day 4: Remote Version Control.

Right now, your code only exists on your laptop. If your hard drive fails, the project is gone. Furthermore, DevOps is all about collaboration and automation. To trigger our CI/CD pipelines next week, your code needs to live in a central repository. On Day 4, we will push your project to GitHub.

### Day 5:
Day 5: Continuous Integration (CI) with GitHub Actions.

Up until now, you have been building your Docker images manually on your laptop. But DevOps is about automation. Our goal now is to configure GitHub to automatically test and build your code every time you merge a branch or push to main.

Here is how to set up your first CI pipeline.

* Step 1: Create the GitHub Actions Directory
GitHub Actions looks for a very specific folder structure in your repository to find automation scripts.

Open your devops-portfolio project in VS Code.

In the root of your project (the same level as app/ and docker-compose.yml), create a new folder named .github. (Do not forget the dot at the beginning!)

Inside the .github folder, create another folder named workflows.

Inside the workflows folder, create a file named ci.yml.

Your structure must look exactly like this:

Plaintext
devops-portfolio/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
├── docker-compose.yml
└── ...

* Step 2: Write the CI Pipeline
A GitHub Actions workflow is written in YAML. It defines "triggers" (when to run) and "jobs" (what to do). We are going to instruct GitHub to spin up a temporary Linux server in the cloud, install Python, and run a code linter (flake8) to ensure your Python code has no syntax errors before it gets built.

Copy and paste this code into your ci.yml file:

YAML
name: Continuous Integration

# 1. Trigger the workflow on pushes or pull requests to the main branch
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

# 2. Define the jobs to run
jobs:
  test-python-code:
    # Use a standard Ubuntu runner provided by GitHub
    runs-on: ubuntu-latest

    steps:
      # Step A: Download your repository's code onto the runner
      - name: Checkout Code
        uses: actions/checkout@v3

      # Step B: Install Python on the runner
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      # Step C: Install dependencies (Flask and Flake8 for linting)
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8
          if [ -f app/requirements.txt ]; then pip install -r app/requirements.txt; fi

      # Step D: Run the linter to check for syntax errors
      - name: Lint with Flake8
        run: |
          # Stop the build if there are Python syntax errors or undefined names
          flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
Save the file.

* Step 3: Push to GitHub and Trigger the Pipeline
Because our YAML file dictates that the pipeline runs on: push to main, simply pushing this new file to GitHub will trigger your very first automated run.

In your Ubuntu terminal, run:

Bash
git add .
git commit -m "Day 5: Add GitHub Actions CI workflow"
git push origin main
Step 4: Watch the Automation Live
Open your web browser and go to your devops-portfolio repository on GitHub.

Click the Actions tab near the top of the page.

You should see a workflow run titled "Day 5: Add GitHub Actions CI workflow" with a yellow spinning circle (in progress) or a green checkmark (success).

Click on the workflow run, and then click on the test-python-code job on the left to see the live terminal output from GitHub's cloud servers executing your exact steps!

## Branch: CD_pipeline_integration

### Day 6: Continuous Delivery (CD) to a Container Registry

Currently, our Docker image only exists on your laptop. If your CI pipeline passes, we want GitHub to automatically build a fresh, production-ready Docker image and store it securely in the cloud. We will use Docker Hub, the industry standard container registry, to store your built images.

Here are your steps to automate the Docker build and push process.

* Step 1: Generate a Docker Hub Access Token
Just like GitHub required a token instead of a password for terminal access, Docker Hub requires a token for automated pipelines.

Go to hub.docker.com and create a free account (if you do not have one already).

Log in and click your profile picture in the top-right corner, then select Account settings.

On the left sidebar, click Personal access tokens (under Security).

Click Generate New Token.

Name it GitHub Actions Pipeline and grant it Read & Write permissions.

Click Generate and copy the token immediately.

* Step 2: Add Secrets to GitHub
We must never put passwords directly into our ci.yml code. Instead, we store them in GitHub Secrets, which injects them safely into the runner when the pipeline executes.

Open your devops-portfolio repository on GitHub.

Click the Settings tab at the top.

On the left sidebar, scroll down to Secrets and variables and click Actions.

Click the green New repository secret button.

Create the first secret:

Name: DOCKERHUB_USERNAME

Secret: Type your exact Docker Hub username.

Click Add secret.

Click New repository secret again to create the second secret:

Name: DOCKERHUB_TOKEN

Secret: Paste the token you copied from Docker Hub.

Click Add secret.

* Step 3: Update Your Pipeline File
Now we will tell GitHub Actions to log into Docker Hub, build your task-api image, and push it to the internet if (and only if) the Flake8 linting passes.

Open .github/workflows/ci.yml in VS Code.

Add the Docker steps at the very bottom of the file. Your complete ci.yml must look exactly like this:

YAML
name: Continuous Integration

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test-python-code:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8
          if [ -f app/requirements.txt ]; then pip install -r app/requirements.txt; fi

      - name: Lint with Flake8
        run: |
          flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics

      # --- NEW DOCKER CD STEPS BELOW ---

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: ./app
          push: true
          # Tags the image with 'latest' and your unique GitHub commit ID
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/task-api:latest
            ${{ secrets.DOCKERHUB_USERNAME }}/task-api:${{ github.sha }}
Save the file.

* Step 4: Trigger the Automation
In your Ubuntu terminal, commit and push these changes to GitHub:

Bash
git add .github/workflows/ci.yml
git commit -m "Day 6: Add Docker build and push to pipeline"
git push origin main

Navigate to the Actions tab on your GitHub repository. You will see your pipeline running the new Docker steps. Once it turns green, log into Docker Hub in your web browser. You will see a brand new task-api repository containing the Docker image that GitHub built for you entirely hands-free.