import keyboard
import pyperclip
import json
import re
from typing import Optional, List, Dict, Any
from uuid import uuid4
from fake_useragent import UserAgent
from pydantic import BaseModel
from tls_client import Session

#-------------------------------------Edit Here-------------------------------------
#professional
USER_PROMPT1 = "help me rephrase the following text in a professional manner, and keep the text length about the same as the original text. also your answer should only consist of the rephrased text, without an introduction : "
KEYBOARD_SHORTCUT1 = 'ctrl+alt+p'

#concise
USER_PROMPT2 = "help me rephrase the following text in the most concise and shortest way possible without damaging the message of the content. also your answer should only consist of the rephrased text, without an introduction : "
KEYBOARD_SHORTCUT2 = 'ctrl+alt+c'

#grammer
USER_PROMPT3 = "help me rephrase the following text, but only fix grammer and spelling mistakes. also your answer should only consist of the rephrased text, without an introduction : "
KEYBOARD_SHORTCUT3 = 'ctrl+alt+g'

#translate
USER_PROMPT4 = "translate the following text into English. also your answer should only consist of the rephrased text, without an introduction : "
KEYBOARD_SHORTCUT4 = 'ctrl+alt+t'
#-----------------------------------------------------------------------------------

class PoeResponse(BaseModel):
    text: Optional[str] = None
    links: List[str] = []
    extra: Dict[str, Any] = {}


class Completion:
    @staticmethod
    def create(
        prompt: str,
        page: int = 1,
        count: int = 10,
        safe_search: str = 'Moderate',
        on_shopping_page: bool = False,
        mkt: str = '',
        response_filter: str = 'WebPages,Translations,TimeZone,Computation,RelatedSearches',
        domain: str = 'youchat',
        query_trace_id: str = None,
        chat: list = None,
        include_links: bool = False,
        detailed: bool = False,
        debug: bool = False,
        proxy: Optional[str] = None,
    ) -> PoeResponse:
        if chat is None:
            chat = []

        proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy} if proxy else {}

        client = Session(client_identifier='chrome_108')
        client.headers = Completion.__get_headers()
        client.proxies = proxies

        response = client.get(
            f'https://you.com/api/streamingSearch',
            params={
                'q': prompt,
                'page': page,
                'count': count,
                'safeSearch': safe_search,
                'onShoppingPage': on_shopping_page,
                'mkt': mkt,
                'responseFilter': response_filter,
                'domain': domain,
                'queryTraceId': str(uuid4()) if query_trace_id is None else query_trace_id,
                'chat': str(chat),  # {'question':'','answer':' ''}
            },
        )

        if debug:
            print('\n\n------------------\n\n')
            print(response.text)
            print('\n\n------------------\n\n')

        if 'youChatToken' not in response.text:
            return Completion.__get_failure_response()

        you_chat_serp_results = re.search(
            r'(?<=event: youChatSerpResults\ndata:)(.*\n)*?(?=event: )', response.text
        ).group()
        third_party_search_results = re.search(
            r'(?<=event: thirdPartySearchResults\ndata:)(.*\n)*?(?=event: )', response.text
        ).group()
        # slots                   = findall(r"slots\ndata: (.*)\n\nevent", response.text)[0]

        text = ''.join(re.findall(r'{\"youChatToken\": \"(.*?)\"}', response.text))

        extra = {
            'youChatSerpResults': json.loads(you_chat_serp_results),
            # 'slots'                   : loads(slots)
        }

        response = PoeResponse(text=text.replace('\\n', '\n').replace('\\\\', '\\').replace('\\"', '"'))
        if include_links:
            response.links = json.loads(third_party_search_results)['search']['third_party_search_results']

        if detailed:
            response.extra = extra

        return response

    @staticmethod
    def __get_headers() -> dict:
        return {
            'authority': 'you.com',
            'accept': 'text/event-stream',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'referer': 'https://you.com/search?q=who+are+you&tbm=youchat',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'cookie': f'safesearch_guest=Moderate; uuid_guest={str(uuid4())}',
            'user-agent': UserAgent().random,
        }

    @staticmethod
    def __get_failure_response() -> PoeResponse:
        return PoeResponse(text='Unable to fetch the response, Please try again.')


# chatbot
def you_chatbot(input_text = " ", user_prompt = USER_PROMPT1):
    prompt = user_prompt + input_text
    response = Completion.create(prompt=prompt, 
                                     # detailed=True
                                     )
    return response.text

# set hotkey
def hotkey_pressed_rephrase():
    copied_text = pyperclip.paste() 
    response = you_chatbot(copied_text)
    pyperclip.copy(response)
    print(response) 

def hotkey_pressed_concise():
    copied_text = pyperclip.paste() 
    response = you_chatbot(copied_text, USER_PROMPT2)
    pyperclip.copy(response)
    print(response) 


def hotkey_pressed_grammer():
    copied_text = pyperclip.paste() 
    response = you_chatbot(copied_text, USER_PROMPT3)
    pyperclip.copy(response)
    print(response) 

    
def hotkey_pressed_translate():
    copied_text = pyperclip.paste() 
    response = you_chatbot(copied_text, USER_PROMPT4)
    pyperclip.copy(response)
    print(response) 

# register the hotkey using the keyboard library
keyboard.add_hotkey(KEYBOARD_SHORTCUT1, hotkey_pressed_rephrase)
keyboard.add_hotkey(KEYBOARD_SHORTCUT2, hotkey_pressed_concise)
keyboard.add_hotkey(KEYBOARD_SHORTCUT3, hotkey_pressed_grammer)
keyboard.add_hotkey(KEYBOARD_SHORTCUT4, hotkey_pressed_translate)
# wait for keyboard events
keyboard.wait()

