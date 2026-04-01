tag: browser
browser.host: chat.openai.com
browser.host: chatgpt.com
title: /ChatGPT/
-
next chat: user.chatgpt_mod("shift-n")
show chats: user.chatgpt_mod("shift-a")
hide chats: user.chatgpt_mod("shift-a")

send message: user.chatgpt_mod("enter")
new line: key(shift-enter)
clear chat: user.chatgpt_mod("backspace")

regenerate: user.chatgpt_mod("r")
stop response: user.chatgpt_mod(".")

scroll top: user.chatgpt_mod("home")
scroll end: user.chatgpt_mod("end")
