'''Example for placing, replacing, and canceling orders.

Usage: python -m examples.orders
'''

import time

from dydx3 import Client
from dydx3.constants import API_HOST_GOERLI
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import NETWORK_ID_GOERLI
from dydx3.constants import ORDER_SIDE_BUY
from dydx3.constants import ORDER_STATUS_OPEN
from dydx3.constants import ORDER_TYPE_LIMIT
from web3 import Web3

# Ganache test address.
ETHEREUM_ADDRESS = '0xd5c368a6a6e1eea20b1856c80416279b336aeda2'
ETH_KEY = "dbef5bd6da96a9df014e12e917a2a8f55cfb6aace975932c8aa348cfff62ec33"

# Ganache node.
WEB_PROVIDER_URL = 'http://localhost:8545'

client = Client(
    network_id=NETWORK_ID_GOERLI,
    host=API_HOST_GOERLI,
    default_ethereum_address=ETHEREUM_ADDRESS,
    eth_private_key = ETH_KEY
)

# Set STARK key.
stark_private_key = client.onboarding.derive_stark_key()
client.stark_private_key = stark_private_key

# Get our position ID.
account_response = client.private.get_account()
# position_id = account_response['account']['positionId']
position_id=15555

# Post an bid at a price that is unlikely to match.
order_params = {
    'position_id': position_id,
    'market': MARKET_BTC_USD,
    'side': ORDER_SIDE_BUY,
    'order_type': ORDER_TYPE_LIMIT,
    'post_only': True,
    'size': '0.0777',
    'price': '20',
    'limit_fee': '0.0015',
    'expiration_epoch_seconds': time.time() + 120,
}
order_response = client.private.create_order(**order_params)
order_id = order_response['order']['id']

# Replace the order at a higher price, several times.
# Note that order replacement is done atomically in the matching engine.
for replace_price in range(21, 26):
    order_response = client.private.create_order(
        **dict(
            order_params,
            price=str(replace_price),
            cancel_id=order_id,
        ),
    )
    order_id = order_response['order']['id']

# Count open orders (there should be exactly one).
orders_response = client.private.get_orders(
    market=MARKET_BTC_USD,
    status=ORDER_STATUS_OPEN,
)
assert len(orders_response['orders']) == 1

# Cancel all orders.
client.private.cancel_all_orders()

# Count open orders (there should be none).
orders_response = client.private.get_orders(
    market=MARKET_BTC_USD,
    status=ORDER_STATUS_OPEN,
)
assert len(orders_response['orders']) == 0