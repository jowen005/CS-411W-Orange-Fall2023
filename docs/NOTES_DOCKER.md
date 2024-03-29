# Docker Notes
## Conceptual Basics
* Container Concept
  * A way to package an application with all the necessary dependencies and configurations
  * Portable and easily shared
  * Makes development and deployment more efficient
  * Everything in isolated environment

* Container Repository
  * Where containers "live"
  * They can be private or public (DockerHub)

* Docker vs Virtual Machine
  * Docker virtualizes the Applications layer
    * uses the kernel of the host
    * smaller size
    * start and run faster
    * cant run on older machines bc its not compatible with docker images (fix: use Docker Toolbox)
  * VM virtualizes the OS kernel and the Applications layer (complete OS)
    * larger and slower start/stop times
    * any VM can run on any OS host

# Technical Basics
* Containers (running)
  * Made up of layers of images (stacked)
  * A running environment for an image
  * Consists of the:
    * Application Image (postgres, redis, mongo, mysql)
    * Environment Configs (port bindings)
    * Virtual File System
  * When you restart a container, all data in app is lost (no data persistence)

* Images (not running)
  * The actual package together with configuration and script
  * Images are built/stacked on one another
  * Types of Images:
    * Application image: on the top of the stack (ex. mongo, mysql, redis)
    * Intermediate image: images in between the base and application image
    * Base image: at the base of the stack (often Linux b/c small in size)
  * In order to delete an image, the container that uses it must be deleted first

* Container vs Host Ports
  * Multiple containers can run on host machine
  * The host machine only has certain port available
  * A host port can only be used by one thing at a time
  * If containers have the same port number, then they must be bound to different host ports

* Workflow with Docker (db could be other types of microservices too i.e. redis)
  * Get db image from DockerHub
  * Develop app on local machine
  * Push app to github
  * CI tool (Actions/Jenkins) builds app and creates app Docker image
  * CI tool pushes app image to private Docker Repository
  * Dev Server pulls app image from Repo and db image from DockerHub
  * End with 2 containers running together on dev server

* Docker Network
  * Docker can create an isolated Docker network that containers can run in
  * Containers in a Docker Network and can talk to eachother using just a container name without localhost port numbers 

* Dockerfile
  * A Dockerfile builds a Docker image from an application
  * A Dockerfile is a blueprint for building Docker images
  * Reserved words:
    * **FROM** --> used to base Dockerfile off of some base image (usually off DockerHub)
    * **ENV** --> used to declare environmental variables (some can be set in docker-compose instead)
    * **RUN** --> executes a Linux command inside the container environment
      * You can have multiple
      * *mkdir* --> directory would be created inside the container
    * **COPY** --> executes on the host environment
      * 1st arg: host path (source)
      * 2nd arg: container path (target)
    * **CMD** --> executes an entry point Linux command (something that starts the app or server)
      * Only one is allowed
  * Building an image from docker file
    * Use **docker build**
  * Whenever you adjust a Dockerfile, you MUST rebuild the image

Private Docker Repositories
* Common options (Amazon ECR, DockerHub, Canister, etc)
* Steps to push to a private repo
  1. Give system permission to push (login)(different ways of doing this depending on repo)
     * **docker login -u __username__**
  2. Build docker image
  3. Tag your image to include the repository address in the name
     * **docker tag __imageid__ __username__/__reponame__:__tag__**
  4. Push image to the respitory address
     * **docker push __username__/__reponame__:__tag__**
  * If you change something in the image or the code, you must re-tag the image, and push again
* Steps to pull from a private repo
  1. Give remote server permission to pull (login)
  2. Create docker-compose file on remote server
   * In the docker-compose file, set the app's image to the imageURI which includes the repository address

Docker Volumes
* A container has a virtual file system where the data is usually stored
  * However, there is not data persistence (data is lost when container restarts)
* With Docker Volumes, a folder in the physical host file system is *mounted* into the virtual file system of the Docker container
  * When a container writes to its file system, it gets replicated (auto-written) to the host file system
  * This way, when a container restarts, it grabs the data from the host file system
* Volume Types:
  1. Host Volume
     * You decide where on the host file system the reference is made
     * **docker run -v __hostpath__:__containerpath__**
  2. Anonymous Volume
     * For each container, a folder is generated that gets mounted (host path is not specified)
     * Folder is automatically generated by Docker
     * **docker run -v __containerpath__**
  3. Named Volume
     * Similar to anonymous volume, however, you can reference the volume by name
     * Should be used in production bc you let Docker worry about volume locations on host
     * **docker run -v __name__:__containerpath__**'
* Docker Volume Locations
  * Windows
    * C:\ProgramData\docker\volumes
  * Linux
    * /var/lib/docker/volumes
  * Mac
    * /var/lib/docker/volumes
    * Docker creates a Linux VM and stores all the Docker data there

## Commands
Misc Commands
* **docker pull _____** --> Pulls an image from DockerHub
* **docker build -t __imagename__:__tag__ __pathtoDockerfile__** --> builds image from Dockerfile

Starting and Stopping Images/Containers
* **docker run __image__** --> Runs/Starts an image (searches DockerHub if not found locally, pulls, and runs)
  * **docker run -d __image__** --> Runs image in detached mode (no CLI interface for container)
  * **docker run -p__hostport__:__containerport__ __image__** --> Binds a container port to a host port and runs
  * **docker run --name __customname__ __image__** --> Runs an image under a custom name
  * **docker run -e __environvariable__ __image__** --> Include environmental variables in image when running
  * **docker run --net __networkname__ __image__** --> Run image in a network
* **docker stop __containerid__** --> Stops container
* **docker start __containerid__** --> Starts container

Interactive Container Terminal
* **docker exec -it __containerid__ /bin/bash** --> Opens interactive terminal inside container
  * type **exit** to exit
  * you can substitute **containerid** for **containername**
  * if **/bin/bash** doesn't work use **/bin/sh**

Viewing Container/Image Info
* **docker ps** --> Shows all running containers
  * **docker ps -a** --> Shows all running and nonrunning containers
* **docker images** --> Shows all images
* **docker logs __containerid__** --> Displays logs of container
  * **docker logs __containername__** --> Displays logs of container

Deleting Containers/Images
* **docker rm __containerid__** --> Removes a container
* **docker rmi __imageid__** --> Removes an image

Network Commands
* **docker network ls** --> Display all networks
* **docker network create __networkname__** --> Creates a Docker Network

# Docker Compose Notes
## Basics
* Concept
  * Creates a convenient and automated way to create Docker Networks and initializing containers
  * When converting from using networks to Docker Compose, all info in container 'run' commands are stored under each separate service
* Volumes
  * When using Named Volumes in docker-compose, you must list all Volume names at the end of the file

## Commands
* **docker-compose up** --> creates and starts all containers
  * **docker-compose -f __dcfile__ up** --> specifies a file to start from
* **docker-compose down** --> shuts down all containers and removes network


