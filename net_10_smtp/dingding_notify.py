import os   
from dingtalkchatbot.chatbot import DingtalkChatbot

qyt_webhook = os.environ.get('DINGDINGWEBHOOK')

# dingding组群发MarkDown
def send_group_msg(webhook, title, text, is_at_all=True):
    dingdingbot = DingtalkChatbot(webhook)
    dingdingbot.send_markdown(title=title, text=text, is_at_all=is_at_all)


if __name__ == "__main__":
    send_group_msg(qyt_webhook, 'title', 'text')
