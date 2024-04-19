import sqlite3
import requests
import subprocess
import platform
import os
import json
import time
from packaging import version
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
STORAGE = os.getenv("STORAGE") or "versions.db"
DOCKER_USERNAME = os.getenv("DOCKER_USERNAME")
DOCKER_ACCESS_TOKEN = os.getenv("DOCKER_ACCESS_TOKEN")
IMAGE_NAME = os.getenv("DOCKER_IMAGE_NAME") or "kea-base"

if platform.system() == "Windows":
    # because of windows beeing windows
    login_command = f"docker login -u {DOCKER_USERNAME} --password \"{DOCKER_ACCESS_TOKEN}\""
else:
    login_command = f"echo \"{DOCKER_ACCESS_TOKEN}\" | docker login -u {DOCKER_USERNAME} --password-stdin"

# Database setup
conn = sqlite3.connect(STORAGE)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS processed_versions (version TEXT UNIQUE, processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, build_time INTEGER)''')
conn.commit()

def is_processed(version_str):
    """
    Helper function to check if version is already processed
    """
    c.execute("SELECT 1 FROM processed_versions WHERE version=?", (version_str,))
    return c.fetchone() is not None

def mark_processed(version_str, build_time):
    """
    Helper function to mark version as processed
    """
    c.execute("INSERT OR IGNORE INTO processed_versions (version, build_time) VALUES (?, ?)", (version_str,build_time,))
    conn.commit()

def should_skip(version_str):
    """
    Helper function to check if version should be skipped
    """
    try:
        parsed_version = version.parse(version_str)
        # Ignore below 1.0.0 or those with a pre-release suffix like "-beta" or a invalid formatted string
        if parsed_version < version.parse("2.0.0") or "-" in version_str or not "." in version_str:
            return True
    except:
        return True
    return False


# URL of the index page
url = 'https://downloads.isc.org/isc/kea/'

# Fetch the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
had_version = False

# all version folders are in <a> tags directly under <td class="indexcolname">
for node in soup.find_all('td', class_='indexcolname'):
#for node in reversed(soup.find_all('td', class_='indexcolname')): to start from the latest version
    link = node.find('a')
    if link and link.text.endswith('/'):
        start = time.time()
        version_str = link.text.strip('/')
        if not is_processed(version_str) and not should_skip(version_str):
            commands = [
                f"echo \"Processing version {version_str}\n\" > kea_builder.log",
                login_command,
                "docker buildx rm kea-builder || true",
                "docker buildx create --name kea-builder --use",
                "docker buildx use kea-builder",
                "docker buildx inspect --bootstrap",
                f"docker buildx build --platform linux/amd64,linux/arm64 --build-arg VERSION={version_str} -t {DOCKER_USERNAME}/{IMAGE_NAME}:{version_str} -t {DOCKER_USERNAME}/{IMAGE_NAME}:latest --push ."
            ]

            for command in commands:
                subprocess.run(command, shell=True, check=True)

            mark_processed(version_str, (time.time() - start) / 60)
            had_version = True

            message = {
                "embeds": [{
                    "title": f"{DOCKER_USERNAME}/{IMAGE_NAME}:{version_str} Built and Published",
                    "description": f"The docker image has successfully been built and published to docker-hub\n\nhttps://hub.docker.com/r/{DOCKER_USERNAME}/{IMAGE_NAME}/tags?name={version_str}",
                    "color": 36413
                }]
            }


            requests.post(WEBHOOK_URL, json=message)

conn.close()

if not had_version:
    print("No new versions found")
    exit(0)
