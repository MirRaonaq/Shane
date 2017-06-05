import random
import string
from flask import Flask, request, url_for, render_template, send_from_directory
from model import *
from api import APICall
import ai
import urllib2
import json

app = Flask(__name__, static_url_path='')

VERIFICATION_TOKEN = 'this_is_not_a_joke'
PAGE_TOKEN = 'EAAEKsbOLkpoBAMRPjqSZBZC7e2Vxy3ZBZAONuOwXD0IUFgPxmDeZCyV6GO2PtexigduoRp8CAeNAAMDFHWlCKmddGBZBn0HkmOep2wU9YDQrU8T7QY8UyI6EZAZCRZBAGWQrlvyr0E3j26v0DeW3szMhHBCQOI8DmwZBPQ2qVkUwtR6A8GCsLpP34bwjEYiEuQdAMZD'
PAGE_ID = '300443787072913'

fb = APICall(PAGE_TOKEN)

BASE_URL = 'https://655ac952.ngrok.io'


def generate_random():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))


def send_to_recipient(message, user_id):
    link = 'https://graph.facebook.com/v2.6/' + PAGE_ID + '/messages'
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "text": message
        }
    }
    print fb.makeRequestPost(link, data)


def semd_image_to_recipient(url, user_id):
    pass


def send_templates_to_recipient(user_id):
    link = 'https://graph.facebook.com/v2.6/' + PAGE_ID + '/messages'
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Smooth Red",
                            "image_url": BASE_URL+'/img/template-1.png',
                            "subtitle": "Default colors: red, white, black",
                            "default_action": {
                                "type": "web_url",
                                "url": BASE_URL+'/'+user_id+'/select_template/1',
                                "messenger_extensions": True,
                                "webview_height_ratio": "tall",
                                "fallback_url": BASE_URL
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": BASE_URL+'/'+user_id+'/select_template/1',
                                    "title": "Select Template"
                                }
                            ]
                        },
                        {
                            "title": "Sleek Black",
                            "image_url": BASE_URL + '/img/template-2.png',
                            "subtitle": "Default colors: white, black",
                            "default_action": {
                                "type": "web_url",
                                "url": BASE_URL + '/' + user_id + '/select_template/2',
                                "messenger_extensions": True,
                                "webview_height_ratio": "tall",
                                "fallback_url": BASE_URL
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": BASE_URL + '/' + user_id + '/select_template/2',
                                    "title": "Select Template"
                                }
                            ]
                        },
                        {
                            "title": "Gracious Gold",
                            "image_url": BASE_URL + '/img/template-3.png',
                            "subtitle": "Default colors: gold, white, black",
                            "default_action": {
                                "type": "web_url",
                                "url": BASE_URL + '/' + user_id + '/select_template/3',
                                "messenger_extensions": True,
                                "webview_height_ratio": "tall",
                                "fallback_url": BASE_URL
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": BASE_URL + '/' + user_id + '/select_template/3',
                                    "title": "Select Template"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    print fb.makeRequestPost(link, data)


def get_sender(response):
    entries = response['entry']
    messaging = entries[len(entries) - 1]['messaging']
    return messaging[len(messaging) - 1]['sender']['id'], messaging


def get_text_message_parts(messaging):
    message = messaging[len(messaging) - 1]['message']['text']
    return message


def get_file_from_parts(messaging):
    try:
        url = messaging[len(messaging) - 1]['message']['attachments'][0]['payload']['url']

        filename = 'static/tmp/'+generate_random()+".pdf"

        response = urllib2.urlopen(url)
        file = open(filename, 'wb')
        file.write(response.read())
        file.close()

        return filename
    except Exception as e:
        print e
        return None


def delete_file(f):
    pass


def get_data(d, id):
    try:
        return d[id]
    except Exception as e:
        print e
        return 'N/A'

def parse_file(f):
    data = ai.getFromJSONFile(f)

    print data

    return {
        'name': data['basics']['name']['surname'],
        'title': data['basics']['title'],
        'number': data['basics']['phone'][0],
        'email': data['basics']['email'][0],
        'website': 'N/A',
        'summary': 'N/A',
        'experience': data['work_experience'],
        'education': data['education_and_training'],
        'skills': data['skills'],
        'activities': data['extracurricular'][0]['Activities']
    }



def change_order(sender, sec1, sec2):
    pass


def change_style(sender, id, value, name):
    if id == '':
        pass

    css = '''
    
    {
    
    }
    
    '''

    putUserInfo(sender, 'custom-style', {id: value})



def change_content(sender, sec, content):
    putResumeInfo(sender, sec, content)


@app.route('/')
def index():
    return 'running...'


@app.route('/<path:path>')
def req_file(path):
    return url_for('static', filename=path)


@app.route('/render/<uid>')
def render(uid):
    print uid
    u = getUserInfo(uid)
    r = u['resume']
    template = 'template-1.html'
    if u['template'] == '2':
        template = 'template-2.html'
    elif u['template'] == '3':
        template = 'template-3.html'
    styles = ''
    try:
        s = u['custom-style']
        for key in s:
            styles += key +': ' + s[key] + '; '
    except:
        pass
    education = [{'start': "09/2015", 'end': "05/2019", 'school': 'MIT', 'degree': 'B.S. Computer Science'}]
    experience = [{'start': '10/2016', 'end': '04/2017', 'place': 'Woodside', 'title': 'Dish Washer'}]
    extra = [{'start': '12/2016', 'end': '03/2017', 'place': 'Sunnyside', 'title': 'Cook'}]
    award = [{'awards': 'NBA Chip'}]
    language = [{'language': 'English'}]
    return render_template(template, name=r['name'], title=r['title'], email=r['email'],
                           number=r['number'], web=r['website'], objective=r['summary'], education=education,
                           experience=experience, extra=extra, language=language, award=award, styles=styles)




@app.route('/<uid>/select_template/<tid>')
def select_template(uid, tid):
    print uid
    putUserInfo(uid, 'template', tid)
    send_to_recipient(uid, 'Template '+tid+' selected. I can help you edit the style and content of your resume.')
    send_to_recipient(uid, 'You can also ask me to send you a preview of your resume or a pdf file anytime.')
    return '<script>window.close()</script>'


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        response = request.get_json()

        if response['object'] == 'page':
            sender, messaging = get_sender(response)

            # check if user exists and is defined
            if user_exists_and_defined(sender):

                    f = get_file_from_parts(messaging)


                    if f is not None:
                        vals = parse_file(f)

                        putUserInfo(sender, 'resume', vals)

                        send_to_recipient('What style would you prefer?', sender)
                        send_templates_to_recipient(sender)

                        delete_file(f)

                    else:
                        try:
                            txt = get_text_message_parts(messaging)
                            action, entities = ai.get_action_value_from(txt)
                            if action is 'style':
                                id = ''
                                value = ''
                                change = ''
                                for entity in entities:
                                    if entity['entity'] == 'styles':
                                        id = entity['value']
                                    elif entity['entity'] == 'style-values':
                                        value = entity['value']
                                    elif entity['entity'] == 'change':
                                        change = entity['value']
                                if id is not '':
                                    if value is not '':
                                        if change is not '':
                                            change_style(sender, id, value, change)
                                        else:
                                            send_to_recipient("Sorry, I don't understand. Please specify the section or name of what you would like to change.", sender)
                                    else:
                                        send_to_recipient(
                                            "Sorry, I don't understand. I need a hint of what you want the "+id+" to be.",
                                            sender)
                                else:
                                    send_to_recipient(
                                        "Sorry, I don't understand. Please be more specific.",
                                        sender)
                            elif action is 'order':
                                sec1 = ''
                                sec2 = ''

                                for entity in entities:
                                    if entity['entity'] == 'change':
                                        if sec1 is '':
                                            sec1 = entity['value']
                                        else:
                                            sec2 = entity['value']

                                if sec1 is not '' and sec2 is not '':
                                    change_order(sender, sec1, sec2)
                                    send_to_recipient(
                                        "done. anything else?",
                                        sender)
                                else:
                                    send_to_recipient(
                                        "Sorry, I don't understand. Please specify the sections or names of what you would like to switch.",
                                        sender)
                            elif action is 'change':
                                sec = ''
                                text = ''

                                for entity in entities:
                                    print entity
                                    if entity['entity'] == 'change':
                                        sec = entity['value']

                                text = txt.split("to", 1)[1].strip()

                                print sec
                                print text

                                if sec is not '' and text is not '':
                                    change_content(sender, sec, text)
                                    send_to_recipient(
                                        "done. Anything else?",
                                        sender)
                                else:
                                    send_to_recipient(
                                        "Sorry, I don't understand. Please be more specific.",
                                        sender)
                            elif action is 'preview':
                                send_to_recipient('sure. '+BASE_URL+'/render/'+sender, sender)
                                pass
                            elif action is 'send':
                                pass
                            else:
                                pass
                        except Exception as e:
                            print 'what'
                            print e
                            return '500'
            # check if user exists but is not defined
            elif userId_exists(sender):
                name = ai.extract_name_from_text(get_text_message_parts(messaging))

                if name is not None:
                    send_to_recipient('Hello, ' + name + '. My name is Shane. I can help you build and design your resume.',
                                      sender)
                    send_to_recipient('What would you like to do?', sender)
                    send_to_recipient('You can start by sending me your resume or we can build it here.', sender)
                    putUserInfo(sender, 'name', name)
                else:
                    send_to_recipient("Sorry, I don't understand. What did you say your name was?", sender)
            # user does not exist
            else:
                create_user(sender)
                send_to_recipient('Hello', sender)
                send_to_recipient('What is your name?', sender)
            return '200'
    else:
        if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFICATION_TOKEN:
            return request.args.get('hub.challenge')
        else:
            return '500'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
