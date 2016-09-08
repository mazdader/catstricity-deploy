# catstricity-deploy
Django+Ansible application for catstricity deployments. Can be used in two ways: local installation and Docker container.

## Depoy and run local instance

### Requirements

* Ansible 2.0+: [Ansible Installation](http://docs.ansible.com/ansible/intro_installation.html)
* _python 2.7_ and _Django 1.10.1_:

```bash
$ sudo apt-get install python-pip
$ sudo pip install django==1.10.1
$ python -m django --version
1.10.1
```
* _Git_:
```bash
$ sudo apt-get install git
```

### Checkout the repository
```bash
$ git clone https://github.com/mazdader/catstricity-deploy.git
```

### Prepare configuration file

Edit _catstricity-deploy/app/app/settings.py_ configuration file - set proper values for `ANSIBLE_HOSTS_FILE`, `ANSIBLE_USERNAME`, `SSH_PRIVATE_KEY_PATH` variables:
* `ANSIBLE_HOSTS_FILE`: path to your Ansible inventory file (see example _hosts_sample_);
* `ANSIBLE_USERNAME`: the username that you want to log in to your servers (default - `ec2-user`);
* `SSH_PRIVATE_KEY_PATH`: absolute path tou you Private SSH key (defaults to `$HOME/.ssh/id_rsa`).

### Run the application
```bash
$ cd catstricity-deploy/app
$ python manage.py runserver 0.0.0.0:8000
```

WEB IU will be accessible at `http://<host_IP>:8000` URL.

## Build and run Docker container

### Requirements

* Checkout the repository:
```bash
$ git clone https://github.com/mazdader/catstricity-deploy.git
```

* Install [Docker](https://docs.docker.com/engine/installation/).
* Put your Private SSH key into repository root.
* Put your Ansible playbook inventory file into repository root.

### Build Docker image

```bash
$ docker build --build-arg ANSIBLE_SSH_KEY=<SSH private key filename> --build-arg HOSTS_FILE=<inventory filename> -t catstricity-deploy .
```

### Run a container with catstricity-deploy application

```bash
$ docker run -d -p 8000:8000 --name catstricity-deploy catstricity-deploy
```

WEB IU will be accessible at [http://localhost:8000](http://localhost:8000) URL.

## WEB UI short description

Clicking on server name as well as on _Run_ link immediatly starts deployment. Clicking on _View results_ link shows output of latest deployment.
