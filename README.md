<div style="text-align:center">
    
# 🤖💰 [Trader One Bot](https://t.me/trader_one_bot)

</div>

![contributors](https://img.shields.io/badge/contributors-3-blue) ![version](https://img.shields.io/badge/version-1.0-red) ![maintainers](https://img.shields.io/badge/maintainers-ez--developers-green) ![code-quality](https://img.shields.io/badge/code--quality-89-informational) ![license](https://img.shields.io/badge/licence-MIT-orange) ![issues](https://img.shields.io/badge/issues-1-critical)

**Trader One Bot™** is a telegram bot built with Telegram's [Bot API](https://core.telegram.org/bots/api) in [Python](https://python.org/) programming language.

## 👥 Maintainers:

-   #### Nuriddin Islamov ([@nuriddinislamov](https://github.com/nuriddinislamov))

-   #### Jahongir Nagmatov ([@jakhongeer](https://github.com/jakhongeer))

-   #### Javlon Kayumov ([@iamjavlon](https://github.com/iamjavlon))

---

## Instructions for developer:

We are happy to hear that you are the next major developer of this project. This project has been developed strongly by the instructions of the business owner. Here you can find all the information about installation, code quality, maintenance and deployment.

## Installation

-   **Clone** the repository using `git clone` command on your machine:

```bash
$ git clone https://github.com/ez-developers/traderbot.git
```

-   **Move** into the project directory:

```bash
$ cd traderbot
```

-   **Create** a virtual environment:

```bash
$ python3 -m venv venv
```

-   **Activate** the virtual environment:

```bash
$ source venv/bin/activate
```

-   **Install** all required packages:

```bash
$ pip install -r requirements.txt
```

#### ❗️ Note: Bot is fully dependent on the backend server. Database connections are done with RESTful API built in the `api` directory of the project folder

Before moving on to runnning _the bot_ and _the server_, you will need to create a `.env` file (note that the file **does not have** a name) in the root of the project directory.

#### Fill up the content of the file with following:

-   **BOT_TOKEN:** bot's token (you can get one from [@BotFather](https://t.me/botfather))
-   **DB_IP:** public IP address of the database server.
    ###### Notice! You should use PostgreSQL database engine, as the project relies on the ArrayField in the [Portfolios model](https://github.com/ez-developers/traderbot/blob/34744209aa2b229e4370ba534f8d1b76efe06bff/app/models.py#L74).
-   **DB_NAME:** name of the database on the server ([more](https://medium.com/swlh/architecture-of-postgresql-db-d6b1ac4cc231))
-   **DB_USER:** database user's username
-   **DB_PASSWORD:** database user's password
-   **API_USER:** username for accessing backend server API with HTTP calls
-   **API_PASSWORD:** password for accessing backend server API with HTTP calls
-   **PAYMENT_TOKEN:** token for accessing payments API of the Telegram
-   **SECRET_KEY:** django secret key
    <br/>

After that, you will need to change the configurations in the [settings.py](https://github.com/ez-developers/traderbot/blob/34744209aa2b229e4370ba534f8d1b76efe06bff/core/settings.py#L53). Now you are ready to start running the server and the bot itself.

## Running the bot and the server

If you are following the instructions from the very beginning, then continue here, otherwise please [go up](#Installation).

-   **First, run the server**. To run:

```bash
$ python3 manage.py runserver
```

-   **Then** run the bot:

```bash
$ python3 bot.py
```

If `logger` in your [main.py](https://github.com/ez-developers/traderbot/blob/34744209aa2b229e4370ba534f8d1b76efe06bff/bot/main.py#L26) is set to `level=logging.DEBUG` you will see the output of all incoming updates from Telegram servers.
