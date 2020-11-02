import requests
import json
import clip_age
import render
import menu

def is_num(test_in):
    try:
        int(test_in)
        return True
    except ValueError:
        return False

def search_by_game(first_run, need_reset, page_num, search_clip_game_response, need_display,user_token, user_timeline):
    if first_run:
        game_name = input('\nPlease specify name of the game you\'d like to search\n')
        time_since_created = input('\nPlease specify the amount of hours since the clip was created\n')
        search_for_game_prefix = 'https://api.twitch.tv/helix/games?name='

        if game_name is not None and is_num(time_since_created):
            #find the twitch game ID
            search_game_command = requests.get(search_for_game_prefix + game_name, headers={"Authorization": "Bearer " + user_token, "Client-ID": "qbd1ct42tyl8wxzptqixf5m1a77mbv"})
            search_game_response = search_game_command.json()
            game_id = search_game_response['data'][0]['id']

            #get clips for sbg
            search_clip_by_game_prefix = 'https://api.twitch.tv/helix/clips?game_id='
            search_clip_game_request = requests.get(search_clip_by_game_prefix + str(game_id) + '&first=100&started_at=' + str(clip_age.find_clip_age(time_since_created)), headers={"Client-ID": "qbd1ct42tyl8wxzptqixf5m1a77mbv", "Authorization": "Bearer " + user_token})
            search_clip_game_response = search_clip_game_request.json()
        else:
            print('\nPlease enter a valid game name and hour specification\n')
            search_by_channel(True, False, 0, search_clip_game_response, True, user_token, user_timeline)
    if need_reset:
        global sbg_all_clips

        sbg_clip1 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game' : 'NULL',
            'embed url' : 'NULL'
        }
        sbg_clip2 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game': 'NULL',
            'embed url': 'NULL'
        }
        sbg_clip3 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game': 'NULL',
            'embed url': 'NULL'
        }
        sbg_clip4 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game': 'NULL',
            'embed url': 'NULL'
        }
        sbg_clip5 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game': 'NULL',
            'embed url': 'NULL'
        }

        sbg_all_clips = [sbg_clip1, sbg_clip2, sbg_clip3, sbg_clip4, sbg_clip5]
        clip_number = 0

        while clip_number < 5:
            print(clip_number)
            sbg_all_clips[clip_number]['title'] = search_clip_game_response['data'][clip_number + page_num]['title']
            sbg_all_clips[clip_number]['view count'] = search_clip_game_response['data'][clip_number + page_num]['view_count']
            sbg_all_clips[clip_number]['url'] = search_clip_game_response['data'][clip_number + page_num]['url']
            sbg_all_clips[clip_number]['broadcaster name'] = search_clip_game_response['data'][clip_number + page_num]['broadcaster_name']

            find_game_id = requests.get('https://api.twitch.tv/helix/games?id=' + search_clip_game_response['data'][clip_number + page_num]['game_id'], headers={"Client-ID": "qbd1ct42tyl8wxzptqixf5m1a77mbv", "Authorization": "Bearer " + user_token})
            game_name = find_game_id.json()
            sbg_all_clips[clip_number]['game'] = game_name['data'][0]['name']

            sbg_all_clips[clip_number]['embed url'] = search_clip_game_response['data'][clip_number + page_num]['embed_url']

            clip_number += 1
            display_num = 1


        #display every time a clip is selected

    if need_display:
        while display_num < 6:
            print('CLIP ' + str(display_num) + ':' +
                '\n Title: ' + sbg_all_clips[display_num-1]['title'] +
                '\n Game: ' + sbg_all_clips[-1]['game'] +
                '\n Broadcaster: ' + sbg_all_clips[display_num-1]['broadcaster name'] +
                '\n Views: ' + str(sbg_all_clips[display_num-1]['view count']) +
                '\n URL : ' + sbg_all_clips[display_num-1]['url']+
                '\n')
            display_num += 1

    print('Select a clip using number in order to add it to your video:\n')
    selected_movement = input('Type \"next\" to view more clips.'
                              '\nType \"previous\" to see the last 5 clips'
                              '\nType \"menu\" to go to the main search menu\n'
                              '\nType \"timeline\" to view your current timeline\n'
                              '\nType \"render\" to render your current timeline\n')

    if selected_movement.lower() == 'next':
        page_num += 5
        if page_num < 100:
            search_by_game(False, True, page_num, search_clip_game_response, True, user_token, user_timeline)
        else:
            print('\nYou have hit the max amount of clips you can view')
    elif selected_movement.lower() == 'previous':
        if page_num != 0:
            page_num -= 5
            search_by_game(False, True, page_num, search_clip_game_response, True, user_token, user_timeline)
        else:
            print('\nYou are at the beginning of the list')
            search_by_game(False, False, 0, search_clip_game_response, False, user_token, user_timeline)
    elif selected_movement.lower() == 'timeline':
        print(user_timeline)
        if user_timeline is not None:
            timeline_number = 0
            while timeline_number < len(user_timeline):
                print('CLIP ' + str(timeline_number + 1) + ':' +
                    '\n Title: ' + user_timeline[timeline_number]['title'] +
                    '\n Game: ' + user_timeline[timeline_number]['game'] +
                    '\n Broadcaster: ' + user_timeline[timeline_number]['broadcaster name'] +
                    '\n Views: ' + str(user_timeline[timeline_number]['view count']) +
                    '\n URL : ' + user_timeline[timeline_number]['url'] + '\n')
                timeline_number += 1
            search_by_game(False, False, 0, search_clip_game_response, False, user_token, user_timeline)
        else:
            print('\nThere are no clips in your timeline')
            search_by_game(False, False, 0, search_clip_game_response, False, user_token, user_timeline)
    elif selected_movement.lower() == 'menu':
        menu.menu(user_timeline)
    elif selected_movement.lower() == 'render':
        render.render(user_timeline)
    elif selected_movement.lower() == '1' or '2' or '3' or '4' or '5':
        user_timeline.append(sbg_all_clips[int(selected_movement)-1])
        print('\nClip ' + selected_movement + ' has been added to your timeline')

        search_by_game(False, False, 0, search_clip_game_response, False, user_token, user_timeline)
    else:
        print('\nPlease use a valid command')
        search_by_game(False, False, 0, search_clip_game_response, False, user_token, user_timeline)