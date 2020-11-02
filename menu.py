import os
import sbg
import sbc
import setup


main_timeline = []
def menu(user_timeline):
    global user_token
    global main_timeline
    main_timeline = user_timeline
    startup = open("info.txt", "r+")
    token = startup.readlines()
    token_size = os.path.getsize("info.txt")
    if token_size == 0:
        setup.setup()
        user_token = token[0]
        startup.close()
    else:
        print('Welcome back to ryepeat.\n\n\n')
        user_token = token[0]

    selected_search_search_mode = input('How would you like to search?'
                                               '\n     1) Search by game'
                                               '\n     2) Search by channel'
                                               '\n'
                                               '\nType a number to select that option\n')
    if selected_search_search_mode == '1' or '2':
        search(int(selected_search_search_mode))
    else:
        print('\nType a valid numerical option.')


def search(search_method):
    if search_method == 1:
        sbg.search_by_game(True, True, 0, None, True, user_token, main_timeline)
    if search_method == 2:
        sbc.search_by_channel(True, True, 0, None, True, user_token, main_timeline)
