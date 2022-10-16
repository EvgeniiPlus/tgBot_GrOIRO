import os
from pathlib import Path


# token = os.getenv('TOKEN')
# channel_id = os.getenv('CHANNEL_ID')
# token_weather = os.getenv('TOKEN_WEATHER')

token ='5630957891:AAHRBSnmwrNU9pWc0inki92Pf0Kqkswym2s'
channel_id = '842095003'
token_weather = 'f73b75a22912e6df0b7e5e2e907ce6fb'
admin_id = '842095003'


headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}
url = "https://groiro.by"

# ttable_url = 'D:\Projects\PycharmProjects\pars\Timetable'
ttable_url = Path(__file__).parent / 'Timetable'
