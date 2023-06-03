import nltk
from collections import defaultdict
import random
import re
from nltk.tokenize import RegexpTokenizer

# nltk.download('punkt')
print('Enter name of corpus file:')
corpus_input = str(input('> '))

with open(corpus_input, 'r', encoding='utf-8') as corpus:
    corpus_read = corpus.read()
    reg_tokenizer = RegexpTokenizer('\S+')
    corpus_tokens = reg_tokenizer.tokenize(corpus_read)
    corpus_bigrams = list(nltk.bigrams(corpus_tokens))

    model = defaultdict(lambda: defaultdict(int))
    for head, tail in corpus_bigrams:
        model[head][tail] += 1

    print(f'Corpus statistics: \n#Tokens: {len(corpus_tokens)}\n#Unique Tokens: {len(set(corpus_tokens))} '
          f'\n#Bigrams: {len(corpus_bigrams)} \n#Model Heads: {len(model.keys())}')

    while True:
        print('Enter a word found in the model to begin, \'auto\' to select randomly, or \'exit\' to exit program:')
        user_input = str(input('> '))

        print('Would you like to save the results to a file? Input the filename here to save or \'N\' to not save:')
        save = str(input('> '))

        if user_input.lower() == 'exit':
            break

        elif user_input != 'auto':
            print('Would you like to get the tail stats on your chosen word? (Y/N): > ')
            stats_input = str(input('> '))
            try:
                if stats_input.lower() == 'y':
                    if user_input in model:
                        print(f'Head: {user_input}')
                        for tail, count in model[user_input].items():
                            print(f'Tail: {tail}    Count: {count}')

                        count = 0
                        for _ in range(10):
                            start_word = user_input
                            proper_nouns = set()
                            for i, word in enumerate(corpus_tokens):
                                if word[0].isupper() and word[-1] not in '.!?':
                                    if i > 0 and corpus_tokens[i - 1][-1] not in '.!?':
                                        proper_nouns.add(word)

                            while True:
                                if start_word[0][-1] not in '.!?':
                                    break

                            chain = [start_word]
                            while len(chain) < 5 or chain[-1][-1] not in '.?!':
                                tails, weights = zip(*model[chain[-1]].items())
                                next_word = random.choices(population=tails, weights=weights)[0]
                                while next_word not in model:
                                    next_word = random.choices(population=tails, weights=weights)[0]
                                if next_word[0].isupper() and next_word not in proper_nouns:
                                    chain.append(next_word.lower())
                                else:
                                    chain.append(next_word)
                            chain[0] = chain[0].capitalize()
                            print(' '.join(chain))
                            content = ' '.join(chain)

                            if save.lower() != 'n':
                                with open(f'{save}.txt', 'a') as f:
                                    if count < 1:
                                        f.write(f'Generated Text For: {corpus_input}: Input Word: {user_input}\n\n')
                                        count += 1
                                    f.write(f'{count} - {content}\n\n')
                                    count += 1
                                    if count == 11:
                                        f.write('\n')

                    elif user_input not in model:
                        raise ValueError

                else:
                    count = 0
                    for _ in range(10):
                        if user_input in model:
                            start_word = user_input
                            proper_nouns = set()
                            for i, word in enumerate(corpus_tokens):
                                if word[0].isupper() and word[-1] not in '.!?':
                                    if i > 0 and corpus_tokens[i - 1][-1] not in '.!?':
                                        proper_nouns.add(word)

                            while True:
                                if start_word[0][-1] not in '.!?':
                                    break

                            chain = [start_word]
                            while len(chain) < 5 or chain[-1][-1] not in '.?!':
                                tails, weights = zip(*model[chain[-1]].items())
                                next_word = random.choices(population=tails, weights=weights)[0]
                                while next_word not in model:
                                    next_word = random.choices(population=tails, weights=weights)[0]
                                if next_word[0].isupper() and next_word not in proper_nouns:
                                    chain.append(next_word.lower())
                                else:
                                    chain.append(next_word)
                            chain[0] = chain[0].capitalize()
                            print(' '.join(chain))
                            content = ' '.join(chain)

                            if save.lower() != 'n':
                                with open(f'{save}.txt', 'a') as f:
                                    if count < 1:
                                        f.write(f'Generated Text For: {corpus_input}: Input Word: {user_input}\n\n')
                                        count += 1
                                    f.write(f'{count} - {content}\n\n')
                                    count += 1
                                    if count == 11:
                                        f.write('\n')

                        else:
                            raise ValueError

            except ValueError:
                print(f'Value Error. The requested word {user_input} is not in the model or does not have enough tail '
                      f'values to complete the full 10 generations. Please input another word and/or '
                      f'check capitalization, the inputs are case sensitive!.')
                print("Current model:", model[user_input])
                print('Would you like to print out the models head(key) values? (Y/N):')
                print_model = str(input('> '))
                if print_model.lower() == 'y':
                    print(set(model.keys()))
                    while True:
                        print('Would you like to search the head keys for a specific word? Input '
                              'the word if you\'d like to search for one, or \'n\' to exit:')
                        search_input = str(input('> '))
                        if search_input.lower() == 'n':
                            break
                        else:
                            if search_input in model.keys():
                                print(f'True: {search_input} is in the model')
                            else:
                                print(f'False: {search_input} is not in the model')
                elif print_model.lower() == 'n':
                    continue
                else:
                    raise ValueError('Please use \'y\' or \'n\' to continue, not cap-sensitive!')

        elif user_input == 'auto':
            count = 0
            for _ in range(10):
                start_words = []
                proper_nouns = set()
                for i, word in enumerate(corpus_tokens):
                    if word[0].isupper() and word[-1] not in '.!?':
                        if i > 0 and corpus_tokens[i - 1][-1] not in '.!?':
                            proper_nouns.add(word)
                            start_words.append(word)

                while True:
                    start_word = random.choice(start_words)
                    if start_word[-1] not in '.!?':
                        break

                chain = random.choices(start_words)
                while len(chain) < 5 or chain[-1][-1] not in '.?!':
                    tails, weights = zip(*model[chain[-1]].items())
                    next_word = random.choices(population=tails, weights=weights)[0]
                    while next_word not in model:
                        next_word = random.choices(population=tails, weights=weights)[0]
                    if next_word[0].isupper() and next_word not in proper_nouns:
                        chain.append(next_word)
                    else:
                        chain.append(next_word)
                print(' '.join(chain))
                content = ' '.join(chain)

                if save.lower() != 'n':
                    with open(f'{save}.txt', 'a') as f:
                        if count < 1:
                            f.write(f'Generated Text For: {corpus_input}: Input Word: {user_input}/{start_word}\n\n')
                            count += 1
                        f.write(f'{count} - {content}\n\n')
                        count += 1
                        if count == 11:
                            f.write('\n')

        print('Repeat the program? (Y/N):')
        repeat = str(input('> '))
        if repeat.lower() == 'y':
            continue
        elif repeat.lower() == 'n':
            break
        else:
            raise TypeError('Must enter \'y\' for yes or \'n\' for no, input is not cap-sensitive')

        #
        #
        #
        #
        # Leftover code from lesson, here incase I ever need to come back to it, not important for program.

        # try:
        #     index = str(user_input)
        #     # if len(corpus_tokens) > index > -len(corpus_tokens):
        #     if len(corpus_bigrams) > index > -len(corpus_bigrams):
        #         # print(corpus_tokens[index])
        #         print(f'Head: {corpus_bigrams[index][0]} Tail: {corpus_bigrams[index][1]}')
        #     else:
        #         raise IndexError
        #
        # except IndexError as e:
        #     # print(f'Index Error: Please choose a valid index between -{len(corpus_tokens) +1} and
        #     {len(corpus_tokens) -1}')
        #     print(f'Index Error: Please choose a valid index between -{len(corpus_bigrams) + 1} and
        #     {len(corpus_bigrams) -1}')
        #
        # except ValueError as e:
        #     # print(f'Value Error: {e}: Please enter an integer value between -{len(corpus_tokens) +1} and
        #     {len(corpus_tokens) -1}')
        #     print(f'Value Error: {e}: Please enter an integer value between -{len(corpus_bigrams) + 1} and
        #     {len(corpus_bigrams) -1}')
        #
        # except TypeError as e:
        #     # print(f'Type Error: {e}: Please enter an integer value between -{len(corpus_tokens) +1} and
        #     {len(corpus_tokens) -1}')
        #     print(f'Type Error: {e}: Please enter an integer value between -{len(corpus_bigrams) + 1} and
        #     {len(corpus_bigrams) - 1}')
