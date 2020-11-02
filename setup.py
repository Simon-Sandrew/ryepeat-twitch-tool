import webbrowser
user_token = ''

def setup():
    global user_token
    print('Welcome to Ryepeat. ')
    print('\nDue to Ryepeat being in early access, this setup is a bit janky. I apologize. This will be changed upon '
          'release of the finished version. If the text instructions are confusing, please watch the youtube video '
          'provided here: ')
    webbrowser.open('https://id.twitch.tv/oauth2/authorize?client_id=qbd1ct42tyl8wxzptqixf5m1a77mbv&redirect_uri=http://localhost&response_type=token&scope=clips:edit')

    user_token = input('\nPlease copy and paste your token and press enter: ')
    write_token = open("info.txt", "w+")
    write_token.write(str(user_token))
    write_token.close()