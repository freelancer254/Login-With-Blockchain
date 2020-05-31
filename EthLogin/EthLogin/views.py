from django.shortcuts import render, redirect
from django.contrib import messages

#for RSA decryption
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode

#for Web3
import json
from web3 import Web3
from eth_account import Account

def loginView(request):
	if request.method=="POST":
		with open("EthLogin/keys/privatekey.pem","rb") as f:
			private_key_file = f.read()
		key = RSA.importKey(private_key_file)
		cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
		private_key_encrypted = request.POST.get('privatekey')
		private_key_decrypted = cipher.decrypt(b64decode(private_key_encrypted))
		private_key_decoded = private_key_decrypted.decode('utf-8','ignore')
		#retrieve the account from private key
		try:
			acct = Account.privateKeyToAccount(private_key_decoded)
			eth_address = acct.address
		except:
			messages.warning(request,'Enter a valid Private Key: This is invalid: {}'.format(private_key_decoded))
			return redirect('login')

		#check if the user is blocked
	
		#connect to the Ethereum blockchain
		infura_url = "ENTER YOUR INFURA RPC MAINNET KEY"
		web3 = Web3(Web3.HTTPProvider(infura_url))
		
		#check if blocked through the smart contract
		contract_address = "0x53b15e59E40ef73577B1e3e8Ee9d5359Ea7Cc86A"
		abi = json.loads('[{"inputs": [{"internalType": "address","name": "contractOwner","type": "address"}],"stateMutability": "nonpayable","type": "constructor"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "sender","type": "address"},{"indexed": false,"internalType": "address","name": "blocked","type": "address"}],"name": "allowAddressEvent","type": "event"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "sender","type": "address"},{"indexed": false,"internalType": "address","name": "unblocked","type": "address"}],"name": "blockAddressEvent","type": "event"},{"inputs": [{"internalType": "address[]","name": "addressToAllow","type": "address[]"}],"name": "allowAddress","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address[]","name": "addressToBlock","type": "address[]"}],"name": "blockAddress","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "addressToCheck","type": "address"}],"name": "checkBlockStatus","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "view","type": "function"}]')
		smart_contract = web3.eth.contract(address=contract_address, abi=abi)
		blocked = smart_contract.functions.checkBlockStatus(eth_address).call()
		if blocked:
			messages.warning(request,'This account is not allowed.')
		else:
			messages.success(request,'Login Successful')
		
		return redirect('login')

	else:
		#retrieve the RSA public key for encryption
		with open("EthLogin/keys/publickey.pem","rb") as f:
			public_key = f.read()
		context = {'public_key':public_key}
		return render(request,'login.html',context)