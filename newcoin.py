import datetime 
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

#creating blockchain
class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        #creating mempool
        self.mempool = []
        self.createblock(proof = 1 , previous_hash = '0')
        #adding nodes 
        self.nodes = set()
    def create_block(self,proof , previous_hash):
        block  = {'index' : len(self.chain) + 1, 
                  'timestamp' : str(datetime.datetime.now()),
                  'proof' : proof, 
                  'previous_hash' : previous_hash,
                  'transactions' : self.mempool}
        self.mempool = []
        self.chain.append(block)
        return block
    
    def last_block(self):
        return self.chain[-1]
    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True: 
            hash_operation = hashlib.sha256(str(new_proof**22 + previous_proof**2 - new_proof**3 + previous_proof**4).encode()).hexdigest()
            if(hash_operation[:4] == '0000'):
                return new_proof
            else:
                new_proof += 1
    def hash(self, block):
        return hashlib.sha256(json.dumps(block , sort_keys=True).encode()).hexdigest()
    def is_valid_blockchain(self, chain):
        previous_block = chain[0]
        previous_proof = previous_block['proof']
        index = 1
        while index < len(chain) : 
            current_block = chain[index]
            current_proof = current_block['proof']
            #checking previous hash 
            previous_hash = self.hash(previous_block)
            if(previous_hash != current_block['previous_hash']):
                return False
            #checking previous proof
            proof = hashlib.sha256(str(current_proof**22 + previous_proof**2 - current_proof**3 + previous_proof**4).encode()).hexdigest()
            if(proof[:4] != '0000'):
                return False
            previous_block = current_block
            index += 1
            
        return True
    #adding transaction
    def add_transaction(self, sender, receiver, exchange):
        self.mempool.append({
            'sender' : sender,
            'receiver' : receiver,
            'exchange' : exchange
        })
        previous_block = self.last_block()
        return previous_block['index'] + 1
    #adding nodes
    def add_nodes(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self) :
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for nodes in network : 
            response = requests.get(f'http://{nodes}/get_chain')
            if(response.status_code == 200):
                length = response.json()['length']
                chain = response.json()['chain']
                if(max_length < length and self.is_valid_blockchain(chain)):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

#creating mining funtions

app = Flask(__name__)

#creating an address for a node
node_address = str(uuid4()).replace('-' ,'')

#creating block chain
blockchain = Blockchain()

@app.route('/mine_block' , methods= ['GET'])
def mine_block():
    previous_block = blockchain.last_block()
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_block['proof'])
    blockchain.add_transaction(sender = node_address , receiver = 'Krishna' , exchange = 0.03)
    new_block = blockchain.create_block(proof , previous_hash)
    return jsonify(new_block) , 200

@app.route('/get_chain' , methods= ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain , 
                'length' : len(blockchain.chain)}
    return jsonify(response) , 200
@app.route('/is_valid', methods = ['GET'])
def is_chain_valid():
    validity = blockchain.is_valid_blockchain(blockchain.chain)
    response = { 'is_valid' : str(validity)}
    return jsonify(response) , 200

#adding transactions
@app.route('/add_transaction' , methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys= ['sender' , 'receiver' , 'exchange']
    response = {}
    status_code = 0
    if(not(json[keys] for keys in transaction_keys)):
        response  = {
            'message' : 'some elements missing/extra in the given data'
        } 
        status_code = 400
    index = blockchain.add_transaction(json['sender'] , json['receiver'] , json['exchange'])
    response = {
        'messeage' : f'transaction added to {index} block'
    }
    status_code = 201
    return jsonify(response) , status_code
        
#adding nodes
@app.route('/add_node',  methods=['POSTS'])
def add_node():
    json = json.get_json()
    nodes = json.get('nodes')
    if node is None:
        return "No Node", 400
    
    for node in nodes:
        blockchain.add_node(node)
    response = { 'messages' : 'all the nodes are shown below',
                'total_nodes' : list(blockchain.nodes)
                }
    return jsonify(response) , 201

#creating census
@app.route('/check_chain', methods=['POSTS'])
def check_chain():
    is_chain_replace = blockchain.replace_chain(blockchain.nodes)
    if(is_chain_replace):
        response = {
            'message' : 'the chain is replaced with longest chian',
            'updated_chain' : blockchain.chain
            }
    else :
        response = {
            
                }
app.run('0.0.0.0' , port = 5000)
