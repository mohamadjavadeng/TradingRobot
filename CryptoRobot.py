import pandas as pd
from telegram import Update
from telegram import ChatMember, InputFile
from telegram.ext import CommandHandler, ContextTypes, Application, MessageHandler
# from telegram.ext import filters
# from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
import requests
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime
import pytz

TOKEN = '6482435292:AAGopzwfmpQZUJElM5tQdwCccWYP91cp_q0'
excelpath = "D:\python\Pandas\TradingRobot\CryptoRobotExcel.csv"
cryptoexcelpath = "D:\python\Pandas\TradingRobot\Crypto Dashboard.csv"


def argmax(x):
    i = 0
    while x[i] == False:
        i = i+1
    return i
#-------------------------------------------------------------#
# get the current price
def get_crypto_price(coin_id):
    url_crypto = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=1'
    response = requests.get(url_crypto)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract price history
        # price_history = data['prices']
        # timestamp = data['prices'][0][0]  # Replace this with your integer timestamp
        # # # Convert the integer timestamp to a date
        # date = datetime.fromtimestamp(timestamp / 1000)
        price = data['prices'][0][1]
        return price
    return None
async def send_msg(update= Update, context= ContextTypes.DEFAULT_TYPE):
    userid = update.effective_user.id
    Name = update.effective_user.first_name
    await context.bot.send_message(chat_id=userid, text=f"Dear {Name} please use permium to buy or sell")

def convert_time(date_string, time_string):
    user_datetime = datetime.strptime(date_string + ' ' + time_string, "%Y-%m-%d %H:%M:%S")
    return user_datetime
#-------------------------------------------------------------#

async def start(update= Update, context= ContextTypes.DEFAULT_TYPE):
    # -----------< inlinekeyboard >--------------------- #
    userid = update.effective_user.id
    Name = update.effective_user.first_name
    if update.effective_chat.type in ["private"]:
        df = pd.read_csv(excelpath)
        filtr = max(df["ChatID"] == str(userid))
        print(filtr)
        if filtr:
            pass
        else:
            df.loc[len(df), ["ChatID", "Name", "Permium"]] = [userid, Name, 0]
        df.to_csv(excelpath, index=False)
        txt = f"""welcome {update.effective_chat.first_name}
use /help to see all available commands"""
        await send_msg(update,context)
        await context.bot.send_message(chat_id=userid, text=txt)

async def help(update= Update, context= ContextTypes.DEFAULT_TYPE):
    text="""all menu in this bot is:
/start
/help
/crypto
/price (Crypto Name)
/alarm YYYY-MM-DD HH:MM:SS"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def crypto(update= Update, context= ContextTypes.DEFAULT_TYPE):
    headers= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
    }
    base_url = "https://www.coingecko.com/en"
    params = {
    'page': 1
    }
    response = requests.get(base_url, headers=headers, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    html_stringio = StringIO(str(soup))
    df_crypto = pd.read_html(html_stringio)[0].head(10)
    text_crypto = []
    cryptos = ['Bitcoin', 'Ethereum', 'BNB', 'XRP', 'Cardano', 'Dogecoin']
    for i in range(0, 10):
        if df_crypto.loc[i, "Coin"].split(" ")[0] in cryptos:
            price = df_crypto.loc[i, "Price"]
            name = df_crypto.loc[i, "Coin"].split(" ")[0]
            if pd.isna(df_crypto.loc[i, "Unnamed: 3"]):
                recommandation = "-"
            else:
                recommandation = df_crypto.loc[i, "Unnamed: 3"]
            # oneHour = df_crypto.loc[i, "1h"]
            # oneDay = df_crypto.loc[i, "24h"]
            # sevenDays = df_crypto.loc[i, "7d"]
            # oneMonth = df_crypto.loc[i, "30d"]
            txt = f"{name} | Price:{price} | recom:{recommandation}"
            text_crypto.append(txt)

    text = f"""crypto prices are:
            {text_crypto[0]},
            {text_crypto[1]}, 
            {text_crypto[2]},
            {text_crypto[3]},
            {text_crypto[4]}"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def price(update= Update, context= ContextTypes.DEFAULT_TYPE):
    crypto_id = str(context.args[0]).lower()
    price = get_crypto_price(crypto_id)
    if price:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text = f"The current price of Bitcoin is: {price}",
                                       reply_to_message_id=update.effective_message.id)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text = "Price not found or unable to fetch.",
                                       reply_to_message_id=update.effective_message.id)
  
async def Alarm_on( context: CallbackContext):
    await context.bot.send_message(chat_id=context.job.chat_id, text="Beep your alarm!")

async def setAlarm(update= Update, context= ContextTypes.DEFAULT_TYPE):
    date = context.args[0]
    time = context.args[1]
    userid = update.effective_user.id
    Name = update.effective_user.first_name
    # tehran_timezone = pytz.timezone('Asia/Tehran')
    # tehran_time = datetime.now(tehran_timezone)
    Alarm = convert_time(date_string=date, time_string=time)
    # utc_time = tehran_time.astimezone(Alarm)
    if update.effective_chat.type in ["private"]:
        df = pd.read_csv(excelpath)
        filtr = max(df["ChatID"] == str(userid))
        print(Alarm)
        if filtr:
            df.loc[df["ChatID"] == str(userid), "Alarm"] = Alarm
        else:
            df.loc[len(df), ["ChatID", "Name", "Permium", "Alarm"]] = [userid, Name, 0, Alarm]
        df.to_csv(excelpath, index=False)
        text = f"Alarm set at {Alarm}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        context.job_queue.run_once(Alarm_on,when=Alarm, chat_id=userid)
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handlers([
        CommandHandler('start', start),
        CommandHandler('help', help),
        CommandHandler('crypto', crypto),
        CommandHandler('price', price),
        CommandHandler('alarm', setAlarm),
        # CommandHandler('joinchat', join_chat),
        # CallbackQueryHandler(button_callback),
        # MessageHandler(filters.TEXT & (~filters.COMMAND),message_rcv)
    ])
    # send_rep_message()
    app.run_polling()


if __name__=='__main__':
    main()