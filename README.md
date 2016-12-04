# Containerized peer to peer network

### Dev env setup
```
 git clone https://github.com/jpoirier55/docker_p2p
 cd docker_p2p
 docker build -f Dockerfile .
```
### Setup master node 
```
docker run -d -e PORT_NUM=8001 -e TCP_PORT_NUM2=65501 -e TCP_PORT_NUM=65001 -p 8001:8001 <docker image ID>
```
PORT_NUM: port for running Django webserver
TCP_PORT_NUM: port for TCP downloading server
TCP_PORT_NUM2: port for TCP split uploading server

### Setup file nodes
```
docker run -d -e PORT_NUM=8002 -e TCP_PORT_NUM2=65502 -e TCP_PORT_NUM=65002 -p 8002:8002 <docker image ID>
docker run -d -e PORT_NUM=8003 -e TCP_PORT_NUM2=65503 -e TCP_PORT_NUM=65003 -p 8003:8003 <docker image ID>
```

### To set file nodes see wiki at 

