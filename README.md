# Health Fair App

Vital Signs Hackathon Project

## Setup

Create virtualenv:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure that AWS credentials are set up through `aws-cli`, then run
`python manage.py setup_dynamodb` and then `.deploy.sh`
