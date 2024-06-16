#mining of blockchain

from blockchain import Blockchian
import json
from flask import Flask,jsonify,request

app  = Flask(__name__)

#creating blockchain
blockchain = Blockchian()


#mining a blcok
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_proof)
    new_block = blockchain.create_block(proof,previous_hash)
    response = {'message' : 'congratulations u mined a block',
                'index' : new_block['index'],
                'timestamp' : new_block['timestamp'],
                'proof' : new_block['proof'],
                'previous_hash' : new_block['previous_hash']
                }
    return jsonify(response) , 200

#gettig full chain
@app.route('/get_chain' , methods = ['GET'])
def get_chain():
    response = { 'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response) , 200
#validating chain
@app.route('/is_valid' , methods=['GET'])
def is_valid():
    isValid =  blockchain.is_chain_valid(blockchain.chain)
    if(isValid):
        response = {'message' : 'chain is valid'}
    else:
        response = {'message' : 'chain not valid'}
    return jsonify(response) , 200
app.run(host='0.0.0.0' , port=5000)