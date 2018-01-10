from typing import Dict

from m0rkcoin_tip_bot import models, wallet


def register_user(user_id: str, user_wallet: str) -> models.User:
    balance_address = wallet.register()
    user_model = models.User(user_id=user_id, user_wallet_address=user_wallet,
                             balance_wallet_address=balance_address)
    user_model.save()
    models.Wallet(wallet_address=balance_address).save()
    return user_model


def get_wallet_balance(user_id: str) -> Dict[str, int]:
    user: models.User = models.User.objects(user_id=user_id).first()
    if not user:
        return {}
    balance = wallet.get_wallet_balance(user.balance_wallet_address)
    return balance


def update_balances():
    print('Updating all wallet balances')
    wallets = models.Wallet.objects
    wallet_addresses = [w.wallet_address for w in wallets]
    balances = wallet.get_all_balances(wallet_addresses)
    for address, details in balances.items():
        wallet_doc: models.Wallet = models.Wallet.objects(
            wallet_address=address).first()
        wallet_doc.actual_balance = details['availableBalance']
        wallet_doc.locked_balance = details['lockedAmount']
        wallet_doc.save()
        print(f'Updated wallet {wallet_doc.wallet_address}')
