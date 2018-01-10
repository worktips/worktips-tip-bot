from typing import List, Dict

from m0rkcoin_tip_bot import rpc_client


def register() -> str:
    result = rpc_client.call_method('createAddress')
    return result['address']


def get_wallet_balance(address: str) -> Dict[str, int]:
    result = rpc_client.call_method('getBalance', {'address': address})
    return result


def get_all_balances(wallet_addresses: List[str]) -> Dict[str, Dict]:
    wallets = {}
    for address in wallet_addresses:
        wallet = rpc_client.call_method('getBalance', {'address': address})
        wallets[address] = wallet
    return wallets
