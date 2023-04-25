
from telegram import Update

from app.telegram.messages import start_messages, open_menu, open_menu_add_spends_or_add_income, open_menu_archive, \
    open_report_today, open_report_yesterday, open_report_this_week, delete_item, spend_or_income_message, \
    create_spend_finances_in_admin, create_income_finances_in_admin
from app.user.models import TelegramUser


def start_handler(update: Update, context):
    print("Start!")
    user_id = update.message.from_user.id
    print(user_id)
    start_messages(user_id, context)
    open_menu(user_id, context)
    print(TelegramUser.objects.filter(chat_id=user_id).count())
    if TelegramUser.objects.filter(chat_id=user_id).count() == 0:
        new_user = TelegramUser(chat_id=user_id)
        new_user.save()


def main_message_handler(update: Update, context):
    user_id = update.message.from_user.id
    print(user_id)
    message = update.message.text
    print(message)
    print("start_123")
    print(context.user_data)
    if "Add info 🧾" == message:
        print("Called Function that will return buttons add spends or add income.")
        open_menu_add_spends_or_add_income(user_id, context)
    elif "Archive 📊" == message:
        open_menu_archive(user_id, context)
        print("Called Function that will return report.")
    elif context.user_data.get("type_finances") == "spend":
        create_spend_finances_in_admin(user_id, context, message)
        print("spend")
    elif context.user_data.get("type_finances") == "income":
        create_income_finances_in_admin(user_id, context, message)
        print("income")


def check_btn(update: Update, context):
    user_id = update.callback_query.message.chat.id
    print(user_id)
    data = update.callback_query.data
    print(data)
    if "report_for_today" == data:
        open_report_today(user_id, context)
    elif "report_for_yesterday" == data:
        open_report_yesterday(user_id, context)
    elif "report_for_this_week" == data:
        open_report_this_week(user_id, context)
    elif "today_delete_item_" in data:
        item_id = data.replace("today_delete_item_", "")
        delete_item(user_id, context, item_id)
        open_report_today(user_id, context)
    elif "yesterday_delete_item_" in data:
        item_id = data.replace("yesterday_delete_item_", "")
        delete_item(user_id, context, item_id)
        open_report_yesterday(user_id, context)
    elif "week_delete_item_" in data:
        item_id = data.replace("week_delete_item_", "")
        delete_item(user_id, context, item_id)
        open_report_this_week(user_id, context)
    elif "add_spend" == data:
        context.user_data["type_finances"] = "spend"
        spend_or_income_message(user_id, context, "Enter spend in format: 'amount - description'")
    elif "add_income" == data:
        context.user_data["type_finances"] = "income"
        spend_or_income_message(user_id, context, "Enter income in format: 'amount - description'")
    # elif "add_transport_spend" == data:







