import asyncio
import logging

from aiohttp import ClientSession
from aiohttp.client import _RequestContextManager
from telegram import Bot

from constants import *


class BinanceAPI:
    def __init__(self):
        self.telegram_token = TELEGRAM_TOKEN
        self.chat_id = CHAT_ID
        self.currency = CURRENCY

    @staticmethod
    async def _make_request(
        http_session: ClientSession, currency: str
    ) -> _RequestContextManager:
        endpoint = "ticker/price"
        params = {"symbol": currency}
        url = f"{BASE_URL}/{endpoint}"

        async with http_session.get(
            url=url,
            params=params,
            headers={
                "Content-Type": "application/json",
                "X-MBX-APIKEY": API_KEY,
            },
        ) as response:
            if response.status == 200:
                result = await response.json()
                logging.info(
                    f"Made request and got Currency: {currency}, Result: {result}"
                ) if not result else None

                return result
            else:
                response_text = await response.text()
                logging.warning(
                    f"Request failed with status code {response.status}: {response_text}"
                )

    async def fetch_currency_rate(self, http_session: ClientSession) -> int:
        ticker_price = await self._make_request(
            http_session=http_session,
            currency=self.currency)

        return int(float(ticker_price["price"]))

    async def gather_concurrent_tasks(self) -> None:
        tasks = list()

        async with ClientSession() as http_session:
            task = self.fetch_currency_rate(http_session)
            tasks.append(task)
            result = await asyncio.gather(*tasks)

            for data in result:
                if not data:
                    logging.warning(
                        f"API response is {data} for one or more currencies in fetch_currency_rate"
                    )

    async def send_currency_rate(self):
        bot = Bot(token=TELEGRAM_TOKEN)

        async with ClientSession() as http_session:
            rate = await self.fetch_currency_rate(http_session=http_session)
            await bot.send_message(chat_id=CHAT_ID, text=f'{str(rate)}$')


if __name__ == "__main__":
    api = BinanceAPI()
    asyncio.run(api.send_currency_rate())
