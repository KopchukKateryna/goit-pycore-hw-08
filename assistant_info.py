BOT_COMMANDS = [
    {"command": "hello", "usage": "hello", "exmp": "hello"},
    {"command": "info", "usage": "info", "exmp": "info"},
    {"command": "add", "usage": "add <name> <number>", "exmp": "add kate 1234567890"},
    {
        "command": "change",
        "usage": "change <name> <old_number> <new_number>",
        "exmp": "change kate 1234567890 0987654321",
    },
    {
        "command": "phone",
        "usage": "phone <name>",
        "exmp": "phone kate",
    },
    {
        "command": "delete",
        "usage": "delete <name>",
        "exmp": "delete kate",
    },
    {"command": "all", "usage": "all", "exmp": "all"},
    {
        "command": "add-birthday",
        "usage": "add-birthday <name> <birthday>",
        "exmp": "add-birthday kate 12.12.1221",
    },
    {
        "command": "show-birthday",
        "usage": "show-birthday <name>",
        "exmp": "show-birthday kate",
    },
    {"command": "birthdays", "usage": "birthdays", "exmp": "birthdays"},
    {"command": "close", "usage": "close", "exmp": "close"},
    {"command": "exit", "usage": "exit", "exmp": "exit"},
]

ASSISTANT_INFO_TABLE_HEADERS = ["COMMAND", "USAGE", "EXAMPLE"]
ASSISTANT_INFO_TABLE_DATA = [
    [c["command"], c["usage"], c["exmp"]] for c in BOT_COMMANDS
]
