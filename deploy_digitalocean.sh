#!/bin/bash
# DigitalOcean Deployment Script

echo "🚀 Deploying to DigitalOcean..."

# 1. Create requirements.txt
cat > requirements.txt << 'REQS'
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
blockfrost-python==0.6.0
requests==2.32.5
beautifulsoup4==4.12.3
python-dotenv==1.0.0
jsonschema==4.25.1
REQS

# 2. Create Procfile
echo "web: gunicorn server:app --bind 0.0.0.0:\$PORT" > Procfile

# 3. Create runtime.txt
echo "python-3.11" > runtime.txt

# 4. Create app.yaml for DigitalOcean
cat > .do/app.yaml << 'YAML'
name: midnight-infrastructure
services:
- name: web
  github:
    repo: Allreality/midnight-infrastructure
    branch: main
  run_command: gunicorn server:app
  environment_slug: python
  instance_size_slug: basic-xxs
  instance_count: 1
  http_port: 8080
  routes:
  - path: /
  envs:
  - key: BLOCKFROST_PROJECT_ID
    scope: RUN_TIME
    type: SECRET
  - key: TREASURY_ADDRESS
    scope: RUN_TIME
    value: addr1q9np4m2eg4xtr8kn6mvccwklpv6a7kxhq8uqkk45gpd2tz326xxqn233h4a3lf5yv3utg7lwlg0vheasx9zjvzyfy8kqs0gpcx
YAML

echo "✅ Deployment files created"
echo ""
echo "Next steps:"
echo "1. Push to GitHub"
echo "2. Connect to DigitalOcean App Platform"
echo "3. Deploy!"
