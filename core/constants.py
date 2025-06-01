import os
import sys
from pathlib import Path

def create_directory(path: str | Path) -> bool:
    try:
        path = Path(path) if isinstance(path, str) else path

        if path.exists():
            return True

        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {str(e)}")
        return False

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

DATA_DIR = os.path.join(ROOT_DIR, "data")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")

create_directory(RESULTS_DIR)

WALLETS_PATH = os.path.join(DATA_DIR, 'wallets.txt')
PROXIES_PATH = os.path.join(DATA_DIR, "proxies.txt")
CEX_DATA_PATH = os.path.join(DATA_DIR, "cex_data.txt")
RESULTS_PATH = os.path.join(RESULTS_DIR, "results.txt")
CEX_CLAIM_PATH = os.path.join(RESULTS_DIR, "cex_claim_success.txt")
ELIGIBLE_DIR_PATH = os.path.join(RESULTS_DIR, "eligible.txt")

MESSAGE_TEMPLATE = """I hereby authorize this message as confirmation of ownership for the wallet address: {wallet_address}. By signing, I acknowledge that I have read and accepted the Airdrop Terms of Service and Privacy Policy. The SHA-256 hash of the referenced terms and policy is: 0x83139cd33c94f79b9d3b427f0f1f482c3f3091ef5896853dc1011e8e46070563

ConnectWallet: {connect_wallet}

Platform: {platform}

UserId: {user_id}

DepositAddress: {deposit_address}
"""
