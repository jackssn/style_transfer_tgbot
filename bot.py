import os
import logging
from urllib.parse import urljoin

import style_transfer

from aiogram import Bot, Dispatcher, executor, types

# telegram token
API_TOKEN = os.environ['API_TOKEN']

# webhook settings
WEBHOOK_HOST = os.environ['WEBHOOK_HOST']
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_PATH)

#webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ['PORT']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def on_startup(dispatcher: 'Dispatcher') -> None:
    logging.warning('Starting...')
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dispatcher: 'Dispatcher') -> None:
    logging.warning('Shutting down...')
    logging.warning('Done.')

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.answer("Hello, <b>%s</b>!\n\nI'm RefresherBot by @jackssn!\n"
                         "If you want to transfer style from one photo to another send me photo "
                         "with text \"style\" and than another photo with text \"content\". "
                         "\n\nAfter that I will send you a result of my work." % message.from_user.first_name,
                         parse_mode='HTML')

#@dp.message_handler(regexp='style', content_types=types.ContentType.PHOTO)
#async def cats(message: types.Message):
#    with open('cat.jpg', 'rb') as photo:
#        await message.answer_photo(photo, caption='Cats are here 😺')

async def upd_dir(message, type_path):
    path = 'data/%s/%s' % (message.from_user.id, type_path)
    if not os.path.exists(path):
        os.makedirs(path)

@dp.message_handler(regexp='style', content_types=types.ContentType.PHOTO)
async def accept_style(message: types.Message):
    await upd_dir(message, 'style')
    await message.photo[-1].download('data/%s/style/%s.jpg' %
                                     (message.from_user.id, (message.date.strftime('%Y%m%d%H%M%S'))))
    await message.reply('Style accepted')

@dp.message_handler(regexp='content', content_types=types.ContentType.PHOTO)
async def accept_content(message: types.Message):
    await upd_dir(message, 'content')
    await upd_dir(message, 'result')
    await message.photo[-1].download('data/%s/content/%s.jpg' % (message.from_user.id,
                                                                 (message.date.strftime('%Y%m%d%H%M%S'))))
    await message.reply('Content accepted. Now wait a result. It takes about 5 minutes.')
    last_style = os.listdir('data/%s/style' % message.from_user.id)
    if last_style:
        last_style = last_style[-1]
    else:
        await message.answer('You are not upload any style-image, so we use default image (picasso).')
    last_content = os.listdir('data/%s/content' % message.from_user.id)[-1]
    style_transfer.main(imsize=256, num_steps=150,
                           img_style=os.path.join('data/%s/style' % message.from_user.id, last_style),
                           img_content=os.path.join('data/%s/content' % message.from_user.id, last_content))
    with open(os.path.join('data/%s/result' % message.from_user.id, last_content), 'rb') as photo:
        await message.answer_photo(photo)

if __name__ == '__main__':

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
