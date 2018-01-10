from mongoengine import Document, StringField, ReferenceField, LongField, \
    DateTimeField


class WalletAddressField(StringField):
    def __init__(self, **kwargs):
        max_length = 100
        regex = r'fmrk[a-zA-Z0-9]{95,}'
        super(WalletAddressField, self).__init__(max_length=max_length,
                                                 regex=regex, **kwargs)


class User(Document):
    user_id = StringField(max_length=20, required=True, unique=True,
                          primary_key=True)
    user_wallet_address = WalletAddressField(required=True, unique=True)
    balance_wallet_address = WalletAddressField()


class Wallet(Document):
    wallet_address = WalletAddressField(required=True, unique=True,
                                        primary_key=True)
    actual_balance = LongField(default=0)
    locked_balance = LongField(default=0)


class Tips(Document):
    from_user = ReferenceField(User)
    to_user = ReferenceField(User)
    amount = LongField()
    date = DateTimeField()
