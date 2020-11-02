import subprocess
import os

def render(user_timeline):
    user_confirm = input('\nRyepeat will output this file in whatever directory it is installed in. It will be titled "finishedvideo.mp4" Are you sure you would like to continue? '
                         '\n     1) Yes'
                         '\n     2) No\n')



    if user_confirm == '2':
        search_by_game(False, False, 0, search_clip_game_response, False)


    if user_confirm == '1':


        print('\n Beginning download')

        dlnumber = 1
        filenames = open('filenames.txt', 'a')
        #Actual rendering of the clips
        while dlnumber <= len(user_timeline):
            subprocess.call(r'youtube-dl.exe ' + user_timeline[dlnumber-1]['url'] + ' -o' + str(os.getcwd()) + r'\u'+ str(dlnumber) + '.%(ext)s')
            subprocess.call('ffmpeg -i ' + str(os.getcwd()) + r'\u' + str(dlnumber) + '.mp4' + ' -r 60 -vf scale=1920:1080 -ar 44100 ' + str(os.getcwd())+ r'\f' + str(dlnumber) +'.mp4')

            filenames.write('file \'f' + str(dlnumber)+'.mp4\'\n')
            os.remove(str(os.getcwd()) + r'\u' + str(dlnumber) + '.mp4')

            dlnumber +=1
        filenames.close()

        subprocess.call(r'ffmpeg -f concat -i filenames.txt -c copy finishedvideo.mp4')
        dlnumber = 1
        while dlnumber <= len(user_timeline):
            os.remove(str(os.getcwd()) + r'\f' + str(dlnumber) + '.mp4')
            dlnumber +=1

        filenames = open('filenames.txt', 'w')
        filenames.write('')
        filenames.close()

        print('Finished Render')

    else:
        print('Please type a valid number.')

