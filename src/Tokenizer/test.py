
import logging

# Adjust the import path if necessary
# Import your modules
logging.basicConfig(level=logging.CRITICAL)

from SyntaxicExtraction import SyntaxicExtraction

# Now you can use the SyntaxicExtraction class
if __name__ == "__main__":
    text = "les chats mangent la souris"
    nlp = SyntaxicExtraction(text)
    tokens = nlp.tokens

    # Process the tokens as needed
    for token in tokens:
        print(token)