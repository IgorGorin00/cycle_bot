import os
import logging
from pathlib import Path
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    filters,
    MessageHandler,
    CommandHandler,
)
from img_translator import get_models, get_visual
from utils import save_image
from secret import token

root_path = Path(".")
data_path = Path("data")
results_path = Path("results")
cache_path = Path("data_cache")
models_path = Path("models")


data_dir = root_path / data_path
results_dir = root_path / results_path
cache_dir = root_path / cache_path
cache_real = cache_dir / "real"
cache_fake = cache_dir / "fake"
models_dir = root_path / models_path
models = get_models(models_dir)
logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)


async def help_command(update: Update, context: CallbackContext) -> None:
    text = "This bot applies different styles to the image sent. \
            Try to send an image and see for yourself!"
    await update.message.reply_text(text)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send photo you need to translate")


def check_dirs_for_user(client_id):
    dirs_to_check = [data_dir, results_dir, cache_real, cache_fake]
    for dir in dirs_to_check:
        if client_id not in os.listdir(dir):
            os.mkdir(dir / client_id)
            logging.info(f'Creating {dir} for {client_id}')


async def get_photo(update: Update, context: CallbackContext) -> None:
    file = await update.message.effective_attachment[-1].get_file()
    client_id = update.message.chat.username
    message_id = update.message.message_id
    file_name = f"{client_id}_{message_id}.png"

    logging.info(f'get_photo called for {client_id}')
    check_dirs_for_user(client_id)
    await file.download_to_drive(data_dir / client_id / file_name)

    text = "Photo uploaded, choose style"
    keyboard = [
        [
            InlineKeyboardButton('Ukiyo-e', callback_data='ukiyoe'),
            InlineKeyboardButton('Monet', callback_data='monet'),
            InlineKeyboardButton('Cezanne', callback_data='cezanne'),
            InlineKeyboardButton('Vangogh', callback_data='vangogh')

        ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)


async def send_images(context, client_id, chat_id) -> None:
    for image_name in os.listdir(results_dir / client_id):
        with open(results_dir / client_id / image_name, 'rb') as image:
            await context.bot.send_photo(chat_id=chat_id, photo=image)
    text = "Here's your image! Send another one or just save this"
    await context.bot.send_message(
        chat_id=chat_id, text=text)


async def translate_to_style(context, chat_id, client_id, style) -> None:

    usr_data_dir = data_dir / client_id
    usr_res_dir = results_dir / client_id
    usr_cache_real_dir = cache_real / client_id
    usr_cache_fake_dir = cache_fake / client_id
    for img_name in os.listdir(usr_data_dir):
        res_img = get_visual(
            img_path=usr_data_dir / img_name,
            model=models[style]
        )
        save_image(res_img, usr_res_dir / img_name)
        await context.bot.send_message(
            chat_id=chat_id, text="Image processed! Sending result...")
    await send_images(context, client_id, chat_id)
    for img_name in os.listdir(usr_data_dir):
        os.replace(usr_data_dir / img_name,
                   usr_cache_real_dir / img_name)
        os.replace(usr_res_dir / img_name,
                   usr_cache_fake_dir / img_name)


async def ukiyoe(update: Update, context: CallbackContext) -> None:
    client_id = update.callback_query.message.chat.username
    chat_id = update.effective_chat.id
    await translate_to_style(context, chat_id, client_id, "ukiyoe")


async def monet(update: Update, context: CallbackContext) -> None:
    client_id = update.callback_query.message.chat.username
    chat_id = update.effective_chat.id
    await translate_to_style(context, chat_id, client_id, "monet")


async def cezanne(update: Update, context: CallbackContext) -> None:
    client_id = update.callback_query.message.chat.username
    chat_id = update.effective_chat.id
    await translate_to_style(context, chat_id, client_id, "cezanne")


async def vangogh(update: Update, context: CallbackContext) -> None:
    client_id = update.callback_query.message.chat.username
    chat_id = update.effective_chat.id
    await translate_to_style(context, chat_id, client_id, "vangogh")


def main():

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(ukiyoe, pattern="^ukiyoe$"))
    application.add_handler(CallbackQueryHandler(monet, pattern="^monet$"))
    application.add_handler(CallbackQueryHandler(cezanne, pattern="^cezanne$"))
    application.add_handler(CallbackQueryHandler(vangogh, pattern="^vangogh$"))
    application.add_handler(MessageHandler(filters.PHOTO, get_photo))
    application.run_polling()
    print("Started")


if __name__ == '__main__':
    main()
