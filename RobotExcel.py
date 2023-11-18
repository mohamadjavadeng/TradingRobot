import numpy as np
import pandas as pd
from telegram import Update
from telegram import ChatMember, InputFile
from telegram.ext import CommandHandler, ContextTypes, Application, MessageHandler
# from telegram.ext import filters
# from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler

TOKEN = '6482435292:AAGopzwfmpQZUJElM5tQdwCccWYP91cp_q0'
excelpath = "./robotinfo.xlsx"

def argmax(x):
    i = 0
    while x[i] == False:
        i = i+1
    return i

async def start(update= Update, context= ContextTypes.DEFAULT_TYPE):
    # -----------< inlinekeyboard >--------------------- #
    userid = update.effective_user.id
    if update.effective_chat.type in ["group", "supergroup"]:
        chatid = update.effective_chat.id
        df = pd.read_excel(excelpath)
        filtr = max(df["chatID"] == chatid)
        print(filtr)
        if filtr:
            print('bye')
        else:
            print("hi")
            chat_member = await context.bot.get_chat_member(chatid, userid)
            if chat_member.status in [ChatMember.ADMINISTRATOR, "creator"]:
                df.loc[len(df), ["userID", "chatID", "Token"]] = [userid, chatid, 0]
        df.to_excel(excelpath, index=False)
    else:
        await context.bot.send_message(chat_id=userid, text=f'welcom {update.effective_chat.first_name}')

async def forbiden(update= Update, context= ContextTypes.DEFAULT_TYPE):
    forbid = str(context.args[0])
    userid = update.effective_user.id
    if update.effective_chat.type in ["group", "supergroup"]:
        chatid = update.effective_chat.id
        df = pd.read_excel(excelpath)
        filtr = (df["chatID"] == chatid)
        chat_member = await context.bot.get_chat_member(chatid, userid)
        if max(filtr) and (chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]):
            if pd.isna(df.loc[argmax(filtr), "forbiden"]):
                print("nan")
                df.at[argmax(filtr), "forbiden"] = forbid
                df.at[argmax(filtr), "Token"] = 1
            else:
                frb = str(df.at[argmax(filtr), "forbiden"]) + "," + forbid
                df.at[argmax(filtr), "forbiden"] = frb
                df.at[argmax(filtr), "Token"] = int(df.at[argmax(filtr), "Token"]) + 1
        else:
            if chat_member.status in [ChatMember.ADMINISTRATOR, "creator"]:
                df.loc[len(df), ["userID", "chatID", "forbiden", "Token"]] = [userid, chatid, forbid, 1]
            else:
                pass
        df.to_excel(excelpath, index=False)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handlers([
        CommandHandler('start', start),
        CommandHandler('forbid', forbiden),
        # CommandHandler('help', help),
        # CommandHandler('dlYoutube', YT_handler),
        # CommandHandler('adminhndl', admin_handler),
        # CommandHandler('frwmes', forward_message),
        # CommandHandler('joinchat', join_chat),
        # CallbackQueryHandler(button_callback),
        # MessageHandler(filters.TEXT & (~filters.COMMAND),message_rcv)
    ])
    # send_rep_message()
    app.run_polling()


if __name__=='__main__':
    main()