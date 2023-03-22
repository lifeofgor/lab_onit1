import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

def get_news(topic):
    url = f"https://news.mail.ru/search/?usid=90&q={topic}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.findAll("a", class_="newsitem__title")
    return articles[:5]

def news(update, context):
    update.sendMessage(chat_id=update.message.chat_id, text="Здравствуйте.")
    topic = " ".join(context.args)
    if not topic:
        update.message.reply_text("Не выбрана тема новости!")
        return
    articles = get_news(topic)
    for article in articles:
        if article["href"][0] == '/':
            url = 'https://news.mail.ru/' + article["href"]
        else:
            url = article["href"]
        update.message.reply_text(
            f'Новость: {article.text}\n Ссылка: {url}'
        )

def main():
    # Your Telegram token
    updater = Updater("5988650326:AAFV4P09YOAYDc7wYibV90AWqABrBG4NSrM", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("news", news))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()