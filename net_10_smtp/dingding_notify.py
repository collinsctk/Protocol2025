from dingtalkchatbot.chatbot import DingtalkChatbot

qyt_webhook = 'https://oapi.dingtalk.com/robot/send?access_token=3957a042c05384519b4257656ff85e5055540ee4e0637b1272266ff894c90e83'


# dingding组群发MarkDown
def send_group_msg(webhook, title, text, is_at_all=True):
    dingdingbot = DingtalkChatbot(webhook)
    dingdingbot.send_markdown(title=title, text=text, is_at_all=is_at_all)


if __name__ == "__main__":
    send_group_msg(qyt_webhook, 'title', 'text')
