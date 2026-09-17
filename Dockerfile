# Image that runs the test suite itself (not the browsers -- those live in the
# Selenium Grid node containers). It only needs Python + the deps.
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so Docker can cache this layer between runs.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the framework.
COPY . .

# Grid mode is the default inside Docker; the compose file points RUN_MODE and
# SELENIUM_REMOTE_URL at the hub service.
ENV RUN_MODE=grid \
    HEADLESS=true \
    SELENIUM_REMOTE_URL=http://selenium-hub:4444/wd/hub

# Default command runs the whole suite in parallel and writes Allure results.
CMD ["pytest", "-n", "2", "--dist", "loadfile"]
