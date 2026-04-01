app: chrome
tag: browser
browser.host: chat.openai.com
browser.host: chatgpt.com
-

chat new: user.chatgpt_mod("shift-o")
chat focus: key(shift-esc)
chat copy code: user.chatgpt_mod("shift-;")
chat copy: user.chatgpt_mod("shift-c")

chat custom: user.chatgpt_mod("shift-i")
chat toggle: user.chatgpt_mod("shift-s")
chat trash: user.chatgpt_mod("shift-backspace")

# chat send message <user.text>: user.chatgpt_send_message(text)
