import aiohttp
from aiohttp import ClientHttpProxyError, ConnectionTimeoutError
from web3 import AsyncWeb3, AsyncHTTPProvider
from eth_account.messages import encode_defunct

from core.utils import write_eligible_wallet, write_result, write_cex_success
from core.constants import MESSAGE_TEMPLATE

w3 = AsyncWeb3(provider=AsyncHTTPProvider())

async def check(address: str, input_wallet: str, proxy: str, user_agent: str, is_claim: bool = False, platform: str = "", deposit_address: str = "", user_id: str = ""):
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(proxy=proxy, timeout=timeout) as session:

            headers = {
                "User-Agent": user_agent
            }

            url_main = "https://airdrop.layeredge.foundation/flow"
            url_checker = f"https://airdrop.layeredge.foundation/api/eligibility?address={address}"
            url_cex = "https://airdrop.layeredge.foundation/api/register/cex"

            # Запрос чтобы установились куки
            status = await _init_request(url_main, address, session, headers)

            if status == -1:
                return status

            headers["Accept"] = "application/json, text/plain, */*"
            headers["Clq-App-Id"] = "layeredge"
            headers["Priority"] = "u=1, i"
            headers["Referer"] = "https://airdrop.layeredge.foundation/flow"

            # получаем аллокацию
            allocation = await _check_eligibility(url_checker, address, input_wallet, session, headers, is_claim)

            if not is_claim:
                return allocation

            if allocation < 0.1:
                print(f"{address} | Аллокация сликом маленькая: {allocation}")
                return False

            # если режим клейма и достаточная аллокация
            headers["Origin"] = "https://airdrop.layeredge.foundation"

            if len(input_wallet) < 50:
                print(f"Не удалось заклеймить, пожалуйста введите вместо {input_wallet}, приватный ключ")
                return False

            status = await _cliam_on_cex(session, url_cex, headers, address, input_wallet, platform, deposit_address, user_id)

            if not status:
                return False

            return allocation

    except Exception as e:
        print(f"{address} | Во время получения аллокации произошла ошибка: {e}")
        return -1

async def _cliam_on_cex(session, url, headers, address, input_wallet, platform, deposit_address, user_id):
    try:
        account = w3.eth.account.from_key(input_wallet)

        message = MESSAGE_TEMPLATE.format(
            wallet_address=address.lower(), connect_wallet=address.lower(), platform=platform, user_id=user_id,
            deposit_address=deposit_address.lower())

        msg_hash = encode_defunct(text=message)
        signature = account.sign_message(msg_hash)['signature'].hex()

        payload = {
            "address": address,
            "chainId": 4207,
            "signature": f"0x{signature}",
            "cexInfo": {
                "platform": platform,
                "depositAddress": deposit_address,
                "userId": user_id
            }
        }

        async with session.request("POST", url, headers=headers, json=payload) as response:
            if not response or response.status != 200:
                if response.status == 400:
                    try:
                        response_cex_json = await response.json()
                        if "message" in response_cex_json:
                            if response_cex_json["message"] == "Cannot be modified after submission":
                                print(f"{address} | Клейм уже выполнен")
                                return 0
                    except:
                        ...
                print(f'Не удалось отправить запрос для клейма на биржу')
                return -1
            response_cex_json = await response.json()

            if 'address' not in response_cex_json or 'cexInfo' not in response_cex_json:
                return False
        
        write_cex_success(input_wallet)
        return True
    except:
        return False

async def _init_request(url: str, address: str, session, headers: dict[str: str]):
    try:
        async with session.request("GET", url, headers=headers) as response:
            if not response or response.status != 200:
                print(f'Не удалось загрузить сайт {url}')
                return -1
            return True
    except ConnectionTimeoutError:
        print(f'{address} | Не удалось дождаться загрузки сайта {url}')
    except ClientHttpProxyError:
        print(f'{address} | Не удалось подключиться к прокси {url}')
    except TimeoutError:
        print(f'{address} | Не удалось дождаться загрузки сайта {url}')
    return -1

async def _check_eligibility(url: str, address: str, input_wallet: str, session, headers: dict[str: str], is_claim):
    try:
        async with session.request("GET", url, headers=headers) as response:
            if not response or response.status != 200:
                print(f'{address} | Не удалось получить аллокацию для адреса {address}')
                return False

            response_json = await response.json()
            if 'allocation' in response_json:
                allocation = response_json["allocation"]
            else:
                print(f'{address} | Не удалось получить аллокацию для адреса {address}')
                return False

            if not is_claim:
                print(f"Проверяю адрес {address} - {allocation}")

            if isinstance(allocation, str):
                allocation = allocation.split('.')[0]

            allocation = float(allocation)

            write_result(input_wallet, allocation)
            if allocation > 0:
                write_eligible_wallet(input_wallet)

            return allocation
    except ConnectionTimeoutError or TimeoutError:
        print(f'{address} | Не удалось дождаться загрузки сайта {url}')
        return False
    except aiohttp.client_exceptions.ClientOSError:
        print(f'{address} | Ошибка при получении аллокации')
        return False
    except TimeoutError:
        print(f"{address} | Не удалось дождаться загрузки сайта {url}")
        return -1
