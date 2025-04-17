CHANNEL_ID = ""
CHAT_ID = ""

ADMIN_ID = ""

with open("filter_profanity_russian.txt") as file:
    WORDS = [row.strip() for row in file]