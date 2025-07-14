import sys
import json
from uuid import uuid4
from flask import Flask, jsonify, request, render_template
from urllib.parse import urlparse
import requests
from blockchain import Blockchain

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()
peers = set()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])

    # No mining reward (removed)
    block = blockchain.new_block(proof)

    return jsonify({
        'message': 'New Block Forged',
        'block': block,
    }), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    return jsonify({'message': f'Transaction will be added to Block {index}'}), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }), 200


@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify({'peers': list(peers)}), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        parsed_url = urlparse(node)
        if parsed_url.netloc:
            peers.add(parsed_url.netloc)
        elif parsed_url.path:
            peers.add(parsed_url.path)
        else:
            return f'Invalid URL: {node}', 400

    return jsonify({'message': 'New nodes have been added', 'peers': list(peers)}), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = resolve_conflicts()
    message = 'Our chain was replaced' if replaced else 'Our chain is authoritative'
    return jsonify({'message': message, 'chain': blockchain.chain}), 200


def resolve_conflicts():
    global blockchain
    neighbours = peers
    new_chain = None
    max_length = len(blockchain.chain)

    for node in neighbours:
        try:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and valid_chain(chain):
                    max_length = length
                    new_chain = chain
        except:
            continue

    if new_chain:
        blockchain.chain = new_chain
        return True

    return False


def valid_chain(chain):
    for i in range(1, len(chain)):
        block = chain[i]
        prev_block = chain[i - 1]

        if block['previous_hash'] != prev_block['current_hash']:
            return False

        if not blockchain.valid_proof(prev_block['proof'], block['proof']):
            return False

    return True


if __name__ == '__main__':
    port = 5000
    if len(sys.argv) == 3 and sys.argv[1] == '-p':
        port = int(sys.argv[2])
    app.run(host='0.0.0.0', port=port)


