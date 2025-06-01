from core.constants import WALLETS_PATH, PROXIES_PATH, RESULTS_PATH, ELIGIBLE_DIR_PATH, CEX_DATA_PATH, CEX_CLAIM_PATH

def read_file(path: str, add=''):
    with open(path, encoding='utf-8') as file:
        return [f"{add}{line.strip()}" if add not in line else line.strip() for line in file]

def read_wallets() -> list[str]:
    return read_file(WALLETS_PATH)

def read_proxies() -> list[str]:
    return read_file(PROXIES_PATH, add='http://')

def read_cex_data() -> list[str]:
    return read_file(CEX_DATA_PATH)

def write_result(address: str, amount: float):
    with open(RESULTS_PATH, 'a', encoding="utf-8") as f:
        f.write(f'{address} - {amount}\n')

def write_eligible_wallet(address: str):
    with open(ELIGIBLE_DIR_PATH, 'a', encoding="utf-8") as f:
        f.write(f'{address}\n')

def write_cex_success(wallet: str):
    with open(CEX_CLAIM_PATH, 'a', encoding="utf-8") as f:
        f.write(f'{wallet}\n')
