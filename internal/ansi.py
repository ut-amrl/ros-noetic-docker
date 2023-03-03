PREFIX = "\x1b["

# Color sequences
RED = PREFIX + "31m"
GREEN = PREFIX + "32m"
YELLOW = PREFIX + "33m"
CYAN = PREFIX + "36m"

# SGR sequences
RESET = PREFIX + "0m"
BOLD = PREFIX + "1m"
BLINK = PREFIX + "5m"
NO_BOLD = PREFIX + "22m"
NO_BLINK = PREFIX + "25m"

# Control Sequences
PREV_LINE = PREFIX + "1F"
CLEAR_LINE = PREFIX + "2K"
