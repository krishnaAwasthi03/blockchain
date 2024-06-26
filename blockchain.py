#libraries needed

import datetime
import hashlib
import json


#Part 1- Creating a Blockchain

class Blockchian:
    def __init__ (self):
        self.chain = []
        self.create_block(proof = 1,  previous_hash = '0')
    def create_block(self, proof, previous_hash):
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : str(datetime.datetime.now()), 
            'proof' : proof,
            'previous_hash' : previous_hash
        }
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return self.chain[-1]
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else :
                new_proof += 1
        return new_proof
    def hash(self, block):
        encoded_block = json.dumps(block).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            hash_previous_block = self.hash(previous_block)
            #checking the hash of previous block
            if(current_block['previous_hash'] != hash_previous_block):
                return False
            #checking proof
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            hahs_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            if(hahs_operation[:4] != '0000'):
                return False
            previous_block = current_block
            block_index += 1
        
        return True
    
