
## Cursorless Cheatsheet

### Actions

- **Spoken form** | **Meaning**
- [pair] repack [target] | Rewrap [target] with [pair]
- [pair] wrap [target] | Wrap [target] with [pair]
- bottom [target] | Scroll to bottom
- break point [target] | Toggle line breakpoint
- bring [target] | Insert copy of [target] at cursor
- bring [target] [destination] | Copy [target] to [destination]
- call [target] | Call [target] on selection
- carve [target] | Cut to clipboard
- center [target] | Scroll to center
- change [target] | Clear and set selection
- chuck [target] | Remove
- clone [target] | Insert copy after
- clone up [target] | Insert copy before
- comment [target] | Toggle line comment
- copy [target] | Copy to clipboard
- crown [target] | Scroll to top
- dedent [target] | Outdent line
- define [target] | Reveal definition
- drink [target] | Edit new line before
- drop [target] | Insert empty line before
- extract [target] | Extract variable
- float [target] | Insert empty line after
- fold [target] | Fold region
- follow [target] | Follow link
- format [formatter] at [target] | Reformat [target] as [formatter]
- give [target] | Deselect
- highlight [target] | Highlight
- hover [target] | Show hover
- indent [target] | Indent line
- inspect [target] | Show debug hover
- move [target] | Move [target] to cursor position
- move [target] [destination] | Move [target] to [destination]
- paste [destination] | Paste from clipboard at [destination]
- phones [target] | Next homophone
- post [target] | Set selection after
- pour [target] | Edit new line after
- pre [target] | Set selection before
- puff [target] | Insert empty lines around
- quick fix [target] | Show quick fix
- reference [target] | Show references
- rename [target] | Rename
- reverse [target] | Reverse targets
- scout [target] | Find in document
- scout all [target] | Find in workspace
- shuffle [target] | Randomize targets
- snippet [target] | Insert snippet
- snippet make [target] | Generate snippet
- sort [target] | Sort targets
- swap [target 1] with [target 2] | Swap [target 1] with [target 2]
- swap with [target] | Swap selection with [target]
- take [target] | Set selection
- type deaf [target] | Reveal type definition
- unfold [target] | Unfold region

### Destinations

- **Spoken form** | **Meaning**
- `after [target]` | Insert after [target]
- `before [target]` | Insert before [target]
- `to [target]` | Replace [target]

### Scopes

- **Spoken form** | **Meaning**
- arg | Argument
- attribute | Attribute
- block | Paragraph
- branch | Branch
- call | Function call
- callee | Function callee
- cell | Notebook cell
- chapter | Chapter
- char | Character
- class | Class
- class name | Class name
- command | Command
- comment | Comment
- condition | Condition
- element | Xml element
- end tag | Xml end tag
- environment | Environment
- file | Document
- funk | Named function
- funk name | Function name
- identifier | Identifier
- if state | If statement

- instance | Instance

- item | Collection item
- key | Collection key
- lambda | Anonymous function
- line | Line
- link | Url
- list | List
- map | Map
- name | Name
- paint | Non whitespace sequence
- paragraph | Named paragraph
- part | Part
- regex | Regular expression
- section | Section
- selector | Selector
- sentence | Sentence
- short paint | Bounded non whitespace sequence
- start tag | Xml start tag
- state | Statement
- subparagraph | Sub paragraph
- subsection | Sub section
- subsubsection | Sub sub section
- tags | Xml both tags
- token | Token
- type | Type
- unit | Unit
- value | Value
- word | Word

### Scope Visualizer

- **Spoken form** | **Meaning**
- `visualize [scope]` | Visualize [scope]
- `visualize [scope] iteration` | Visualize [scope] iteration range
- `visualize [scope] removal` | Visualize [scope] removal range
- `visualize nothing` | Hide scope visualizer

### Modifiers

- **Spoken form** | **Meaning**
- `[number] [scope]s` | [number] instances of [scope] including target, going forwards
- `[number] [scope]s backward` | [number] instances of [scope] including target, going backwards
- `[nth] [scope]` | [nth] instance of [scope] in iteration scope
- `[nth] last [scope]` | [nth]-to-last instance of [scope] in iteration scope
- `[nth] next [scope]` | [nth] instance of [scope] after target
- `[nth] previous [scope]` | [nth] instance of [scope] before target
- `[scope]` | Containing instance of [scope]
- `[scope] backward` | Single instance of [scope] including target, going backwards
- `[scope] forward` | Single instance of [scope] including target, going forwards
- `bounds` | Bounding paired delimiters
- `content` | Keep content filter
- `empty` | Keep empty filter
- `end of` | Empty position at end of target
- `every [scope]` | Every instance of [scope]
- `first [number] [scope]s` | First [number] instances of [scope] in iteration scope
- `head` | Extend through start of line
- `head [modifier]` | Extend through start of [modifier]
- `inside` | Interior only
- `its` | Infer previous mark
- `just` | No inference
- `last [number] [scope]s` | Last [number] instances of [scope] in iteration scope
- `leading` | Leading delimiter range
- `next [number] [scope]s` | Next [number] instances of [scope]
- `next [scope]` | Next instance of [scope]
- `previous [number] [scope]s` | Previous [number] instances of [scope]
- `previous [scope]` | Previous instance of [scope]
- `start of` | Empty position at start of target
- `tail` | Extend through end of line
- `tail [modifier]` | Extend through end of [modifier]
- `trailing` | Trailing delimiter range

### Paired Delimiters

- **Spoken form** | **Meaning**
- `box` | Square brackets
- `curly` | Curly brackets
- `diamond` | Angle brackets
- `escaped box` | Escaped square brackets
- `escaped quad` | Escaped double quotes
- `escaped round` | Escaped parentheses
- `escaped twin` | Escaped single quotes
- `pair` | Any
- `quad` | Double quotes
- `round` | Parentheses
- `skis` | Backtick quotes
- `twin` | Single quotes
- `void` | Whitespace

### Special Marks

- **Spoken form** | **Meaning**
- `down [number]` | Line number down from cursor
- `nothing` | Nothing
- `row [number]` | Line number modulo 100
- `source` | Previous source
- `special` | Unknown symbol
- `that` | Previous target
- `this` | Current selection
- `up [number]` | Line number up from cursor

### Compound Targets

- **Spoken form** | **Meaning**
- `[target 1] and [target 2]` | [target 1] and [target 2]
- `[target 1] between [target 2]`

 | Between [target 1] and [target 2]
- `[target 1] past [target 2]` | [target 1] through [target 2]
- `[target 1] slice [target 2]` | [target 1] vertically through [target 2]
- `[target 1] until [target 2]` | [target 1] until start of [target 2]
- `between [target]` | Between selection and [target]
- `past [target]` | Selection through [target]
- `slice [target]` | Selection vertically through [target]
- `until [target]` | Selection until start of [target]