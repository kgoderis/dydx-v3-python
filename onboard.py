'''Example for onboarding an account and accessing private endpoints.

Usage: python -m examples.onboard
'''

from dydx3 import Client
from dydx3.constants import API_HOST_GOERLI
from dydx3.constants import NETWORK_ID_GOERLI
from web3 import Web3

if __name__ == "__main__":

    # Ganache test address.
    ETHEREUM_ADDRESS = '0xd5c368a6a6e1eea20b1856c80416279b336aeda2'
    ETH_KEY = "dbef5bd6da96a9df014e12e917a2a8f55cfb6aace975932c8aa348cfff62ec33"

    # Ganache node.
    WEB_PROVIDER_URL = 'http://localhost:8545'

    client = Client(
        network_id=NETWORK_ID_GOERLI,
        host=API_HOST_GOERLI,
        default_ethereum_address=ETHEREUM_ADDRESS,
        # web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
        eth_private_key = ETH_KEY
    )

    # Set STARK key.
    stark_key_pair_with_y_coordinate = client.onboarding.derive_stark_key()
    client.stark_private_key = stark_key_pair_with_y_coordinate['private_key']
    (public_x, public_y) = (
        stark_key_pair_with_y_coordinate['public_key'],
        stark_key_pair_with_y_coordinate['public_key_y_coordinate'],
    )

    # Onboard the account.
    # onboarding_response = client.onboarding.create_user(
    #     stark_public_key=public_x,
    #     stark_public_key_y_coordinate=public_y,
    # )
    # print('onboarding_response', onboarding_response)

    # Query a private endpoint.
    accounts_response = client.private.get_user()
    print('accounts_response', accounts_response)
