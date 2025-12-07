Title: Talon 0.4.0 documentation

URL Source: https://talonvoice.com/docs/

Markdown Content:
Introduction[¶](https://talonvoice.com/docs/#introduction "Link to this heading")
---------------------------------------------------------------------------------

Overview[¶](https://talonvoice.com/docs/#overview "Link to this heading")
-------------------------------------------------------------------------

Talon aims to bring programming, realtime video gaming, command line, and full desktop computer proficiency to people who have limited or no use of their hands, and vastly improve productivity and wow-factor of anyone who can use a computer.

[Join the Slack](https://talonvoice.com/chat) to talk, get hyped, or for help with Talon.

NOTE: This Talon release is very new and is not fully documented yet! Please ask any questions in the #help channel on the Slack linked above.

*   System requirements:
    
    *   macOS High Sierra (10.13) or newer. Talon is a universal2 build with native Apple Silicon support.
        
    *   Linux / X11 (Ubuntu 18.04+, and most modern distros), Wayland support is currently limited to XWayland
        
    *   Windows 8 or newer
        
    
*   Powerful voice control - Talon comes with a free speech recognition engine, and it is also compatible with Dragon with no additional setup.
    
*   Multiple algorithms for eye tracking mouse control (depends on a single Tobii 4C, Tobii 5 or equivalent eye tracker)
    
*   Noise recognition system (pop and hiss). Many more noises coming soon.
    
*   Scriptable with Python 3 (via embedded CPython, no need to install or configure Python on your host system).
    
*   Talon is very modular and adaptable - you can use eye tracking without speech recognition, or vice versa.
    

Getting Started[¶](https://talonvoice.com/docs/#getting-started "Link to this heading")
---------------------------------------------------------------------------------------

1.  Download and install [Talon](https://talonvoice.com/) for your operating system.
    
2.  Run the Talon app.
    
3.  Open the Talon Home directory. This is `%APPDATA%\Talon` on Windows, and `~/.talon` on macOS/Linux. (Talon has a menu in your system tray near the clock, you can use `Scripting -> Open ~/.talon` as a shortcut open Talon Home).
    
4.  Add some scripts to `~/.talon/user` to add voice commands and other behaviour to Talon (see the [Getting Scripts](https://talonvoice.com/docs/#getting-scripts) section below). Your user scripts control all of the voice commands in Talon, so Talon won’t recognize any commands until you add some scripts.
    
5.  Install Conformer using Talon’s Speech Recognition menu.
    
6.  Go to `Scripting -> View Log` in the menu for debug output, or `Scripting -> Open REPL` for a Python command line.
    

Getting Scripts[¶](https://talonvoice.com/docs/#getting-scripts "Link to this heading")
---------------------------------------------------------------------------------------

The best way to get started right now is to clone [talonhub/community](https://github.com/talonhub/community) into your `~/.talon/user` directory. Ask in #help on Slack if you run into any problems.

Learning Talon[¶](https://talonvoice.com/docs/#learning-talon "Link to this heading")
-------------------------------------------------------------------------------------

These are some resources to help you learn to use and customize Talon:

*   [Talon Practice (by chaosparrot)](https://chaosparrot.github.io/talon_practice/)
    
*   [talonhub/community README](https://github.com/talonhub/community/blob/master/README.md)
    
*   [Unofficial Community Wiki](https://talon.wiki/)
    
*   [Search User Repositories](https://search.talonvoice.com/)
    

.talon Files[¶](https://talonvoice.com/docs/#talon-files "Link to this heading")
--------------------------------------------------------------------------------

Overview[¶](https://talonvoice.com/docs/#overview "Link to this heading")
-------------------------------------------------------------------------

Voice commands are defined in files with the `.talon` file extension, located in the `user` directory inside [Talon Home](https://talonvoice.com/docs/#getting-started).

`.talon` files can:

*   match specific applications, window titles, or other criteria
    
*   define voice commands
    
*   define global hotkeys
    
*   reimplement global actions (for example, to change the behavior of Talon in a specific application)
    
*   set settings
    
*   enable tags
    

Creating a file in `user` named `hello.talon` with these contents will declare a voice command:

hello talon: "hello world"

This means when you say `hello talon`, Talon will type `hello world`.

This is a more advanced example:

\# activate this .talon file if the current app name is "Chrome"
\# you can find app names by running ui.apps() in the REPL
app.name: Chrome
\-
\# key\_wait increases the delay when pressing keys (milliseconds)
\# this is useful if an app seems to jumble or drop keys
settings():
    key\_wait \= 4.0

\# activate the global tag "browser"
tag(): browser

\# define some voice commands
hello chrome: "hello world"
switch tab: key(ctrl\-tab)
go to google:
    \# note: use key(cmd-t) on Mac
    key(ctrl\-t)
    insert("google.com")
    key(enter)

The `-` on the line after after `app.name` is _important_.

*   Lines above the `-` are used to set criteria for activating the file.
    
*   Lines below the `-` declare things or activate tags.
    

Any line beginning with `#` is considered to be a comment and ignored.

API Reference[¶](https://talonvoice.com/docs/#module-talon "Link to this heading")
----------------------------------------------------------------------------------

_class_ talon.Context(_name: str \= None_, _\*_, _desc: str \= None_)[¶](https://talonvoice.com/docs/#talon.Context "Link to this definition")

Creating a Context:

from talon import Context
ctx \= Context()

action\_class(_path: str_) → Callable\[\[Class\], ActionClassProxy\][¶](https://talonvoice.com/docs/#talon.Context.action_class "Link to this definition")

@ctx.action\_class('prefix')
class Actions:
    def action\_name():
        print("Running actions.prefix.action\_name()")

action(_path: str_)[¶](https://talonvoice.com/docs/#talon.Context.action "Link to this definition")

@ctx.action('prefix.action\_name')
def action\_name():
    print("Running actions.prefix.action\_name()")

capture(_path: str \= None_, _\*_, _rule: str \= None_) → Callable\[\[DecoratedT\], DecoratedT\][¶](https://talonvoice.com/docs/#talon.Context.capture "Link to this definition")

@ctx.capture('number', rule\='(one | two)')
def number(m) \-\> int:
    return 1 if m\[0\] \== 'one' else 2

dynamic\_list(_path: str_) → Callable\[\[DecoratedT\], DecoratedT\][¶](https://talonvoice.com/docs/#talon.Context.dynamic_list "Link to this definition")

@ctx.dynamic\_list('prefix.list\_name')
def list\_name() \-\> Union\[str, list\[str\], dict\[str, str\]\]:
    return \['word', 'word'\]

_property_ matches_: str_[¶](https://talonvoice.com/docs/#talon.Context.matches "Link to this definition")

Describe when to activate this Context. If not specified, Context is always active.

ctx.matches \= r"""
os: windows
app.name: Slack
"""

Type:

str

_property_ apps[¶](https://talonvoice.com/docs/#talon.Context.apps "Link to this definition")

apps:

ctx.apps\["chrome"\] \= r"""
os: windows
app.name: Google Chrome
"""

Type:

str

_property_ selections_: dict\[str, str\]_[¶](https://talonvoice.com/docs/#talon.Context.selections "Link to this definition")

selections:

ctx.selections\["user.listname"\] \= """
some text to use for a subset selection
"""

Type:

dict\[str, str\]

_property_ lists_: dict\[str, Mapping\[str, str\]\]_[¶](https://talonvoice.com/docs/#talon.Context.lists "Link to this definition")

lists:

ctx.lists\["user.listname"\] \= \["word", "word2"\]
ctx.lists\["user.listname"\] \= {
    "pronunciation": "word",
}

Type:

dict\[str, Union\[list\[str\], dict\[str, str\]\]\]

_property_ settings[¶](https://talonvoice.com/docs/#talon.Context.settings "Link to this definition")

settings:

ctx.settings \= {
    "input\_wait": 1.0,
}

Type:

dict\[str, Any\]

_property_ tags[¶](https://talonvoice.com/docs/#talon.Context.tags "Link to this definition")

tags:

ctx.tags \= \["user.terminal"\]

Type:

frozenset\[str\]

_property_ commands_: Mapping\[str, CommandImpl\]_[¶](https://talonvoice.com/docs/#talon.Context.commands "Link to this definition")

Return the commands defined by this Context

Type:

dict\[str, CommandImpl\]

_property_ hotkeys_: Mapping\[str, ScriptImpl\]_[¶](https://talonvoice.com/docs/#talon.Context.hotkeys "Link to this definition")

Return the hotkeys defined by this Context

Type:

dict\[str, ScriptImpl\]

_class_ talon.Module(_name: str \= None_, _\*_, _desc: str \= None_)[¶](https://talonvoice.com/docs/#talon.Module "Link to this definition")

Creating a Module:

from talon import Module
mod \= Module()

action\_class(_cls: Class_) → ActionClassProxy[¶](https://talonvoice.com/docs/#talon.Module.action_class "Link to this definition")

@mod.action\_class
class Actions:
    def action\_name():
        "Description of the action"

    def second\_action(arg1: int, arg2: str\='') \-\> str:
        "Action with arguments, return type, and body"
        return 'test'

action(_func: DecoratedT_) → ActionDecl\[DecoratedT\][¶](https://talonvoice.com/docs/#talon.Module.action "Link to this definition")

@mod.action
def action\_name():
    "Description of the action"

capture(_\*_, _rule: str_) → Callable\[\[DecoratedT\], DecoratedT\][¶](https://talonvoice.com/docs/#talon.Module.capture "Link to this definition")

capture(_func: DecoratedT_) → DecoratedT

@mod.capture
def capture\_name() \-\> str:
    "Description of the capture"

scope(_func: ScopeFunc_) → ScopeDecl[¶](https://talonvoice.com/docs/#talon.Module.scope "Link to this definition")

@mod.scope
def scope():
    return {
        "key": "value",
    }

\# call scope.update() at any time to force a scope update

setting(_name: str, type: ~typing.Type\[~talon.scripting.types.T\], default: ~talon.scripting.types.T | ~talon.scripting.types.SettingDecl.NoValueType \= <talon.scripting.types.SettingDecl.NoValueType object\>, desc: str \= None_) → SettingDecl\[T\][¶](https://talonvoice.com/docs/#talon.Module.setting "Link to this definition")

mod.setting("setting\_name", int, default\=0, desc\="an example integer setting")
mod.setting("setting\_name\_2", str, default\='', desc\="an example string setting")

list(_name: str_, _desc: str \= None_) → NameDecl[¶](https://talonvoice.com/docs/#talon.Module.list "Link to this definition")

mod.list("list\_name", desc\="list description")

mode(_name: str_, _desc: str \= None_) → NameDecl[¶](https://talonvoice.com/docs/#talon.Module.mode "Link to this definition")

mod.mode("mode\_name", desc\="mode description")

tag(_name: str_, _desc: str \= None_) → NameDecl[¶](https://talonvoice.com/docs/#talon.Module.tag "Link to this definition")

mod.tag("tag\_name", desc\="tag description")

talon.actions[¶](https://talonvoice.com/docs/#talon.actions "Link to this definition")

…

talon.registry[¶](https://talonvoice.com/docs/#talon.registry "Link to this definition")

…

talon.scope[¶](https://talonvoice.com/docs/#talon.scope "Link to this definition")

…

talon.settings[¶](https://talonvoice.com/docs/#talon.settings "Link to this definition")

…

talon.storage[¶](https://talonvoice.com/docs/#talon.storage "Link to this definition")

…

talon.app[¶](https://talonvoice.com/docs/#talon-app "Link to this heading")
---------------------------------------------------------------------------

talon.app.register(_topic: str_, _cb: Callable_) → None[¶](https://talonvoice.com/docs/#talon.app.register "Link to this definition")

Register for an application event.

*   `ready`: Talon is ready. Your callback will be called after Talon launch and during script reloads.
    
*   `launch`: Talon launched. Your callback will only be called immediately after Talon launch.
    
*   `startup`: Talon launched during system startup.
    

from talon import app

def app\_ready():
    print("Talon is ready")
app.register("ready", app\_ready)

talon.app.unregister(_topic: Any_, _cb: Callable_) → None[¶](https://talonvoice.com/docs/#talon.app.unregister "Link to this definition")

Unregister a previously registered event:

app.unregister("ready", app\_ready)

talon.app.notify(_title: str \= None_, _subtitle: str \= None_, _body: str \= None_, _sound: bool \= False_) → None[¶](https://talonvoice.com/docs/#talon.app.notify "Link to this definition")

Display a desktop notification, optionally playing a sound.

from talon import app

app.notify(body\="Hello world")
app.notify(title\="Hello world",
           subtitle\="Welcome to Talon",
           body\="Enjoy your stay.",
           sound\=True)

talon.clip[¶](https://talonvoice.com/docs/#talon-clip "Link to this heading")
-----------------------------------------------------------------------------

talon.clip.has\_mode(_mode: str_) → bool[¶](https://talonvoice.com/docs/#talon.clip.has_mode "Link to this definition")

Check if a clipboard mode is supported.

Useful modes: “main”, “select”, “find”

talon.clip.text(_\*_, _mode: str \= None_) → str | None[¶](https://talonvoice.com/docs/#talon.clip.text "Link to this definition")

Get the text contents of the clipboard.

talon.clip.set\_text(_s: str_, _\*_, _mode: str \= None_) → None[¶](https://talonvoice.com/docs/#talon.clip.set_text "Link to this definition")

Set the text contents of the clipboard.

talon.clip.image(_\*_, _mode: str \= None_) → Image | None[¶](https://talonvoice.com/docs/#talon.clip.image "Link to this definition")

Get the image contents of the clipboard.

talon.clip.set\_image(_image: Image_, _\*_, _mode: str \= None_) → None[¶](https://talonvoice.com/docs/#talon.clip.set_image "Link to this definition")

Set the image contents of the clipboard.

talon.clip.clear(_\*_, _mode: str \= None_) → None[¶](https://talonvoice.com/docs/#talon.clip.clear "Link to this definition")

Clear the clipboard.

_exception_ talon.clip.NoChange[¶](https://talonvoice.com/docs/#talon.clip.NoChange "Link to this definition")

talon.clip.revert(_\*_, _old: PyMimeData \= None_, _mode: str \= None_) → Generator\[None, None, None\][¶](https://talonvoice.com/docs/#talon.clip.revert "Link to this definition")

Restore the old contents of the clipboard after running a block:

from talon import clip

with clip.revert():
    clip.set\_text("this will only be set temporarily")

talon.clip.capture(_timeout: float \= 0.5_, _\*_, _inc: int \= 0_, _mode: str \= None_, _formats: list\[str\] \= None_) → Generator\[ChangePromise, None, None\][¶](https://talonvoice.com/docs/#talon.clip.capture "Link to this definition")

Capture a change in the clipboard, then restore the old text contents:

from talon import actions, clip

with clip.capture() as s:
    actions.edit.copy()
print(s.get())

talon.fs[¶](https://talonvoice.com/docs/#talon-fs "Link to this heading")
-------------------------------------------------------------------------

from talon import fs

def on\_change(path, flags):
    if flags.renamed:
        print("renamed", path)
    if flags.exists:
        print("changed", path)
    else:
        print("deleted", path)

fs.watch('/path/to/stuff', on\_change)

_class_ talon.fs.FsEventFlags(_exists: bool_, _renamed: bool_, _stat: os.stat\_result | None_)[¶](https://talonvoice.com/docs/#talon.fs.FsEventFlags "Link to this definition")

talon.fs.watch(_path: str_, _cb: Callable\[\[str, [FsEventFlags](https://talonvoice.com/docs/index.html#talon.fs.FsEventFlags "talon.fs.FsEventFlags")\], None\]_) → None[¶](https://talonvoice.com/docs/#talon.fs.watch "Link to this definition")

Watch _path_ for changes and call `cb(path: str, flags: FsEventFlags)` when changes occur.

talon.fs.unwatch(_path: str_, _cb: Callable\[\[str, [FsEventFlags](https://talonvoice.com/docs/index.html#talon.fs.FsEventFlags "talon.fs.FsEventFlags")\], None\]_) → None[¶](https://talonvoice.com/docs/#talon.fs.unwatch "Link to this definition")

Remove _cb_ from the set of callbacks being watched for _path_.

talon.noise[¶](https://talonvoice.com/docs/#talon-noise "Link to this heading")
-------------------------------------------------------------------------------

talon.noise.register(_topic: Any_, _cb: Callable_) → None[¶](https://talonvoice.com/docs/#talon.noise.register "Link to this definition")

Register for a noise event.

*   `""` - an empty string registers the callback for all noises.
    
*   `"pop"`
    
*   `"hiss"`
    

from talon import noise

def on\_pop(active):
    print("pop")
noise.register("pop", on\_pop)

def on\_hiss(active):
    print("hiss", active)
noise.register("hiss", on\_hiss)

talon.noise.unregister(_topic: Any_, _cb: Callable_) → None[¶](https://talonvoice.com/docs/#talon.noise.unregister "Link to this definition")

Unregister a previously registered event:

noise.unregister("pop", on\_pop)
No text detected.
Try a screenshot instead.
0
:
00

