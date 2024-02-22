import asyncio

from aiohttp import ClientSession
from aiohttp.client import _RequestContextManager
from telegram import Bot

from constants import *


class BinanceAPI:
    def __init__(self):
        self.chats = CHATS
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

    async def send_currency_rate(self):
        bot = Bot(token=TELEGRAM_TOKEN)

        async with ClientSession() as http_session:
            rate = await self.fetch_currency_rate(http_session=http_session)
            for chat in CHATS.split(','):
                await bot.send_message(
                    chat_id=chat,
                    text=f'{str(rate)}$'
                )

    async def start_sending_currency_rate(self):
        while True:
            await self.send_currency_rate()
            await asyncio.sleep(SLEEP_TIME)


if __name__ == "__main__":
    api = BinanceAPI()
    asyncio.run(api.start_sending_currency_rate())
