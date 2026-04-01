app: cursor
os: mac
-

# --- Journal article note-taking ---

copy to notes:
    user.article_copy_to_notes()

article copy to notes:
    user.article_copy_to_notes()

tag {user.article_tag}:
    user.article_tag(article_tag)

add note <user.text>:
    user.article_add_note(text)

article note add <user.text>:
    user.article_add_note(text)

open article notes:
    user.article_open_notes()

article notes open:
    user.article_open_notes()

capture sentence to notes:
    user.article_capture_sentence_to_notes()

article sentence capture:
    user.article_capture_sentence_to_notes()
