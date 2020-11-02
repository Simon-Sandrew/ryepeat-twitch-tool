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

def search_by_channel(first_run, need_reset, page_num, search_clip_channel_response, need_display,user_token, user_timeline):
    if first_run:
        channel_name = input('\nPlease specify name of the channel you\'d like to search\n')
        time_since_created = input('\nPlease specify the amount of hours since the clip was created\n')
        search_for_channel_prefix = 'https://api.twitch.tv/helix/users?login='

        if channel_name is not None and is_num(time_since_created):
            #find the twitch game ID
            search_channel_command = requests.get(search_for_channel_prefix + channel_name, headers={"Authorization": "Bearer " + user_token, "Client-ID": "qbd1ct42tyl8wxzptqixf5m1a77mbv"})
            search_channel_response = search_channel_command.json()
            channel_id = search_channel_response['data'][0]['id']

            #get clips for sbg
            search_clip_by_channel_prefix = 'https://api.twitch.tv/helix/clips?broadcaster_id='
            search_clip_channel_request = requests.get(search_clip_by_channel_prefix + str(channel_id) + '&first=100&started_at=' + str(clip_age.find_clip_age(time_since_created)), headers={"Client-ID": "qbd1ct42tyl8wxzptqixf5m1a77mbv", "Authorization": "Bearer " + user_token})
            search_clip_channel_response = search_clip_channel_request.json()
        else:
            print('\nPlease enter a valid channel name and hour specification\n')
            search_by_channel(True, False, 0, search_clip_channel_response, True, user_token, user_timeline)
    if need_reset:
        global sbc_all_clips

        sbc_clip1 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game' : 'NULL',
            'embed url' : 'NULL'
        }
        sbc_clip2 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game': 'NULL',
            'embed url': 'NULL'
        }
        sbc_clip3 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game': 'NULL',
            'embed url': 'NULL'
        }
        sbc_clip4 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game': 'NULL',
            'embed url': 'NULL'
        }
        sbc_clip5 = {
            'title': 'NULL',
            'view count': 'NULL',
            'url': 'NULL',
            'broadcaster name': 'NULL',
            'game': 'NULL',
            'embed url': 'NULL'
        }

        sbc_all_clips = [sbc_clip1, sbc_clip2, sbc_clip3, sbc_clip4, sbc_clip5]
        clip_number = 0

        while clip_number < 5:
            sbc_all_clips[clip_number]['title'] = search_clip_channel_response['data'][clip_number + page_num]['title']
            sbc_all_clips[clip_number]['view count'] = search_clip_channel_response['data'][clip_number + page_num]['view_count']
            sbc_all_clips[clip_number]['url'] = search_clip_channel_response['data'][clip_number + page_num]['url']
            sbc_all_clips[clip_number]['broadcaster name'] = search_clip_channel_response['data'][clip_number + page_num]['broadcaster_name']

            find_channel_id = requests.get('https://api.twitch.tv/helix/games?id=' + search_clip_channel_response['data'][clip_number + page_num]['game_id'], headers={"Client-ID": "qbd1ct42tyl8wxzptqixf5m1a77mbv", "Authorization": "Bearer " + user_token})
            game_name = find_channel_id.json()
            sbc_all_clips[clip_number]['game'] = game_name['data'][0]['name']

            sbc_all_clips[clip_number]['embed url'] = search_clip_channel_response['data'][clip_number + page_num]['embed_url']

            clip_number += 1
            display_num = 1
        print('Select a clip using number in order to add it to your video:\n')

        #display every time a clip is selected

    if need_display:
        while display_num < 6:
            print('CLIP ' + str(display_num) + ':' +
                '\n Title: ' + sbc_all_clips[display_num-1]['title'] +
                '\n Game: ' + sbc_all_clips[-1]['game'] +
                '\n Broadcaster: ' + sbc_all_clips[display_num-1]['broadcaster name'] +
                '\n Views: ' + str(sbc_all_clips[display_num-1]['view count']) +
                '\n URL : ' + sbc_all_clips[display_num-1]['url']+
                '\n')
            display_num += 1

    selected_movement = input('Type \"next\" to view more clips.'
                              '\nType \"previous\" to see the last 5 clips'
                              '\nType \"menu\" to go to the main search menu\n'
                              '\nType \"timeline\" to view your current timeline\n'
                              '\nType \"render\" to render your current timeline\n')

    if selected_movement.lower() == 'next':
        page_num += 5
        if page_num < 100:
            search_by_channel(False, True, page_num, search_clip_channel_response, True, user_token, user_timeline)
        else:
            print('\nYou have hit the max amount of clips you can view')
    elif selected_movement.lower() == 'previous':
        if page_num != 0:
            page_num -= 5
            search_by_channel(False, True, page_num, search_clip_channel_response, True, user_token, user_timeline)
        else:
            print('\nYou are at the beginning of the list')
            search_by_channel(False, False, 0, search_clip_channel_response, False, user_token, user_timeline)
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
            search_by_channel(False, False, 0, search_clip_channel_response, False, user_token, user_timeline)
        else:
            print('\nThere are no clips in your timeline')
            search_by_channel(False, False, 0, search_clip_channel_response, False, user_token, user_timeline)
    elif selected_movement.lower() == 'menu':
        menu.menu(user_timeline)
    elif selected_movement.lower() == 'render':
        render.render(user_timeline)
    elif selected_movement.lower() == '1' or '2' or '3' or '4' or '5':
        user_timeline.append(sbc_all_clips[int(selected_movement)-1])
        print('\nClip ' + selected_movement + ' has been added to your timeline')

        search_by_channel(False, False, 0, search_clip_channel_response, False, user_token, user_timeline)
    else:
        print('\nPlease use a valid command')
        search_by_channel(False, False, 0, search_clip_channel_response, False, user_token, user_timeline)





