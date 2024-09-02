import os

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()


class SepoliaChain:
    # sepolia测试网
    chain_id = 11155111
    rpc_url = "https://rpc.sepolia.org"


# 合约地址
contract_address = "0x800eC0D65adb70f0B69B7Db052C6bd89C2406aC4"  # Sepolia Elixir 领水合约地址

# 合约 ABI（这是一个示例 ABI，实际使用时需要用你的合约的 ABI）
contract_abi = [
    {
        "constant": False,
        "inputs": [{"name": "a", "internalType": "address", "type": "address"}],
        "name": "maxMint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


# 账户地址和私钥（仅示例，不要在实际场景中使用）
# todo
from_address = os.getenv("from_address")
private_key = os.getenv("private_key")

web3 = Web3(Web3.HTTPProvider(SepoliaChain.rpc_url))

# 测试网络联通状态
web3.is_connected()

# 创建合约实例
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

while True:
    # 获取地址余额
    wallet = web3.to_checksum_address(from_address)
    wei = web3.eth.get_balance(wallet)
    balance = web3.from_wei(wei, "ether")
    print(f"余额为:{balance} ETH")

    # 构建交易
    print(f"gas:{web3.eth.gas_price}")
    ## 交易计数flag
    nonce = web3.eth.get_transaction_count(web3.to_checksum_address(from_address))
    print(f"nonce:{nonce}")

    # type2 交易参数（EIP-1559）
    transaction = {
        "chainId": SepoliaChain.chain_id,  # 1 为以太坊主网
        "type": "0x02",
        "value": web3.to_wei(0, "ether"),
        "nonce": nonce,
    }

    ## 构建合约交互参数
    transaction = contract.functions.maxMint(
        web3.to_checksum_address(from_address)
    ).build_transaction(transaction)

    # 签名交易
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # 发送交易
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # 打印交易哈希
    print(f"Transaction sent with hash: {txn_hash.hex()}")

    # 等待交易确认
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    print(f"Transaction receipt: {txn_receipt}")
