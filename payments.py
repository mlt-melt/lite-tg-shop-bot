from config import db
import aiohttp


def api_crypto():
    token = db.get_token('CRYPTO')
    return token

async def getCoins():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.nowpayments.io/v1/merchant/coins', headers={'x-api-key': api_crypto()}) as resp:
            response = await resp.json()
            return response['selectedCurrencies']

async def createPayment(amount, paycurrency):
    headers = {
        'x-api-key': api_crypto()
    }
    payload = {
        "price_amount": float(amount),
        "price_currency": "usd",
        "pay_currency": paycurrency,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.nowpayments.io/v1/payment', headers=headers, data=payload) as resp:
            response = await resp.json()
            return response

async def check_pay(payment_id):
    headers = {
        'x-api-key': api_crypto()
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.nowpayments.io/v1/payment/{payment_id}', headers=headers) as resp:
            response = await resp.json()
            return response['payment_status']