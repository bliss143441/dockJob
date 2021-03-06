# Compose Exmaples

As Dockjob is designed to be run as part of a �docker stack� with Kong in front of it providing https and user accounts I have provided this section with a set of examples showing how it could be run. These examples should be run on a machine with a docker environment which is set up in a swarm. The commands should be run from a directory with the relevant .yml file.

To use these you need to arrange to set the following enviroment variables on the machine running docker swarm:
````
 | Variable Name | Example Value | Description |
 |---------------|---------------|-------------|
 | EXTURL | https://somefunnyhostname.com | URL users use to access web frontend  |
 | EXTPORT | 443 | Port users use to access web frontend |
````
I do this by adding 
````
export EXTURL=https://somefunnyhostname.com
export EXTPORT=443
````
to the end of ~/.bashrc

See [Enviroment Variables](../ENVVARIABLES.md) for documentation of possible container enviroment variables that can be used as settings.

# Dockjob Standalone
This uses docker to run dockjob standalone on a machine. This example shows setting dockjob options via environment variables. You must change the urls in docker-compose-standalone.yml replacing the host name with the hostname clients need to use to access dockjob.
Command to run:
````
docker stack deploy --compose-file=docker-compose-standalone.yml dockjob-standalone
````
Note: If you see a message that this node is not a swarm manager you may need to run docker swarm init

(For this option your EXTURL won't be SSL and your EXTPORT will be 80.
Now visit ${EXTURL}:${EXTPORT}/frontend

When done use 
````
docker stack rm dockjob-standalone
````
to halt the stack.

# Dockjob with https

The next example uses Kong to expose dockjob as https. For this to work you need to add two secrets to the swarm, 'webservices_cert' and 'webservices_key'. They contain the SSL certificate and SSL key that the server will use. An example command to create them is here:

````
docker secret create webservices_cert - <<EOF
**FILE HERE**
EOF
````

Replace **FILE HERE** with the actual certificate file contents. Repeat for the key.

To use SSL you will need a proper hostname. Take the file docker-compose-https.yml and replace cat-sdts.metcarob-home.com with your own hostname.

Command to run:
````
docker stack deploy --compose-file=docker-compose-https.yml dockjob-https
````

You may need to wait a bit as the database is created and Kong is setup.

Now visit https://** YOU HOST **:443/frontend
You should notice you now have a https connection.

Use the docker stack rm command to stop the services.

# Dockjob with https and user auth

The final exmaple builds on the previous one by configuring Kong to only allow access to the dockjob api with a username and password. Dockjob is also configured to tell it's frontend component to prompt for a log on by setting the APIAPP_APIACCESSSECURITY enviroment variable.

You will again have to change the hostname in X and run this command to start the stack:
````
docker stack deploy --compose-file=docker-compose-https-basic-auth.yml dockjob-https-basic-auth
````

Now visit https://** YOU HOST **:443/frontend
The username and password is sampleuser - this can be changed in the compose file. I expect most deployments would migrate this password into a docker secret.

Use the docker stack rm command to stop the services.

# Dockjob with external hostname passed in via a secret

The application requires knowldege of the external url the users use to access the service. This is so the frontend app can correctly call the API. In my use case for dockJob I have a docker secret set up with the external host name. (This drives the SSL certificate process) It is useful for me that dockJob can pick up the hostname from this secret. Unfortunatly it is required in mutiple enviroment variables in different ways. To resolve this I have implemented a method that will allow another enviroment variables to be refered to. This compose file demos this.

To use it create a secret:
````
echo "somefunnyhostname.com" | docker secret create webservices_hostname -
````

Execute the compose file
````
docker stack deploy --compose-file=docker-compose-hostname-from-secret.yml dockjob-hnsecret
````

Finally use the docker logs command and verify the values were set correctly.



