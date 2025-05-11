# --- DEPLOYMENT SCRIPT (deploy.sh) ---
# Save this as deploy.sh and run it on AWS EC2
# Make sure to chmod +x deploy.sh before running

#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-dev -y

# Install virtual environment
pip3 install virtualenv

# Create venv
virtualenv venv
source venv/bin/activate

# Install dependencies
pip install flask flask_sqlalchemy weasyprint gunicorn

# Open port 5000 if needed
sudo ufw allow 5000

# Run the app
export FLASK_APP=app.py
flask run --host=0.0.0.0
