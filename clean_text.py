from num_to_words import num_to_word
import re


def remove_spaces_and_hyphens(texts):
    # Replace all hyphens (single or consecutive) with spaces
    t = texts.replace('-', ' ').replace('--', ' ')
    t = t.replace('"', ' ')
    t = t.replace('’', ' ')
    t = t.replace("'", ' ')
    t = t.replace("‘", ' ')
    t = re.sub('       +', " ", t)  ### For removing long spaces
    # Remove leading and trailing white spaces
    t = t.strip()

    # Remove extra spaces between words (if any)
    t = ' '.join(t.split())

    return t


def translate_numerals_to_words(text, lang='ta'):
    # Split the text into words
    words = text.split()

    # Initialize a list to store translated words
    translated_words = []

    for word in words:
        # Check if the word is a numeral
        if word.replace(',', '', 1).replace('.', '', 1).isdigit():
            # Handle decimal numbers
            if '.' in word:
                integer_part, decimal_part = word.split('.')
                integer_word = num_to_word(int(integer_part), lang=lang)
                decimal_word = num_to_word(int(decimal_part), lang=lang)
                translated_word = f"{integer_word} point {decimal_word}"
            else:
                # Translate the numeral to words using your num_to_word function
                translated_word = num_to_word(int(word.replace(',', '')), lang=lang)
                
            translated_words.append(translated_word)
        else:
            # If it's not a numeral, leave it as it is
            translated_words.append(word)

    # Join the translated words into a single string
    translated_text = ' '.join(translated_words)

    return translated_text
