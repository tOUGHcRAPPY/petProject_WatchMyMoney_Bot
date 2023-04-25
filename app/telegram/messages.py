from datetime import datetime, timedelta

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from app import finances
from app.finances.models import Finance
from app.telegram.bot import bot
from app.user.models import TelegramUser


def start_messages(user_id, context):
    bot.send_message(user_id, text="Hello and welcome to WatchMyMoney Bot! 👩🏻‍💻 \n"
                                   "I am Your financial assistant and here is what I will do for You: \n"
                                   "1. Receive information about Your spends and income. \n"
                                   "2. Give You information about spend and income in different time period.")


def open_menu(user_id, context):
    list_btn = [
        [KeyboardButton("Add info 🧾", callback_data="add_info")],
        [KeyboardButton("Archive 📊", callback_data="archive")]
    ]
    keyboard = ReplyKeyboardMarkup(list_btn, True)
    bot.send_message(user_id, reply_markup=keyboard, text="Menu:")


def open_menu_add_spends_or_add_income(user_id, context):
    list_btn = [
        [InlineKeyboardButton("Add spend", callback_data="add_spend")],
        [InlineKeyboardButton("Add income", callback_data="add_income")]
    ]
    keyboard = InlineKeyboardMarkup(list_btn)
    bot.send_message(user_id, reply_markup=keyboard, text="Spend/Income")


def open_menu_spend_categories(user_id, context):
    list_btn = [
        [InlineKeyboardButton("Add transport spend", callback_data="add_transport_spend")],
        [InlineKeyboardButton("Add utility payments spend", callback_data="add_utility_spend")],
        [InlineKeyboardButton("Add grocery shopping spend", callback_data="add_grocery_spend")],
        [InlineKeyboardButton("Add clothes shopping spend", callback_data="add_clothes_spend")],
        [InlineKeyboardButton("Add entertainment spend", callback_data="add_entertainment_spend")],
        [InlineKeyboardButton("Add food delivery / coffee / tea sped", callback_data="add_food/coffee/tea_spend")]
    ]
    keyboard = InlineKeyboardMarkup(list_btn)
    bot.send_message(user_id, reply_markup=keyboard, text="Spend_Categories")


def open_menu_archive(user_id, context):
    list_btn = [
        [InlineKeyboardButton("Report for today", callback_data="report_for_today")],
        [InlineKeyboardButton("Report for yesterday", callback_data="report_for_yesterday")],
        [InlineKeyboardButton("Report for this week", callback_data="report_for_this_week")]
    ]
    keyboard = InlineKeyboardMarkup(list_btn)
    bot.send_message(user_id, reply_markup=keyboard, text="Select date or duration:")


def open_report_today(user_id, context):
    finances = Finance.objects.filter(user=TelegramUser.objects.get(chat_id=user_id),
                                      date_time__date=datetime.now().date())
    sum_income = 0
    sum_spend = 0
    list_btn = []
    for item in finances:
        emoji_status = ""
        if item.finance_status == True:
            sum_income += item.amount
            emoji_status = "🟢"
        else:
            sum_spend += item.amount
            emoji_status = "🔴"
        list_btn.append([InlineKeyboardButton(f"{emoji_status} {item.amount} UAH - {item.description}", callback_data="_"),
                         InlineKeyboardButton("❌", callback_data="today_delete_item_" + str(item.id))
                         ])
    sum_finances = sum_income - sum_spend
    keyboard = InlineKeyboardMarkup(list_btn)
    bot.send_message(user_id, reply_markup=keyboard, text=f"Today: \n"
                                                          f"Total income : {sum_income} \n"
                                                          f"Total spend :{sum_spend} \n"
                                                          f"Total {sum_finances}")


def open_report_yesterday(user_id, context):
    yesterday = datetime.now().date() - timedelta(days=1)
    finances = Finance.objects.filter(user=TelegramUser.objects.get(chat_id=user_id),
                                      date_time__date=yesterday)
    sum_income = 0
    sum_spend = 0
    list_btn = []
    for item in finances:
        emoji_status = ""
        if item.finance_status == True:
            sum_income += item.amount
            emoji_status = "🟢"
        else:
            sum_spend += item.amount
            emoji_status = "🔴"
        list_btn.append([InlineKeyboardButton(f"{emoji_status} {item.amount} UAH - {item.description}", callback_data="_"),
                         InlineKeyboardButton("❌", callback_data="yesterday_delete_item_" + str(item.id))
                         ])
    sum_finances = sum_income - sum_spend
    keyboard = InlineKeyboardMarkup(list_btn)
    bot.send_message(user_id, reply_markup=keyboard, text=f"Yesterday: \n"
                                                          f"Total income : {sum_income} \n"
                                                          f"Total spend :{sum_spend} \n"
                                                          f"Total {sum_finances}")


def open_report_this_week(user_id, context):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    print("Hello")
    print(start_of_week)
    print(today.weekday())
    finances = Finance.objects.filter(user=TelegramUser.objects.get(chat_id=user_id),
                                      date_time__date__gte=start_of_week)
    sum_income = 0
    sum_spend = 0
    list_btn = []
    for item in finances:
        emoji_status = ""
        if item.finance_status == True:
            sum_income += item.amount
            emoji_status = "🟢"
        else:
            sum_spend += item.amount
            emoji_status = "🔴"
        list_btn.append([InlineKeyboardButton(f"{emoji_status} {item.amount} UAH - {item.description}", callback_data="_"),
                         InlineKeyboardButton("❌", callback_data="week_delete_item_" + str(item.id))
                         ])
    sum_finances = sum_income - sum_spend
    keyboard = InlineKeyboardMarkup(list_btn)
    bot.send_message(user_id, reply_markup=keyboard, text=f"This week: \n"
                                                          f"Total income : {sum_income} \n"
                                                          f"Total spend :{sum_spend} \n"
                                                          f"Total {sum_finances}")


def delete_item(user_id, context, item_id):
    print("Start/Delete")
    item = Finance.objects.get(id=item_id)
    print(item)
    item.delete()
    print(item.description)
    text = f"Delete item: \n description: {item.description} \n amount: {item.amount}"
    bot.send_message(user_id, text=text)


def spend_or_income_message(user_id, context, text):
    bot.send_message(user_id, text=text)


def create_spend_finances_in_admin(user_id, context, data):
    print("spend - ", data)
    list_element = data.split("-")
    print(list_element)
    try:
        new_spend = Finance(
            description=list_element[1],
            finance_status=False,
            amount=list_element[0],
            user=TelegramUser.objects.get(chat_id=user_id)
        )
        new_spend.save()
        bot.send_message(user_id, text=f"Your spend {new_spend.amount} UAH {new_spend.description} is successfully saved.")
    except ValueError:
        bot.send_message(user_id, text="Please input Your spend in next order:\n"
                                       "amount - description\n"
                                       "For example: 13579 - communal payments")


def create_income_finances_in_admin(user_id, context, data):
    print("income - ", data)
    list_element = data.split("-")
    try:
        new_income = Finance(
            description=list_element[1],
            finance_status=True,
            amount=list_element[0],
            user=TelegramUser.objects.get(chat_id=user_id)
        )
        new_income.save()
        bot.send_message(user_id, text=f"Your income {new_income.amount} UAH {new_income.description} is successfully saved.")
    except ValueError:
        bot.send_message(user_id, text="Please input Your income in next order:\n"
                                       "amount - description\n"
                                       "For example: 13579 - salary")