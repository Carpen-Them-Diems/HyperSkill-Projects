import sys
import random
import time
import json
import datetime
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log_format = '%(asctime)s | %(levelname)s: %(message)s'
handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(handler)


class TbosTerminators:
    def __init__(self):
        self.stop_explore = False
        self.title = '''\nx_=========================================================================================================================================_x
   ████████╗░░░░░░██████╗░░█████╗░██╗░██████╗ ████████╗███████╗██████╗░███╗░░░███╗██╗███╗░░██╗░█████╗░████████╗░█████╗░██████╗░██╗░██████╗
   ╚══██╔══╝░░░░░░██╔══██╗██╔══██╗╚█║██╔════╝ ╚══██╔══╝██╔════╝██╔══██╗████╗░████║██║████╗░██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗╚█║██╔════
   ░░░██║░░░█████╗██████╦╝██║░░██║░╚╝╚█████╗░ ░░░██║░░░█████╗░░██████╔╝██╔████╔██║██║██╔██╗██║███████║░░░██║░░░██║░░██║██████╔╝░╚╝╚█████╗░
   ░░░██║░░░╚════╝██╔══██╗██║░░██║░░░░╚═══██╗ ░░░██║░░░██╔══╝░░██╔══██╗██║╚██╔╝██║██║██║╚████║██╔══██║░░░██║░░░██║░░██║██╔══██╗░░░░╚═══██╗
   ░░░██║░░░░░░░░░██████╦╝╚█████╔╝░░░██████╔╝ ░░░██║░░░███████╗██║░░██║██║░╚═╝░██║██║██║░╚███║██║░░██║░░░██║░░░╚█████╔╝██║░░██║░░░██████╔╝
   ░░░╚═╝░░░░░░░░░╚═════╝░░╚════╝░░░░╚═════╝░ ░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝░░░╚═════╝░
x_=========================================================================================================================================_x'''
        self.unavailable = {'feature': 'Feature unavailable at this time, update will be coming in the near future!',
                            'scores': 'No scores to display, play a game and set the first!'}
        self.menu_items = {'play': '[Play]', 'new': '[New] Game', 'load': '[Load] Game', 'back': '[Back] to game',
                           'high': '[High] scores',
                           'main': 'Return to [Main] Menu', 'save': '[Save] and exit', 'help': '[Help]',
                           'exit': '[Exit]'}
        self.menu_main = f'\n{self.menu_items["new"]}\n{self.menu_items["load"]}\n{self.menu_items["high"]}\n{self.menu_items["help"]}\n{self.menu_items["exit"]}\n'
        self.menu_game = f'''
        |==========================|
        |           MENU           |
        |                          |
        | {self.menu_items['back']}           |
        | {self.menu_items['main']}    |
        | {self.menu_items['save']}          |
        | {self.menu_items['exit']}                   |
        |==========================|'''
        self.bot_count = 3
        self.bots = {}
        self.player_name = None
        self.high_scores = {}
        self.save_slots = {'1': 'empty', '2': 'empty', '3': 'empty'}
        self.slot = '0'
        self.locations = []
        self.explored_locations = []
        self.unexplored_locations = []
        self.player_titanium = 0
        self.titanium_scan = False
        self.enemy_scan = False

        if len(sys.argv) >= 3:
            self.seed = sys.argv[1]
            self.min_duration = int(sys.argv[2])
            self.max_duration = int(sys.argv[3])
            self.location_names = sys.argv[4].replace(' ', '_').split(',')

        else:
            self.seed = 'default'
            self.min_duration = 0
            self.max_duration = 0
            self.location_names = ['Beach', 'Cave', 'Apple_Store', 'Walmart', 'Is_that_a_spaceship?', 'Random_Uber',
                                   'WWE_Octagon', 'Strange_House', 'Apple_Bee\'s']

        self.animation_time = random.randint(self.min_duration, self.max_duration)
        random.seed(self.seed)

    def start_(self):
        self.menu_()

    def restart_(self):
        self.start_()

    def save_(self, exit_on_save='no'):
        if os.path.isfile("saved_slots.json"):
            with open('saved_slots.json', 'r+') as f:
                slot_info = json.load(f)
            self.save_slots['1'] = slot_info['1']
            self.save_slots['2'] = slot_info['2']
            self.save_slots['3'] = slot_info['3']

        game_state = {'player_name': self.player_name,
                      'player_titanium': self.player_titanium,
                      'player_robots': self.bot_count,
                      'titanium_scanner': self.titanium_scan,
                      'enemy_scanner': self.enemy_scan
                      }
        while True:
            print("    Select save slot:")
            for num, status in self.save_slots.items():
                print(f"     [{num}] {status}")

            slot = input("\nYour command:\n> ")
            if slot.lower() == 'back':
                break

            elif slot in self.save_slots.keys():
                save_file = f"save_file_{slot}.json"

                with open(save_file, "w+") as f:
                    json.dump(game_state, f)

                self.save_slots[slot] = f'{self.player_name} Titanium: {self.player_titanium} Robots: {self.bot_count} ' \
                                        f'Last save: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} ' \
                                        f'Upgrades: {"location_info" if self.titanium_scan is True else ""}' \
                                        f'{"enemy_info" if self.enemy_scan is True else ""}'
                slot_info = {
                            '1': self.save_slots['1'],
                            '2': self.save_slots['2'],
                            '3': self.save_slots['3']
                            }
                with open('saved_slots.json', 'w') as f:
                    json.dump(slot_info, f)

                # HighScores.save_score_('no')

                print('                        |==============================|\n'
                      '                        |    GAME SAVED SUCCESSFULLY   |\n'
                      '                        |==============================|')

                if exit_on_save.lower() == 'yes':
                    sys.exit(1)
                else:
                    hub.start_hub_()
            else:
                print('invalid save slot')

    def load_(self):
        no_slots = False
        if not os.path.isfile('saved_slots.json'):
            print('There are no saved slots available')
            no_slots = True

        elif os.path.isfile('saved_slots.json'):
            with open('saved_slots.json', 'r') as f:
                slot_info = json.load(f)
            self.save_slots['1'] = slot_info['1']
            self.save_slots['2'] = slot_info['2']
            self.save_slots['3'] = slot_info['3']
            no_slots = False

        print("    Select save slot to load:")
        for slot, status in self.save_slots.items():
            print(f"     [{slot}] {status}")

        if no_slots is False:
            while True:
                try:
                    slot = input('\nYour command:\n> ')
                    if slot.lower() == 'back':
                        break

                    elif self.save_slots[slot] == 'empty':
                        print('This slot is empty!')
                        continue

                    elif slot.lower() not in ['1', '2', '3', 'back']:
                        print('Invalid input')
                        continue

                    with open(f"save_file_{slot}.json", "r") as f:
                        game_state = json.load(f)

                    self.player_name = game_state['player_name']
                    self.player_titanium = game_state['player_titanium']
                    self.bot_count = game_state['player_robots']
                    self.enemy_scan = game_state['enemy_scanner']
                    self.titanium_scan = game_state['titanium_scanner']
                    self.slot = slot

                    print("                        |==============================|\n"
                          "                        |    GAME LOADED SUCCESSFULLY  |\n"
                          "                        |==============================|\n"
                          f"                       Welcome back, commander {self.player_name}!")

                    hub.start_hub_()

                except FileNotFoundError:
                    print("\nNo saved game found!")
                    continue

                except json.JSONDecodeError:
                    print("\nInvalid save file format!")
                    continue

                except Exception as e:
                    print("\nAn error occurred while loading the game:", str(e))
                    continue

    @staticmethod
    def animate_(duration):
        for _ in range(duration):
            print(".", end="", flush=True)
            time.sleep(1)

    def menu_(self):
        while True:
            print(self.title)
            print(self.menu_main)
            command = str(input('Your command:\n '))
            if command.lower() == 'exit':
                print('\nGoodbye and thanks for playing! - T-BO(Carpen-Them-Diemz)')
                sys.exit(0)

            elif command.lower() == 'new':
                self.player_name = str(input('\nEnter your name:\n '))
                self.begin_()

            elif command.lower() == 'load':
                self.load_()

            elif command.lower() == 'high':
                HighScores.load_scores_()

            elif command.lower() == 'help':
                help.menu_()

            else:
                print('Invalid input menu_')

    def begin_(self):
        print(f'\nGreetings, commander {self.player_name}!\nAre you ready to begin?\n[Yes] [No] Return to Main[Menu]\n')
        ready_to_begin = False

        while not ready_to_begin:
            player_command = input('Your command:\n ')
            if player_command.lower() == 'no':
                print('\nHow about now.\nAre you ready to begin?\n[Yes] [No]  Return to Main[Menu]\n')
                continue

            elif player_command.lower() == 'yes':
                ready_to_begin = True
                hub.start_hub_()

            elif player_command.lower() == 'menu':
                self.menu_()

            else:
                print('2.5Invalid input')
                continue

    def explore_(self):
        self.locations = []
        self.unexplored_locations = []
        max_locations = random.randint(1, 9)
        n_locations = len(self.locations)
        self.stop_explore = False

        while n_locations == 0 and self.stop_explore is False:
            if n_locations < max_locations:
                location = Location(random.choice(self.location_names))
                self.locations.append(location)
                self.unexplored_locations.append(location)

                print('\nSearching', end='')
                game.animate_(self.animation_time)
                print()
                if len(self.unexplored_locations) > 0 and n_locations < max_locations:
                    for index, location in enumerate(self.unexplored_locations, start=1):
                        print(f'[{index}] {location.__str__()}')
                    print('\n[S] to continue searching')

                else:
                    for index, location in enumerate(self.unexplored_locations, start=1):
                        print(f'[{index}] {location.__str__()}')
                    print('\nNo more unexplored locations\n       [Back]  [S]')

                while True:
                    try:
                        # print(self.unexplored_locations)
                        if len(self.unexplored_locations) > 0:
                            choice = input("\nYour command:\n")

                            if choice.lower() == 's':
                                # print("\nChoose a location to explore [#]:")
                                if len(self.unexplored_locations) < max_locations:
                                    break
                                else:
                                    for index, location in enumerate(self.unexplored_locations, start=1):
                                        print(f'[{index}] {location.__str__()}')
                                    print('\nNo more locations in sight\n       [Back]')
                                    continue

                            elif choice.lower() == 'back':
                                self.stop_explore = True
                                hub.start_hub_()

                            elif choice.isdigit() and 1 <= int(choice) <= len(self.unexplored_locations):
                                choice = int(choice)
                                location = self.unexplored_locations[choice - 1]
                                if not location.explored:
                                    location.explore_location_()
                                    self.explored_locations.append(location)
                                    self.unexplored_locations.pop(choice - 1)
                                    hub.start_hub_()

                                else:
                                    print(f"{location.__str__()} has already been explored.")
                                    if location.name in self.unexplored_locations:
                                        del self.unexplored_locations[location.name]
                                    print('Choose a new location', end='')
                                    game.animate_(self.animation_time)
                                    continue
                            else:
                                print('Invalid input')
                                for index, location in enumerate(self.unexplored_locations, start=1):
                                    print(f'[{index}] {location.__str__()}')
                                continue
                        else:
                            print('No more locations nearby\n  [Back]  [S]')
                            for index, location in enumerate(self.unexplored_locations, start=1):
                                print(f'[{index}] {location.__str__()}')
                            continue

                    except StopIteration:
                        if len(self.unexplored_locations) == 0:
                            print('\nNo more locations in sight.\n       [Back]\n')
                            continue
                        else:
                            for index, location in enumerate(self.unexplored_locations, start=1):
                                print(f'[{index}] {location.__str__()}')
                            print('\nNo more unexplored locations\n       [Back]  [S]')

                    # except ValueError as e:
                    #     print("Invalid input. Please enter a valid location number.", e)
                    #     continue

                    # except IndexError:
                    #     print("\nInvalid input. Please enter a valid location number.\n")
                    #     for index, location in enumerate(self.unexplored_locations, start=1):
                    #         print(f'{index} {location.__str__()}')
                    #     print('\n[S] to continue searching')
                    #     continue
            else:
                print('No more locations in sight')


class Hub:
    def __init__(self):
        self.hub_template =  '+==============================================================================+\n' \
                             '{head1}{head}\n' \
                             '{shoulder1}{shoulder}\n' \
                             '{body1}{body}\n' \
                             '{waist1}{waist}\n' \
                             '{feet1}{feet}\n' \
                             '+==============================================================================+\n' \
                             '| Titanium: {titanium:04}                                                               |\n' \
                             '+==============================================================================+\n' \
                             '|                  [Ex]plore                          [Up]grade                |\n' \
                             '|                  [Save]                             [M]enu                   |\n' \
                             '+==============================================================================+'

        self.store_menu = '\n     |================================|\n' \
                          '     |          UPGRADE STORE         |\n' \
                          '     |                         Price  |\n' \
                          '     | [1] Titanium Scan         250  |\n' \
                          '     | [2] Enemy Encounter Scan  500  |\n' \
                          '     | [3] New Robot            1000  |\n' \
                          '     |                                |\n' \
                          '     | [Back]                         |\n' \
                          '     |================================|'

    def hub_menu(self):
        head = '|  $   $$$$$$$   $  ' * (game.bot_count - 1)
        shoulder = '|  $$$$$     $$$$$  ' * (game.bot_count - 1)
        body = '|      $$$$$$$      ' * (game.bot_count - 1)
        waist = '|     $$$   $$$     ' * (game.bot_count - 1)
        feet = '|     $       $     ' * (game.bot_count - 1)

        head1 = '  $   $$$$$$$   $  '
        shoulder1 = '  $$$$$     $$$$$  '
        body1 = '      $$$$$$$      '
        waist1 = '     $$$   $$$     '
        feet1 = '     $       $     '

        return self.hub_template.format(titanium=game.player_titanium, head1=head1, shoulder1=shoulder1,
                                        body1=body1, waist1=waist1, feet1=feet1, head=head, shoulder=shoulder,
                                        body=body, waist=waist, feet=feet)

    def hub_store(self):
        print(self.store_menu + '\n')
        while True:
            command = input('Enter your command:\n> ')
            if command.lower() == 'back':
                hub.start_hub_()
                break
            elif command == '1' and game.player_titanium >= 250:
                game.player_titanium -= 250
                game.titanium_scan = True
                # print(f'{game.player_name} Successfully bought: Titanium Scanner! Titanium: -250 = {game.player_titanium}')
                print('\nPurchase successful. You can now see how much titanium you can get from each found location.')
                hub.start_hub_()
            elif command == '2' and game.player_titanium >= 500:
                game.player_titanium -= 500
                game.enemy_scan = True
                # print(f'{game.player_name} Successfully bought: Enemy Scanner! Titanium: -500 = {game.player_titanium}')
                print('\nPurchase successful. You will now see how likely you will encounter an enemy at each found location.')
                hub.start_hub_()
            elif command == '3' and game.player_titanium > 1000:
                # if game.bot_count < 4:
                game.player_titanium -= 1000
                game.bot_count += 1
                # print(f'{game.player_name} Successfully bought: New Robot! Titanium: -1000 = {game.player_titanium}')
                print('\nPurchase successful. You now have an additional robot')
                hub.start_hub_()
                # else:
                #     print('You can only have 4 bots at a time!')
                #     continue
            elif command not in ['1', '2', '3', 'back']:
                print('Invalid input')
                continue
            else:
                print(f'Not enough titanium!')  # for item: {game.player_titanium}')
                continue

    def start_hub_(self):
        while True:
            print(self.hub_menu())
            choice = str(input('\nYour command:\n'))
            if choice.lower() == 'm':
                while True:
                    print(game.menu_game, '\n')
                    choice = str(input('Your command:\n'))

                    if choice.lower() == 'back':
                        break

                    elif choice.lower() == 'main':
                        game.start_()

                    elif choice.lower() == 'save':
                        game.save_('yes')
                        sys.exit(1)

                    elif choice.lower() == 'exit':
                        print('\nGoodbye and thanks for playing! - T-BO(Carpen-Them-Diemz)')
                        sys.exit(0)

                    else:
                        print('\nInvalid input\n')

            elif choice.lower() == 'ex':
                game.explore_()
                return

            elif choice.lower() == 'up':
                self.hub_store()
                return

            elif choice.lower() == 'save':
                game.save_()

            elif choice.lower() == 'back':
                hub.start_hub_()

            else:
                print('\nInvalid input\n')
                continue


class Location:
    def __init__(self, name):
        self.name = name
        self.titanium = random.randint(10, 100)
        self.game_over = '              |==============================|\n' \
                         '              |          GAME OVER!          |\n' \
                         '              |==============================|\n'
        self.encounter_rate = random.random()
        self.explored = False

    def explore_location_(self):
        user_encounter = random.random()
        if user_encounter > self.encounter_rate:
            self.location_explored()
            self.explored = True
            game.player_titanium += self.titanium
        elif user_encounter < self.encounter_rate:
            game.bot_count -= 1
            if game.bot_count > 0:
                print('Deploying robots!', end='')
                game.animate_(game.animation_time)
                print('Enemy encounter!', end='')
                game.animate_(game.animation_time)
                print(f"\n{self.name} explored successfully, 1 robot lost..")
                print(f"Acquired {self.titanium} lumps of titanium")
                game.player_titanium += self.titanium

            else:
                if game.bot_count < 1:
                    print('\nDeploying robots!', end='')
                    game.animate_(game.animation_time)
                    print('\nEnemy encounter!!!', end='')
                    game.animate_(game.animation_time)
                    print(f'\nMission aborted, the last robot lost...\n{self.game_over}')
                    HighScores.save_score_('no')
                    game.start_()
                    return
                    # print('Game over: Looks like all your bots have been destroyed!\nWould you like to save your score? [Yes/No]')
                    # while True:
                    #     command = input('Your command:\n> ')
                    #     if command.lower() == 'yes':
                    #         HighScores.save_score_('yes')
                    #         sys.exit(1)
                    #     elif command.lower() == 'no':
                    #         sys.exit(0)
                    #     else:
                    #         print('Invalid input, [Yes] to save score, [No] to continue to main screen')
                    #         continue

    def location_explored(self):
        print("\nTraveling to new location!", end='')
        game.animate_(game.animation_time)
        print(f'\nDeploying Robots!', end='')
        game.animate_(game.animation_time)
        print(f"\n{self.name} explored successfully, with no enemies encountered and damage taken.")
        print(f"Acquired {self.titanium} lumps of titanium")

    def __str__(self):
        if game.titanium_scan and game.enemy_scan is True:
            return f'{self.name}: Titanium: {self.titanium}: Encounter rate: {round(self.encounter_rate * 100)}%'
        elif game.titanium_scan is True:
            return f'{self.name}: Titanium: {self.titanium}'
        elif game.enemy_scan is True:
            return f'{self.name}: Encounter rate: {round(self.encounter_rate* 100)}%'
        else:
            return f'{self.name}'

    def __repr__(self):
        return f"Location(name={self.name}, titanium={self.titanium}, encounter_rate={self.encounter_rate}, explored={self.explored})"


class HighScores:
    def __init__(self):
        self.high_score_max = 10
        self.high_score_save_success = '          |==================================|\n' \
                                       '          |   HIGH-SCORE SAVED SUCCESSFULLY  |\n' \
                                       '          |==================================|'

    @staticmethod
    def load_scores_():
        while True:
            if os.path.isfile('high_scores.json'):
                with open('high_scores.json', 'r+') as f:
                    high_scores = json.load(f)
                print('\n    HIGH SCORES\n')
                for index, score in high_scores.items():
                    print(f"({index}) {score['name']} {score['score']}")
                print('\n     [Back]')

            else:
                print('No high scores or high score file is corrupted/damaged\n        [Back]')

            command = input('Enter command:\n> ')
            if command.lower() == 'back':
                break
            else:
                print('Invalid input')

            # if os.path.isfile('high_scores.json'):
            #     with open('high_scores.json', 'r') as f:
            #         high_scores = json.load(f)
            #     print('\n      HIGH SCORES\n')
            #     for index, (name, score) in enumerate(high_scores.items(), start=1):
            #         score = f'({index}) {score["name"]} {score["score"]}'
            #         print(score)
            #     print('\n     [Back]')
            # else:
            #     print('No high scores or high score file is corrupted/damaged\n        [Back]')
            # command = input('Enter command:\n> ')
            # if command.lower() == 'back':
            #     break
            # else:
            #     print('Invalid input')

    @staticmethod
    def save_score_(ext='no'):
        high_score_saved = False
        if not os.path.isfile('high_scores.json') and not os.path.isfile('duskers/high_scores.json'):
            data = {'1': {'name': f'{game.player_name}', 'score': f'{game.player_titanium}'}}
            with open('high_scores.json', 'w+') as f:
                json.dump(data, f)
            print('                                                           \n'
                  '                      |==================================|\n'
                  '                      |   HIGH-SCORE SAVED SUCCESSFULLY  |\n'
                  '                      |==================================|')
            if ext.lower() == 'yes':
                sys.exit(1)

        elif os.path.isfile('high_scores.json') or os.path.isfile('duskers/high_scores.json'):
            if os.path.isfile('high_scores.json'):
                file_name = 'high_scores.json'
            elif os.path.isfile('duskers/high_scores.json'):
                file_name = 'duskers/high_scores.json'
            with open(file_name, 'r+') as f:
                high_scores = json.load(f)
                player_score = {'name': f'{game.player_name}', 'score': f'{game.player_titanium}'}
                for index, score in high_scores.items():
                    if game.player_titanium > int(score['score']) and len(high_scores) <= 10:
                        for i in reversed(range(1, len(high_scores) + 1)):
                            if i >= int(index):
                                high_scores[str((i + 1))] = high_scores[str(i)]
                        high_scores[index] = player_score
                        if len(high_scores) > 10:
                            high_scores = dict(list(high_scores.items())[:10])
                        high_score_saved = True
                        break

                    elif int(index) == len(high_scores) and len(high_scores) < 10:
                        high_scores[str((len(high_scores) + 1))] = player_score
                        high_score_saved = True
                        break

                    elif len(high_scores) > 10:
                        print('Error: Too many high scores in high_score.json')

                f.seek(0)
                json.dump(high_scores, f)

            if high_score_saved is True:
                print('                                                          \n'
                      '                      |==================================|\n'
                      '                      |   HIGH-SCORE SAVED SUCCESSFULLY  |\n'
                      '                      |==================================|')

                if ext.lower() == 'yes':
                    sys.exit(1)

            elif high_score_saved is False:
                print(f'Your score: {game.player_titanium} does not meet the requirements for high score, '
                      f'keep on trying!')

                if ext.lower() == 'yes':
                    sys.exit(1)

        # new_high_score = False
        # if os.path.isfile('high_scores.json'):
        #     with open('high_scores.json', 'r+') as f:
        #         high_scores = json.load(f)
        #         count = 0
        #         for index, score in high_scores.items():
        #             # print(score)
        #             if game.player_titanium > int(score['score']):
        #                 count = int(index)
        #
        #                 high_scores[index] = {'name': f'{game.player_name}', 'score': f'{game.player_titanium}'}
        #                 new_high_score = True
        #
        #             elif count == len(high_scores) and count < 10:
        #                 index = str(int(index) + 1)
        #                 high_scores[index] = {'name': f'{game.player_name}', 'score': f'{game.player_titanium}'}
        #                 new_high_score = True
        #
        #         if new_high_score is False:
        #             print(f'Your score: {game.player_titanium} does not meet the requirements for high score '
        #                   f'placement: {high_scores["10"]}, keep on trying!')
        #
        #         elif new_high_score is True:
        #             print('\n                       |==================================|\n'
        #                   '                       |   HIGH-SCORE SAVED SUCCESSFULLY  |\n'
        #                   '                       |==================================|')
        #
        # elif not os.path.isfile('high_scores.json') and not os.path.isfile('duskers/high_scores.json'):
        #     data = {'1': {f'name': f'{game.player_name}', 'score': f'{game.player_titanium}'}}
        #         # , '2': {'name': None, 'score': 0},
        #         #     '3': {'name': None, 'score': 0}, '4': {'name': None, 'score': 0},
        #         #     '5': {'name': None, 'score': 0}, '6': {'name': None, 'score': 0},
        #         #     '7': {'name': None, 'score': 0}, '8': {'name': None, 'score': 0},
        #         #     '9': {'name': None, 'score': 0}, '10': {'name': None, 'score': 0}}
        #
        #     with open('high_scores.json', 'w+') as f:
        #         json.dump(data, f)
        #
        #     print('\n                       |==================================|\n'
        #           '                       |   HIGH-SCORE SAVED SUCCESSFULLY  |\n'
        #           '                       |==================================|')
        #
        #     if exit.lower() == 'yes':
        #         sys.exit(1)


class Help:
    def __init__(self):
        self.menu = '''\nWelcome to TBO'S Terminators, this is a search and explore game where the goal is to collect as 
much titanium as possible to land yourself on the top 10 leaderboard. You gain titanium by exploring 
locations, but be careful because you only start with 3 robots and there is a chance at an enemy encounter 
at every stop. With the titanium you collect you can also buy upgrades for your robot and buy new robots 
to replace your lost ones with your titanium. If you run out of all robots that\'s game over! 

The instructions for available commands will be visible at each step of the game but you can always type
back to go back. Here are a few of the commands that can be used through the game to get you started:
(Commands are not cse sensitive)
            
[New] = Start a new game
[Load] = load a previously saved game
[High] = See the highscores list
[Help] = Bring you to this help screen
[Exit] = Exit the game
[Yes] = Yes, self explanatory I think!
[No] = Some people say yes means no, but that's weird here it just means no
[Back] = Go back to previous step
[1] - [10] = Choose one of the provided actions
[Menu] = Go to the main menu
[Ex] = Explore, begin exploring locations location
[S] = Look for the next location
[Up] = Go to the upgrade shop\n'''

    def menu_(self):
        while True:
            print(self.menu)
            command = input('Command here:\n> ')
            if command.lower() == 'back':
                break

            else:
                print('Invalid input, enter "Back" to go back to main menu')
                continue


game = TbosTerminators()
help = Help()
hub = Hub()
game.start_()
