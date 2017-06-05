from watson_developer_cloud import ConversationV1
import json
import os
import subprocess
# from selenium import webdriver
# from xvfbwrapper import Xvfb

conversation = ConversationV1(
        username='bf882a69-bfc8-45b2-bd0b-c45ce756947b',
        password='2uQaCTLHhliA',
        version='2017-04-21'
    )

workspace_id = '04174a9c-650c-409f-bdb3-93290679e4ad'


def extract_name_from_text(text):

    response = conversation.message(
        workspace_id=workspace_id,
        message_input={'text': text}
    )

    for entity in response['entities']:
        if entity['entity'] == 'sys-person':
            return entity['value']

    return None


def get_action_value_from(text):
    response = conversation.message(
        workspace_id=workspace_id,
        message_input={'text': text}
    )

    action = ''

    try:
        if len(response['entities']) != 0:
            for entity in response['entities']:
                if entity['entity'] == 'styles':
                    action = 'style'
                    id = entity['value']
                elif entity['entity'] == 'style-values':
                    value = entity['value']
                elif entity['entity'] == 'change' or entity['entity'] == 'alter':
                    if action == '':
                        action = 'change'
                elif entity['entity'] == 'order':
                    pass

            return action, response['entities']
        else:
            for entity in response['intents']:
                if entity['intent'] == 'preview':
                    action = 'preview'
                elif entity['intent'] == 'alter':
                    action = 'change'
            return action, response['intents']
    except Exception as e:
        print e



def execute(text):

    response = conversation.message(
        workspace_id=workspace_id,
        message_input={'text': text}
    )

    print response

    try:
        entity = response['entities'][0]
        if entity['entity'] == 'sys-person':
            return entity['value']

        print json.dumps(response, indent=2)
    except Exception as e:
        print e
        try:
            entity = response['intents'][0]
            if entity['entity'] == 'sys-person':
                return entity['value']
            print json.dumps(response, indent=2)
        except Exception as e:
            print e


# def save_page_to_image(url):
#     d = Xvfb(width=400, height=400)
#     d.start()
#     browser = webdriver.Firefox()
#     url = "http://stackoverflow.com/questions/4091940/how-to-save-web-page-as-image-using-python"
#     browser.get(url)
#     destination = "screenshot_filename.jpg"
#     if browser.save_screenshot(destination):
#         print "File saved in the destination filename"
#     browser.quit()


# save_page_to_image('https://google.com')


# execute('send me a preview')

# print get_action_value_from('change my name to Mir')

#fileLocation is the input string of where the file is located
#The format of the input string should just be "/your/path/to/file"
def getFromJSONFile(fileLocation):
    #CHANGE WHAT IS INSIDE THIS NEXT LINE TO YOUR DIRECTORY, THIS IS MY DIRECTORY FOR THE RESUMEPARSER
    fileLocation = r'C:\Users\mdnah\Desktop\tbd\server\'' + fileLocation
    os.chdir(r"C:\Users\mdnah\Desktop\tbd\server\ResumeParser\ResumeTransducer")
    print subprocess.call(r"java -cp '.\bin\*;..\GATEFiles\lib\*;..\GATEFiles\bin\gate.jar;.\lib\*' code4goal.antony.resumeparser.ResumeParserProgram "+fileLocation+" output.json", shell=True)
    with open('output.json', 'r') as output_file:
        data=json.load(output_file)
    return data


# print getFromJSONFile(r'C:\Users\mdnah\Desktop\tbd\server\static\tmp\N401BGWC.pdf')


#def swapResumeSections(userId,key1,key2):


#The main method below was for testing to see if getFromJSONFile worked alongside putUserInfo. This is how you
#would use the two methods if you wanted to add a name to the firebase
#def main():
    #out=getFromJSONFile('/Users/Harrison/Documents/HarrisonNgoResume.docx')
    #putUserInfo('uid','name',out['basics']['name']['firstName'])
#    putUserInfo('uid2','phone','1234567890')
 #   putUserInfo('uid2','address','hoodside')

#main()