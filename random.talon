[focus] title <phrase>: user.switcher_focus_app_title("*", "{phrase}")
cursor <phrase>: user.switcher_focus_app_title("Cursor", "{phrase}")

(direct | edit) <user.system_path>:
    user.open_file_custom(system_path)
folder <user.system_path>:
    insert(system_path)

website repository: insert("https://github.com/RebeccaStevenson/reversal-learning")

insert date: user.insert_current_date()
insert date long: user.insert_current_date("%A, %B %d, %Y")
lower: key(down:12)
hire: key(up:12)

prompt debug: insert("Below you will find a script followed by the output from running the script. Could you please help me debug the following error:")
dough: edit.line_insert_down()
bow: edit.line_insert_up()

terminal Settings: insert("Import-Module PSReadLine")
import module: insert("Import-Module PSReadLine")

add daily note <user.text>:
    user.add_daily_note(text)

add note <user.text>:
    user.append_to_daily_note_text(text)

[create] daily note <user.text>:
    user.create_or_append_date_note_text(text)

(add) <user.system_path>:
    user.open_file_custom(system_path)
    sleep(300ms)
    edit.file_start()
    sleep(400ms)
    
    # Only run date formatting and key commands if it's notes.md
    user.maybe_disable_speech_for_notes(system_path)
    
(continue) <user.system_path>:
    user.open_file_custom(system_path)
    sleep(200ms)
    edit.file_start()
    sleep(200ms)    
    edit.line_insert_down()


therapy note <user.text>:
    user.add_note_to_physical_therapy(text)

recording start: user.recording_start()
recording stop: user.recording_stop()

cut paste: 
    key(alt-cmd-v)
    user.play_thunk()
