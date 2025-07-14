# P2P Blockchain Network Simulation

This project implements a basic peer-to-peer (P2P) blockchain simulation using Python and Flask. Each node operates independently, maintaining its own copy of the blockchain, and communicates with other nodes to share blocks, transactions, and resolve conflicts using a simple consensus mechanism.

## Overview

The goal of this simulation is to demonstrate how a decentralized blockchain network operates in practice. It includes core blockchain components such as transactions, proof-of-work mining, peer discovery, and chain resolution, all integrated with a minimal user interface for ease of interaction and visualization.

## Features

- Implementation of a basic blockchain structure with blocks, transactions, and hashes
- Mining logic using a simplified Proof-of-Work (PoW) algorithm
- Transaction creation and inclusion into blocks
- Node registration and peer-to-peer communication
- Longest chain consensus to resolve conflicts across nodes
- Web interface to visualize the blockchain and interact with the network


## Project Structure

project/
│
├── blockchain.py         # Blockchain logic and data structure
├── node.py               # Flask-based web server and REST API
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Frontend interface for blockchain explorer
└── static/
    └── style.css         # Styling for the frontend UI


## Running the Simulation

Open separate terminals to run multiple nodes on different ports:

```bash
# Terminal 1
python node.py -p 5000

# Terminal 2
python node.py -p 5001

# Terminal 3
python node.py -p 5002
```

Then access each node in your browser:

- http://localhost:5000
- http://localhost:5001
- http://localhost:5002


## Using the Web Interface

- **Connected Peers**: Register other running nodes to establish communication.
- **Blockchain View**: Inspect blocks, transactions, and hash values visually.
- **New Transaction**: Submit transactions between users.
- **Mine Block**: Solve the proof-of-work puzzle and add a new block.
- **Resolve Chain**: Synchronize the blockchain by adopting the longest valid chain among peers.