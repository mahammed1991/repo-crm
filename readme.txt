Installing Google Portal

1. Clone the google-portal repository into your local system

hg clone https://<username>@bitbucket.org/regalix/google-portal

2. Set up server configuration using vagrant in local machine to avoid conflicts
    a. Download virtual box debian package and install(https://www.virtualbox.org/wiki/Linux_Downloads)
    b. Download vagrant debian package and install(https://www.vagrantup.com/downloads.html)
    c. install ansible to configure virtual machine(http://docs.ansible.com/intro_installation.html)

3. Run command "vagrant up" to configure VM

4. Connect to VM using command "vagrant ssh"

5. Code will be available under vagrant directory(cd /vagrant/)

6. Activate pre installed virtualenv 'google-portal'(source /opt/python/venv/google-portal/bin/activate)

7. Run the application(python manage.py runserver 0.0.0.0:8000)

8. Access the application on - http://127.0.0.1:5000