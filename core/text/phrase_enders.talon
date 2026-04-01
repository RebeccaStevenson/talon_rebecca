# Functional phrase enders
# These complement "over" (which just terminates via the phrase_ender list)

# ── Enter: insert text then press Enter ──
phrase <user.text> enter:
    user.add_phrase_to_history(text)
    insert(text)
    key(enter)
{user.prose_formatter} <user.prose> enter:
    user.insert_formatted(prose, prose_formatter)
    key(enter)
<user.format_code>+ enter:
    user.insert_many(format_code_list)
    key(enter)

# ── Space: insert text then add a trailing space ──
phrase <user.text> space:
    user.add_phrase_to_history(text)
    insert(text)
    key(space)
{user.prose_formatter} <user.prose> space:
    user.insert_formatted(prose, prose_formatter)
    key(space)
<user.format_code>+ space:
    user.insert_many(format_code_list)
    key(space)

# ── Tab: insert text then press Tab ──
phrase <user.text> tab:
    user.add_phrase_to_history(text)
    insert(text)
    key(tab)
{user.prose_formatter} <user.prose> tab:
    user.insert_formatted(prose, prose_formatter)
    key(tab)
<user.format_code>+ tab:
    user.insert_many(format_code_list)
    key(tab)

# ── Escape: insert text then press Escape ──
phrase <user.text> escape:
    user.add_phrase_to_history(text)
    insert(text)
    key(escape)
{user.prose_formatter} <user.prose> escape:
    user.insert_formatted(prose, prose_formatter)
    key(escape)
<user.format_code>+ escape:
    user.insert_many(format_code_list)
    key(escape)

# ── Scratch that: cancel the phrase without inserting ──
phrase <user.text> scratch that:
    skip()
{user.prose_formatter} <user.prose> scratch that:
    skip()
<user.format_code>+ scratch that:
    skip()
