# The community rule already handles `open {user.website}`. Rebecca also uses
# `bring me <website>` as an alias, so keep that alias explicit here.
bring me {user.website}: user.open_url(website)

open talon home page: user.open_url("http://talonvoice.com")
bring me talon home page: user.open_url("http://talonvoice.com")
open talon slack: user.open_url("http://talonvoice.slack.com/messages/help")
bring me talon slack: user.open_url("http://talonvoice.slack.com/messages/help")
open talon wiki: user.open_url("https://talon.wiki/")
bring me talon wiki: user.open_url("https://talon.wiki/")
open talon practice: user.open_url("https://chaosparrot.github.io/talon_practice/")
bring me talon practice: user.open_url("https://chaosparrot.github.io/talon_practice/")
open talon repository search: user.open_url("https://search.talonvoice.com/search/")
bring me talon repository search: user.open_url("https://search.talonvoice.com/search/")
open amazon: user.open_url("https://www.amazon.com/")
bring me amazon: user.open_url("https://www.amazon.com/")
open dropbox: user.open_url("https://dropbox.com/")
bring me dropbox: user.open_url("https://dropbox.com/")
open google: user.open_url("https://www.google.com/")
bring me google: user.open_url("https://www.google.com/")
open google calendar: user.open_url("https://calendar.google.com")
bring me google calendar: user.open_url("https://calendar.google.com")
open google maps: user.open_url("https://maps.google.com/")
bring me google maps: user.open_url("https://maps.google.com/")
open google scholar: user.open_url("https://scholar.google.com/")
bring me google scholar: user.open_url("https://scholar.google.com/")
open gmail: user.open_url("https://mail.google.com/")
bring me gmail: user.open_url("https://mail.google.com/")
open github: user.open_url("https://github.com/")
bring me github: user.open_url("https://github.com/")
open gist: user.open_url("https://gist.github.com/")
bring me gist: user.open_url("https://gist.github.com/")
open wikipedia: user.open_url("https://en.wikipedia.org/")
bring me wikipedia: user.open_url("https://en.wikipedia.org/")
open youtube: user.open_url("https://www.youtube.com/")
bring me youtube: user.open_url("https://www.youtube.com/")

amazon hunt <user.text>$: user.search_with_search_engine("https://www.amazon.com/s/?field-keywords=%s", user.text)
amazon (that | this):
    text = edit.selected_text()
    user.search_with_search_engine("https://www.amazon.com/s/?field-keywords=%s", text)
amazon paste: user.search_with_search_engine("https://www.amazon.com/s/?field-keywords=%s", clip.text())

google hunt <user.text>$: user.search_with_search_engine("https://www.google.com/search?q=%s", user.text)
google (that | this):
    text = edit.selected_text()
    user.search_with_search_engine("https://www.google.com/search?q=%s", text)
google paste: user.search_with_search_engine("https://www.google.com/search?q=%s", clip.text())

map hunt <user.text>$: user.search_with_search_engine("https://maps.google.com/maps?q=%s", user.text)
map (that | this):
    text = edit.selected_text()
    user.search_with_search_engine("https://maps.google.com/maps?q=%s", text)
map paste: user.search_with_search_engine("https://maps.google.com/maps?q=%s", clip.text())

scholar hunt <user.text>$: user.search_with_search_engine("https://scholar.google.com/scholar?q=%s", user.text)
scholar (that | this):
    text = edit.selected_text()
    user.search_with_search_engine("https://scholar.google.com/scholar?q=%s", text)
scholar paste: user.search_with_search_engine("https://scholar.google.com/scholar?q=%s", clip.text())

wiki hunt <user.text>$: user.search_with_search_engine("https://en.wikipedia.org/w/index.php?search=%s", user.text)
wiki (that | this):
    text = edit.selected_text()
    user.search_with_search_engine("https://en.wikipedia.org/w/index.php?search=%s", text)
wiki paste: user.search_with_search_engine("https://en.wikipedia.org/w/index.php?search=%s", clip.text())
