from core.utils import read_proxies, read_wallets, read_cex_data
from core.reqs import check
from core.console import init_console

from fake_useragent import UserAgent
from web3 import AsyncWeb3, AsyncHTTPProvider
import asyncio
import random

WALLETS = read_wallets()
PROXIES = read_proxies()
CEX_DATAS = read_cex_data()
ADDRESSES = []

w3 = AsyncWeb3(provider=AsyncHTTPProvider())

for wallet in WALLETS:
    if wallet:
        if wallet[:2] != '0x':
            wallet = '0x' + wallet

        if len(wallet) > 50:
            address = w3.eth.account.from_key(wallet).address
            ADDRESSES.append(address)
        else:
            ADDRESSES.append(wallet)

total_addresses = len(ADDRESSES)

check_allocation = True
cex_claim = True

ua = UserAgent(os=["Windows", "Linux", "Ubuntu", "Mac OS X"])

async def worker(i, address, input_wallet, proxy, user_agent, is_claim, platform, deposit_address, user_id):
    allocation = await check(address, input_wallet, proxy, user_agent, is_claim, platform, deposit_address, user_id)

    return i, allocation

async def main(is_claim, platform):
    sum_allocation = 0
    eligible_addresses = 0

    while len(ADDRESSES) > 0:
        tasks = []
        deposit_address = "",
        user_id = ""
        for i, address in enumerate(ADDRESSES):
            proxy = PROXIES[i]
            input_wallet = WALLETS[i]
            user_agent = ua.random
            if is_claim:
                deposit_address = CEX_DATAS[i].split(':')[0]
                user_id = CEX_DATAS[i].split(':')[1]
            task = asyncio.create_task(worker(i, address, input_wallet, proxy, user_agent, is_claim, platform, deposit_address, user_id))
            await asyncio.sleep(random.uniform(1, 2))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        successes = []
        failed_proxies = []

        for i, allocation in results:
            if isinstance(allocation, bool):
                print('not not a')
                continue
            if allocation == -1:
                failed_proxies.append(PROXIES[i])
            elif allocation >= 0:
                successes.append(i)
                if allocation > 0:
                    sum_allocation += allocation
                    eligible_addresses += 1

        for indx in sorted(successes, reverse=True):
            ADDRESSES.pop(indx)
            PROXIES.pop(indx)
            WALLETS.pop(indx)
            if is_claim:
                CEX_DATAS.pop(indx)

        for proxy in failed_proxies:
            PROXIES.remove(proxy)

    print(f"Элигабл кошельков: {eligible_addresses} / {total_addresses}")
    print(f"Всего токенов: {sum_allocation}")


def select_mode():
    mode = init_console()

    if mode == 'Выход':
        exit(0)

    is_claim = True if mode != "Чекер" else False
    platform = mode.split(' ')[0].lower() if mode in ["Gate", "Kucoin", "HashKey Global", "HTX"] else ""

    return is_claim, platform

if __name__ == '__main__':
    is_claim, platform = select_mode()
    asyncio.run(main(is_claim, platform))