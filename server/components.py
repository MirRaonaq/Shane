class User:

    def __init__(self, id, name, email, phone, links):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.links = links


class Links:

    def __init__(self, website, linkedIn, twitter, facebook, dribbble):
        self.website = website
        self.linkedIn = linkedIn
        self.twitter = twitter
        self.facebook = facebook
        self.dribbble = dribbble


class Section:

    def __init__(self, title, subtitle, right, bullet_points):
        self.title = title
        self.subtitle = subtitle
        self.right = right
        self.bullet_points = bullet_points


class Resume:

    def __init__(self, raw):
        self.raw = raw
        self.user = User(raw[0], raw[1], raw[2], raw[3], raw[4])
        self.links = Links(raw[5], raw[6], raw[7], raw[8], raw[9])
        self.summary = raw[10]
        self.education = raw[11]
        self.employment = raw[12]
        self.skills = raw[13]
        self.projects = raw[14]
        self.awards = raw[15]
        self.activities = raw[16]



