# Indexer for Ethereum to get transaction list by ETH address
# https://github.com/Adamant-im/ETH-transactions-storage
# By Artem Brunov, Aleksei Lebedev. (c) ADAMANT TECH LABS
# v. 1.1

from web3 import Web3
import psycopg2
import time
import sys
import logging
import configparser
from web3.middleware import geth_poa_middleware



cp=configparser.ConfigParser()
cp.read("config.ini")
node_address = cp.get('base','node_address')
log_file_path = cp.get('base','log_file_path')
start_block_number = cp.get('base','start_block_number')

db_host = cp.get('db','host')
db_user = cp.get('db','user')
db_password = cp.get('db','password')

# Get postgre database name
if len(sys.argv) < 2:
    print('Add postgre database name as an argument')
    exit()

dbname = sys.argv[1]

# Connect to geth node
#web3 = Web3(Web3.IPCProvider("/home/geth/.ethereum/geth.ipc"))

# Or connect to parity node
#web3 = Web3(Web3.IPCProvider("/home/parity/.local/share/io.parity.ethereum/jsonrpc.ipc"))
web3 = Web3(Web3.HTTPProvider(node_address))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
abi=[{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"}]
erc = web3.eth.contract(abi=abi)
transfer_topic="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
abi_721=[{"constant":False,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"mint","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"approved","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"constant":True,"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"}]
erc_721 = web3.eth.contract(abi=abi_721)

# Start logger
logger = logging.getLogger("EthIndexerLog")
logger.setLevel(logging.INFO)
lfh = logging.FileHandler(log_file_path)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
lfh.setFormatter(formatter)
logger.addHandler(lfh)

try:
    conn = psycopg2.connect(dbname=dbname, host=db_host, user=db_user, password=db_password)
    conn.autocommit = True
    logger.info("Connected to the database")
except:
    logger.error("Unable to connect to database")

# Delete last block as it may be not imparted in full
cur = conn.cursor()
cur.execute('DELETE FROM public.ethtxs WHERE block = (SELECT Max(block) from public.ethtxs)')
cur.close()
conn.close()

# Adds all transactions from Ethereum block
def insertion(blockid, tr):
    tx_count = 0
    time = web3.eth.getBlock(blockid)['timestamp']
    for x in range(0, tr):
        trans = web3.eth.getTransactionByBlock(blockid, x)
        txhash = trans['hash']
        value = trans['value']
        inputinfo = trans['input']
        fr = trans['from']
        to = trans['to']
        gasprice = trans['gasPrice']
        tx_receipt= web3.eth.getTransactionReceipt(trans['hash'])
        gas =tx_receipt['gasUsed']
        contract_to = ''
        contract_value = ''
        # Check if transaction is a contract transfer
        if len(tx_receipt['logs']) > 0 :
            for log in tx_receipt['logs']:
                log_addr = log['address'].lower()
                if len(log['topics'])> 0 and log['topics'][0].hex() == transfer_topic :
                    try:
                        event = erc.events.Transfer().processLog(log)['args']
                        contract_to = "0"*(64-len(event['to'][2:]))+event['to'][2:]
                        contract_value = "0"*(64-len(hex(event['value'])[2:]))+hex(event['value'])[2:]
                    except Exception as e:
                        try:
                            event = erc_721.events.Transfer().processLog(log)['args']
                            contract_to = "0"*(64-len(event['to'][2:]))+event['to'][2:]
                            contract_value = hex(event['tokenId'])[2:]
                        except Exception as e:
                            continue
                    logger.info(contract_to)
                    logger.info(contract_value)
        # if inputinfo.startswith('0xa9059cbb'):
        #     contract_to = inputinfo[10:-64]
        #     contract_value = inputinfo[74:]
        if fr is not None:
            fr = fr.lower()
        if to is not None:
            to = to.lower()
        if txhash is not None:
            txhash = txhash.hex().lower()
        if contract_to is not None:
            contract_to = contract_to.lower()
        if contract_value is not None:
            contract_value = contract_value.lower()
        cur.execute(
            'INSERT INTO public.ethtxs(time, txfrom, txto, value, gas, gasprice, block, txhash, contract_to, contract_value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (time, fr, to, value, gas, gasprice, blockid, txhash, contract_to, contract_value))
        tx_count+=1
    logger.info('Block ' + str(blockid) + ' contain ' + str(tx_count) + ' transactions')

# Fetch all of new (not in index) Ethereum blocks and add transactions to index
while True:
    try:
        conn = psycopg2.connect(dbname=dbname, host=db_host, user=db_user, password=db_password)
        conn.autocommit = True
    except:
        logger.error("Unable to connect to database")

    cur = conn.cursor()

    cur.execute('SELECT Max(block) from public.ethtxs')
    maxblockindb = cur.fetchone()[0]
    # On first start, we index transactions from a block number you indicate. 46146 is a sample.
    if maxblockindb is None:
        maxblockindb = int(start_block_number)
    if maxblockindb < int(start_block_number):
        maxblockindb = int(start_block_number)

    endblock = int(web3.eth.blockNumber)

    logger.info('Current best block in index: ' + str(maxblockindb) + '; in Ethereum chain: ' + str(endblock))

    for block in range(maxblockindb + 1, endblock):
        transactions = web3.eth.getBlockTransactionCount(block)
        if transactions > 0:
            insertion(block, transactions)
        else:
            logger.info('Block ' + str(block) + ' does not contain transactions')
    cur.close()
    conn.close()
    time.sleep(20)
