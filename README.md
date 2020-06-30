# Style transfer telegram bot

Telegram bot using Aiogram and Python3. You upload two images: **style** 
and **content**, and bot send you a content-image with style from style-image.

## How to use

1. Send /start to @refresher_jackssnbot in Telegram
2. Send style-photo with caption "style"
3. Send content-photo with caption "content"
4. Waiting for result-photo (it takes about 5-10 minutes)

## How to deploy

1. Buy VPS, for example, [here](https://firstvds.ru/). You need server with KVM virtualization, other types has old kernel version for Docker. Price about 3$/month
2. Install Docker - [instruction (ru)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-debian-9-ru)
3. You need add swap-space to bot right working (I added 4 GB). [Instruction (en)](https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-debian-9)
3. Create Dockerfile like
 [this](https://github.com/jackssn/style_transfer_tgbot/blob/master/Dockerfile) 
. And dont't forget insert your Telegram bot API_TOKEN
4. Deploy bot via Docker with command: `docker build -t <CONTEINER_NAME> ./`
5. Start bot in Docker with command: `docker run -t -d <CONTEINER_NAME>`

## Plans

1. This realization work with `executor.start_pooling()`. 
There are free servers (with memory and disk limits) 
where bots just sleeping after some time (about 30 minutes). 
If we want the bot to work always we need to use 
`executor.start_webhook()`. This good way with free 
hostings like **heroku** and **pythonanywhere**.
2. This code has some bags with async-commands. Parallel dialogs 
while bot working with images doesn't work.

## About project

It's final project in Deep Learning School p.1 [Spring 2020]