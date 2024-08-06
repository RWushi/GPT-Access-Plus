from quart import Quart, request
from Payment import success, processing, fail
from Config import dp

app = Quart(__name__)

@app.route('/webhooks/maxpay', methods=['POST'])
async def maxpay_webhook():
    payment_data = await request.json

    user_id = payment_data.get('user_id')
    period = payment_data.get('period')
    status = payment_data.get('status')
    secret_key = payment_data.get('secret_key')

    if secret_key != '341728':
        return "Неверный secret_key", 403

    if status == 1:
        await success(user_id, period)
    elif status in [0, 2, 3]:
        await processing(user_id)
    elif status in [4, 5, 6]:
        await fail(user_id)

    return "Ответ получен", 200

async def start_maxpay(dp):
    await app.run_task(host='0.0.0.0', port=8080)
