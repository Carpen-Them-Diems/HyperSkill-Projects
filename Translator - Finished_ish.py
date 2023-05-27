import requests
import argparse
from bs4 import BeautifulSoup as Bs
import sys


# 1. List of languages the translator will be able to translate, in a list, so they can be accessed by index.

languages_list = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
                  'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']


# 2. Printing a welcome message and enumerating the list of languages marked by index.

print('\nWelcome to TBO\'s Translator! Current supported languages include: ')
for index, language in enumerate(languages_list, 1):
    print(f'{index}. {language}')


# 3. Collecting the source and target languages from the user, either through user input using the input()
# functions, or by taking them directly through the CLI using the argparse library.

# Command line interface input collection
parser = argparse.ArgumentParser()

parser.add_argument('source', nargs='?', default=None, type=str, help='Choose the source language to translate from.')
parser.add_argument('target', nargs='?', default=None, type=str, help='Choose the target language to translate to or '
                                                                      '"all" to translate to all available languages.')
parser.add_argument('words', nargs='*', default=None, type=str, help='Choose the word/words to translate.')

parser.add_argument('--src', nargs='?', default=None, type=str, help='Choose the source language to translate from.')
parser.add_argument('--trg', nargs='?', default=None, type=str, help='Choose the target language to translate to or '
                                                                     '"all" to translate to all available languages.')
parser.add_argument('--w', nargs='*', default=None, type=str, help='Choose the word/words to translate.')

args = parser.parse_args()

all_languages = False
source_language = None
target_languages = None
words = None

if args.source is None and args.src is None:
    source_language = str(input('\nType the source language you wish to translate from: '))
    target_languages = str(input('Type the target to language you would like to translate to or \'all\' '
                                 'for all languages: '))
    # save_file = str(input('Would you like to save the translations to a file - (Yes/No): '))
    words = str(input('Type the word/words you would like to translate: '))

save_file = str(input('Would you like to save results as a file? - (Y/N)'))


#** Attempting to also strip any possible whitespaces off the beginning and ends of the words but cant get it. **#

# arg_list = [args.source, args.target, args.words, args.src, args.trg, args.w, source_language, target_languages,words]
# cleaned_args = []
# print(arg_list)
# for arg in arg_list:
#     if arg is not None and arg is not list:
#         arg = str(arg).strip()
#         cleaned_args.append(arg)
#     elif arg is None or arg is list:
#         cleaned_args.append(arg)
#
# args.source = str(cleaned_args[0])
# args.target = str(cleaned_args[1])
# args.words = str(cleaned_args[2])
# args.src = str(cleaned_args[3])
# args.trg = str(cleaned_args[4])
# args.w = str(cleaned_args[5])
# source_language = str(cleaned_args[6])
# target_languages = str(cleaned_args[7])
# words = str(cleaned_args[8])


# 4. Checking the user inputs for errors and handling them with exception/error handling.

if args.target == 'all' or args.trg == 'all' or target_languages == 'all':
    if (args.source or args.src or source_language) in list(map(str.lower, languages_list)):
        source_language = args.source or args.src or source_language
        target_languages = languages_list
        target_languages.remove(source_language.capitalize())
        target_languages_dict = {index: language for index, language in enumerate(target_languages)}
        words = args.words or args.w or words
        all_languages = True

        if words or args.words or args.w is list:
            print(f'\nYou chose \'{" ".join(words).capitalize()}\' as the words to translate from '
                  f'{source_language.capitalize()} to {" ".join(target_languages)}.')
        else:
            print(f'\nYou chose \'{words.capitalize()}\' as the words to translate from '
                  f'{str(source_language).capitalize()} to {str(target_languages).capitalize()}')
    else:
        print(f"Sorry, the program doesn't support \"{args.src or args.source or source_language}\", "
              f"please check your spelling and/or choose a valid option from the provided list, thank you!")
        sys.exit(1)


elif (args.src and args.trg) is None and (source_language and target_languages) is None:
    if args.source.lower() not in list(map(str.lower, languages_list)):
        print(f"Sorry, the program doesn't support \"{args.source}\", please check your spelling and/or choose "
              f"a valid option from the provided list, thank you!")
        sys.exit(1)
    elif args.target.lower() not in list(map(str.lower, languages_list)) and args.target.lower() != 'all':
        print(f"Sorry, the program doesn't support \"{args.target}\", please check your spelling and/or choose "
              f"a valid option from the provided list, thank you!")
        sys.exit(1)

elif (args.source and args.target) is None and (source_language and target_languages is None):
    if args.src.lower() not in list(map(str.lower, languages_list)):
        print(f"Sorry, the program doesn't support \"{args.src}\", please check your spelling and/or choose "
              f"a valid option from the provided list, thank you!")
        sys.exit(1)
    elif args.trg.lower() not in list(map(str.lower, languages_list)) and args.trg.lower() != 'all':
        print(f"Sorry, the program doesn't support \"{args.trg}\", please check your spelling and/or choose "
              f"a valid option from the provided list, thank you!")
        sys.exit(1)

elif (args.source and args.target is None) and (args.src and args.trg is None):
    if source_language.lower() not in list(map(str.lower, languages_list)):
        print(f"Sorry, the program doesn't support \"{source_language}\", please check your spelling and/or choose "
              f"a valid option from the provided list, thank you!")
        sys.exit(1)
    elif target_languages.lower() not in list(map(str.lower, languages_list)) and target_languages.lower() != 'all':
        print(f"Sorry, the program doesn't support \"{target_languages}\", please check your spelling and/or choose "
              f"a valid option from the provided list, thank you!")
        sys.exit(1)

else:
    source_language = args.src or args.source or source_language
    target_languages = args.trg or args.target or target_languages
    words = args.w or args.words or words
    print(words)
    if words is not list:
        print(f'\nYou chose \'{"".join(words).capitalize()}\' as the words to translate from '
              f'{str(source_language).capitalize()} to {str(target_languages).capitalize()}')
    else:
        print(f'\nYou chose \'{words.capitalize()}\' as the words to translate from '
              f'{str(source_language).capitalize()} to {str(target_languages).capitalize()}')


# 5. Getting the necessary url for the translations using f-string formatting,
# then requesting the raw data from the url and using BeautifulSoup (Bs) to parse the content using
# the built-in 'html parser'. Then we check the status code of the request to make sure the .get() request was
# successful, if it was then we gather the specific data we want from the raw_content using the .find_all()
# and .get_text() methods, strip away the extra whitespace with .strip() (and anything else necessary).
# We are looking for: translations of the word, source examples (src ltr) and target examples (trg ltr).
# ***To find the needed arguments for the .find_all() methods we can print the raw html data and look
# through it, or we can look through the html code on the website itself using dev tools.***

if type(words) is list:
    words = '+'.join(args.words or args.w or words)

if not all_languages:
    headers = {'User-Agent': "Mozilla/5.0"}

    try:
        url = f'https://context.reverso.net/translation/{source_language.lower()}-{target_languages.lower()}' \
              f'/{words.lower()}'
        r = requests.get(url, headers=headers)
        raw_content = Bs(r.content, 'html.parser')

        if r.status_code == 200:
            print(f'{r.status_code} OK\n')

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            print(f'HTTPError: Sorry, unable to find: {words}\nCheck to make sure you spelt the word '
                  f'correctly and try again, thank you.')
            sys.exit(2)

    except requests.ConnectionError as e:
        print(f'ConnectionError: {e}')
        print(f'Something wrong with your internet connection.')
        sys.exit(3)

    except Exception as ex:
        print(f'An error occurred: {ex}')
        sys.exit(0)

    else:

        # Find translations
        translations = [t.get_text(strip=True) for t in
                        raw_content.find_all('span', class_='display-term')]

        # FIND EXAMPLES:
        # Find source sentences
        source_sentences = raw_content.find_all('div', class_='src ltr')
        source_text = [t.get_text().strip() for t in source_sentences]

        # Find target sentences
        target_sentences = raw_content.find_all('div', class_=['trg ltr', f'{target_languages[:2]}'])
        target_text = [t.get_text().strip() for t in target_sentences]


# 6. The same thing here as 5 except with a loop to iterate through each language for an input of 'all' and appending
# them to lists to be used later.

elif all_languages:
    translations_list = []
    source_examples_list = []
    target_examples_list = []
    status = False
    count = 0

    for i in range(0, len(target_languages)):
        url = f'https://context.reverso.net/translation/{source_language.lower()}-{target_languages[i].lower()}' \
              f'/{words.lower()}'
        headers = {'User-Agent': "Mozilla/5.0"}

        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            raw_content = Bs(r.content, 'html.parser')

            if r.status_code == 200 and status is False:
                print(f'{r.status_code} OK\n')
                status = True

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print(f'HTTPError: Sorry, unable to find: {words}\nCheck to make sure you spelt the word '
                      f'correctly and try again, thank you.')
                sys.exit(2)

        except requests.exceptions.RequestException as e:
            print(f'Request Exception: {e}')
            print('Something wrong with your internet connection...\nCheck your connection and try again.')
            sys.exit(3)

        except Exception as ex:
            print(f'An error occurred: {ex}')
            sys.exit(0)

        else:

            # Find translations
            translations = [t.get_text(strip=True) for t in raw_content.find_all(['span', 'div'],
                            class_=["display-term", 'translation', 'translation rtl dict no-pos'])]
            print(translations)
            # FIND EXAMPLES:
            # Find source sentences
            source_sentences = raw_content.find_all('div', class_='src ltr')
            source_text = [t.get_text().strip() for t in source_sentences]

            # Find target sentences
            target_sentences = raw_content.find_all('div', class_=['trg ltr', 'trg rtl',
                                                                   target_languages_dict[i].lower()])
            target_text = [t.get_text().strip() for t in target_sentences]
            # print(target_text)
            if len(translations) == 0:
                print(f'There are no translations in "{target_languages[i]}" for your selected words, '
                      f'check your spelling or try less at a time.')
                sys.exit(0)

            # Append the recovered information as dictionaries for easy access to the lists above.
            translations_list.append({f'{target_languages[i]}': translations[0:3]})
            source_examples_list.append({f'{target_languages[i]}': source_text[0:3]})
            target_examples_list.append({f'{target_languages[i]}': target_text[0:3]})


# 7. Now we must define the function that will print out the correct translations and example sentences,
# in the proper format.


def print_results(target_langs, all):
    count = 0
    result = ''
    if not all:
        result += f'{target_langs.capitalize()} Translations: \n'
        for t in translations:
            if count < 5:
                result += f'{t}\n'
                count += 1
            else:
                count = 0
                break

        result += f'\n{target_langs.capitalize()} Examples: \n'
        for i in range(len(source_text)):
            if count < 5:
                result += f'{source_text[i]}\n{target_text[i]}\n\n'
                count += 1
            else:
                count = 0
                break

        print(result)
        print('Thank you for using TBO\'s translator, be sure to leave a comment/review if you\'d like to, this is '
              'my first project and I am only weeks into learning coding from scratch. So feedback is appreciated!')

        return result + '\nThank you for using TBO\'s translator, be sure to leave a comment/review if you\'d like ' \
                        'to, \nthis is my first project and I am only weeks into learning coding from scratch. ' \
                        '\nSo feedback is appreciated!'

    else:
        for i in range(len(target_langs)):
            result += f'\n{target_langs[i]} Translations: \n'
            for n in range(3):
                result += f'{translations_list[i][target_langs[i]][n]}\n'
            result += f'\n\n{target_langs[i]} Examples: \n'
            for m in range(3):
                result += f'{source_examples_list[i][target_langs[i]][m]}\n' \
                          f'{target_examples_list[i][target_langs[i]][m]}\n\n'

        print(result)
        print('Thank you for using TBO\'s translator, be sure to leave a comment/review if you\'d like to, this is '
              'my first project and I am only weeks into learning coding from scratch. So feedback is appreciated!')

        return result + '\nThank you for using TBO\'s translator, be sure to leave a comment/review if you\'d like ' \
                        'to,\nthis is my first project and I am only weeks into learning coding from scratch. ' \
                        '\nSo feedback is appreciated!'


# 8. Finally, we just have to call the functions while saving their outputs to a new file or overriding a
# previous one with the same name (the word being translated).

if not all_languages:
    if save_file.lower() == 'y':
        file_name = f'{words[:20]}.txt'
        with open(file_name, 'w+', encoding='utf-8') as save_results:
            save_results.write(print_results(target_languages, all_languages))
    else:
        print_results(target_languages, all_languages)

else:
    if save_file.lower() == 'y':
        file_name = f'{words[:20]}.txt'
        with open(file_name, 'w+', encoding='utf-8') as save_results:
            save_results.write(print_results(target_languages, all_languages))
    else:
        print_results(target_languages, all_languages)
