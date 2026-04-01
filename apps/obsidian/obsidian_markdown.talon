app: obsidian
-
# Markdown authoring and formatting helpers.

add H one [<user.text>]:
    insert("# ")
    user.insert_formatted(text or "", "CAPITALIZE_FIRST_WORD")

add H two [<user.text>]:
    insert("## ")
    user.insert_formatted(text or "", "CAPITALIZE_FIRST_WORD")

add H three [<user.text>]:
    insert("### ")
    user.insert_formatted(text or "", "CAPITALIZE_FIRST_WORD")

add H four [<user.text>]:
    insert("#### ")
    user.insert_formatted(text or "", "CAPITALIZE_FIRST_WORD")

add H five [<user.text>]:
    insert("##### ")
    user.insert_formatted(text or "", "CAPITALIZE_FIRST_WORD")

add list: insert("- ")
add task: insert("- [ ] ")
form bold [at this]: key(cmd-b)
form italic [at this]: key(cmd-i)

show (help | settings): key(cmd-,)
add (prop | tag): key(cmd-;)
