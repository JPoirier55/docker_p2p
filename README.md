# Containerized peer to peer network

### Overview
This project is an undergraduate research project for Colorado State University Dept. of Electrical and Computer Engineering. Docker containers allow for separation and deployment completely independent of the underlying operating system. This allows for users to pack up, ship and move entire applications without having to reconfigure dependencies and source. 

In our case for this project, Docker is a new way to create a cluster of nodes that can be queried, and there are multiple tests and analysis that can be run. Because Docker containers can be built on the same OS, speeds between these can be extremely fast, so networking can be tested for any future research. 

This project will entail designing and developing a containerized peer to peer network which can be deployed and tested. Each peer will be hosted by a container, and the entire cluster of containers will make up a virtual peer to peer network. The design of the network will be designed based on the Gnutella model discussed below. This model is the simplest for having individual nodes which are identical and easily replicated. 

###Network Design
The entire project will be developed from scratch written in Python and Ansible. The end product will be a repository that can be cloned, deployed and run on any host, and replicated to the user’s needs. The structure for the network will be based on the design of Gnutella. 

In this design, the network does a periodic refresh when a query is made, to check the neighboring nodes. The node doing the querying will put out a request for a file including its address, which gets sent to all neighboring nodes. If these nodes have no file, but have other neighbors, the request is passed on, if not, the request comes back failure. Each node keeps a cache of its own neighbors, and when a new node is added, there is an update to the cache. If a node has the file requested, the address of the node doing the querying will be used to send the file back directly. 

In the Gnutella model, there is a set predetermine number of hops before there is a failure sent back from the entire system, usually 7. In this system the design will use a smaller maximum because there are much fewer nodes. 

The peer node must be able to handle both incoming queries, as well as send out queries. This allows the network to be replicated and deployed easily. This also replicates what real world networks typically look like because peers will download software which is run and used for both incoming and outgoing requests.

