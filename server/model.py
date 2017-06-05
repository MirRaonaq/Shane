'''

        users
            uid
                name
                email
                phone

                link
                    name
                    href

                rid
                    sid
                        name
                        title
                        subtitle
                        start
                        end
                        bulletpoints
                            text
                        sid
                            name
                            title
                            subtitle
                            start
                            end
                            bulletpoints
                                text

'''
from firebase import firebase

firebase = firebase.FirebaseApplication('https://shane-71f51.firebaseio.com')
# firebase = firebase.FirebaseApplication('https://shane-faae4.firebaseio.com')

def getUserInfo(userId):
    global firebase
    return firebase.get('/users', userId)


def putUserInfo(userId, key, info):
    global firebase
    uinfo = getUserInfo(userId)
    uinfo[key] = info
    resultPut = firebase.put('/users', userId, uinfo)
    return resultPut


def putResumeInfo(userId, key, info):
    global firebase
    uinfo = getResumeFromUser(userId)
    uinfo[key] = info
    resultPut = firebase.put('/users/'+userId, 'resume', uinfo)


def getResumeFromUser(userId):
    global firebase
    return firebase.get('/users/'+userId, 'resume')


def user_exists_and_defined(userId):
    global firebase
    # if firebase.get('/users/'+userId, 'name') !=' ':
    #     return True
    # else:
    #     return False
    if userId_exists(userId):
        if firebase.get('/users/' + userId, 'name') != 'N/A':
            return True
        else:
            return False
    else:
        return False

def userId_exists(userId):
    global firebase
    if firebase.get('users/', userId) is None:
        return False
    else:
        return True

def create_user(userId):
    global firebase
    resultPut = firebase.put('/users/', userId, {'name': 'N/A'})


# print user_exists_and_defined('992271094209706')