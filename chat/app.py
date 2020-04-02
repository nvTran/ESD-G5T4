from telegram.client import Telegram

tg = Telegram(
    api_id='api_id',
    api_hash='api_hash',
    phone='+31611111111',  # you can pass 'bot_token' instead
    database_encryption_key='changekey123',
)
tg.login()

# if this is the first run, library needs to preload all chats
# otherwise the message will not be sent
result = tg.get_chats()
result.wait()

result = tg.send_message(
    chat_id=args.chat_id,
    text=args.text,
)
# `tdlib` is asynchronous, so `python-telegram` always returns you an `AsyncResult` object.
# You can receive a result with the `wait` method of this object.
result.wait()
print(result.update)