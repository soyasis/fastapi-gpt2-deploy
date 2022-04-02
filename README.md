## TODOS
- available on all ports
  - maybe follow example with port 8080 instead of 8000
  - add https

# Deployment

## Setup AWS EC2 Instance running FastAPI App
Main reference: https://markus-hinsche.github.io/tut-practical-aspects-of-ml/#33

0. Setup EC2 Instance (via AWS console)
For PyTorch models use a t2.medium ubuntu instance

1. Open Ports (via console)
go to 'Security groups' and c'lick launch-wizard-1'
SSH (leave as is)
HTTP  TCP 80  0.0.0.0/0
HTTP  TCP 80  ::/0
HTTPS TCP 443 0.0.0.0/0
HTTPS TCP 443 ::/0

2. SSH to instance
`ssh -i "KeyName.pem" ubuntu@ec2-52-29-80-212.eu-central-1.compute.amazonaws.com`

*If you encounter an error saying: It is required that your private key files are NOT accessible by others, then run this command (once) before you run ssh:*
`chmod 600 path/to/KeyName.pem`

2.1 Update packages
`sudo apt-get update`
`sudo apt-get install  git-lfs`

3. Clone your repo
`git clone https://github.com/your-repo`

*for large files (i.e. model) you need to instal git LFS*

`git lfs pull`

4. Install python3 in ubuntu instance
`sudo apt install python3.8`

5. Install Python Virtual Machine
`sudo apt-get install python3.8-venv`

6. Create Python3 venv inside app
`python3.8 -m  venv venv`

7. activate env
`. venv/bin/activate`

8. Upgrade pip
`pip install --upgrade pip`

9. Install requirements.txt
`pip install -r ../requirements.txt`

*if not in requirements make sure to install the follwing:*
`pip install fastapi uvicorn gunicorn`

*if torch install gets killed try without cashing*
`pip install -r ../requirements.txt --no-cache-dir`

10. Route Ports
`sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8000`

11. Initiate FastAPI
`uvicorn main:app --host="0.0.0.0" --port=8000`

12. Open public IPv4 address
http://3.68.197.29/docs


## Configure instance to keep running

1. create in the repo's root dir a `supervisor.conf` file with the following:
```
[program:webservice]
command=/home/ubuntu/fastapi-gpt2-deploy/app/venv/bin/gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker main:app
directory=/home/ubuntu/fastapi-gpt2-deploy/app/
user=ubuntu
autostart=true
autorestart=true
stderr_logfile=/var/log/fastapi-gpt2-deploy/app/app.err.log
stdout_logfile=/var/log/fastapi-gpt2-deploy/app/app.out.log
```
*to enable the log files you will need to make a directory in var/log/*

2. Install Supervisor
`sudo apt install supervisor`

3. link config file
`sudo ln -s /home/ubuntu/fastapi-gpt2-deploy/supervisor.conf /etc/supervisor/conf.d`

4. Restart and check Supervisor
`sudo /etc/init.d/supervisor restart`
`sudo supervisorctl status`
