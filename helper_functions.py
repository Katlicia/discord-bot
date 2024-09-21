import re

def check_keyword(content, word):
    url_pattern = r'(https?://\S+|www\.\S+)'  # URL
    mention_pattern = r'(<@!?&?\d+>)'  # Mentions
    emoji_pattern = r'(<a?:\w+:\d+>)'  # Custom emotes

    content = re.sub(url_pattern, '', content)
    content = re.sub(mention_pattern, '', content)
    content = re.sub(emoji_pattern, '', content)

    pattern = fr'\b{re.escape(word)}\b'

    # Checks if word is in content.
    return bool(re.search(pattern, content))