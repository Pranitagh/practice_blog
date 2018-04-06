import pymongo
import bottle
import sessions
import users
import posts
import html
import re


@bottle.route('/')
def home_page():
    cookie = bottle.request.get_cookie("session")

    username = session.get_sessionusername(cookie)

    getposts = posted.get_posts(10)

    return bottle.template('homepage', dict(myposts=getposts, username=username))


@bottle.get('/signup')
def signup():
        return bottle.template("signup",
                           dict(username="", password="",
                                password_error="",
                                email="", username_error="", email_error="",
                                verify_error =""))

@bottle.post('/signup')
def process_signup():

    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    verify = bottle.request.forms.get("verify")
    errors = {'username': html.escape(username), 'email': html.escape(email)}

    if validate_signupentry(username, password, verify, email, errors):

        if not user.add_user(username, password, email):
            # this was a duplicate
            errors['username_error'] = "Username already in use. Please choose another"
            return bottle.template("signup", errors)

        session_id = session.start_session(username)
        print (session_id)
        bottle.response.set_cookie("session", session_id)
        bottle.redirect("/dashboard")
    else:
        print ("user did not validate")
        return bottle.template("signup", errors)

@bottle.get("/dashboard")
def present_welcome():

    cookie = bottle.request.get_cookie("session")
    username = session.get_sessionusername(cookie)  # see if user is logged in
    if username is None:
        print ("welcome: can't identify user...redirecting to signup")
        bottle.redirect("signup")

    return bottle.template("dashboard", {'username': username})

@bottle.get('/login')
def present_login():
    return bottle.template("login",  dict(username="", password="", login_error=""))


@bottle.post('/login')
def process_login():

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    print ("username submitted ", username, "password ", password)

    user_record = user.validate_login(username, password)
    if user_record:
        # username is stored in the user collection in the _id key
        session_id = session.start_session(user_record['_id'])

        if session_id is None:
            bottle.redirect("/dashboard")

        cookie = session_id

        bottle.response.set_cookie("session", cookie)

        bottle.redirect("/dashboard")

    else:
        return bottle.template("login",
                               dict(username=html.escape(username), password="",
                                    login_error="Invalid Login"))



def validate_signupentry(username, password, verify, email, errors):
    userregex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    passwordregex = re.compile(r"^.{3,20}$")
    emailregex = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error'] = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""

    if not userregex.match(username):
        errors['username_error'] = "invalid username. try just letters and numbers"
        return False

    if not passwordregex.match(password):
        errors['password_error'] = "invalid password."
        return False
    if password != verify:
        errors['verify_error'] = "password must match"
        return False
    if email != "":
        if not emailregex.match(email):
            errors['email_error'] = "invalid email address"
            return False
    return True



@bottle.get('/logout')
def process_logout():
    cookie = bottle.request.get_cookie("session")
    session.end_session(cookie)
    bottle.response.set_cookie("session", "")
    bottle.redirect("/")


@bottle.get('/newpost')
def newpost():
    cookie = bottle.request.get_cookie("session")
    username = session.get_sessionusername(cookie)  # see if user is logged in
    if username is None:
        bottle.redirect("/login")
    return bottle.template('newpost', dict(subject="", body = "", errors="", tags="", username=username))

def extract_tags(tags):

    whitespace = re.compile('\s')

    nowhite = whitespace.sub("",tags)
    tags_array = nowhite.split(',')

    # let's clean it up
    taglist = []
    for tag in tags_array:
        if tag not in taglist and tag != "":
            taglist.append(tag)

    return taglist

@bottle.get("/post/<permalink>")
def show_post(permalink="notfound"):

    cookie = bottle.request.get_cookie("session")

    username = session.get_sessionusername(cookie)
    permalink = html.escape(permalink)

    print("about to query on permalink = ", permalink)
    post = posted.get_post_by_permalink(permalink)

    if post is None:
        bottle.redirect("/post_not_found")

    # init comment form fields for additional comment
    comment = {'name': "", 'body': "", 'email': ""}

    return bottle.template("entry_template", dict(post=post, username=username, errors="", comment=comment))

@bottle.get("/post_not_found")
def post_not_found():
    return "Sorry, post not found"

@bottle.post('/newpost')
def post_newpost():
    title = bottle.request.forms.get("subject")
    post = bottle.request.forms.get("body")
    tags = bottle.request.forms.get("tags")

    cookie = bottle.request.get_cookie("session")
    username = session.get_sessionusername(cookie)  # see if user is logged in
    if username is None:
        bottle.redirect("/login")

    if title == "" or post == "":
        errors = "Post must contain a title and blog entry"
        return bottle.template("newpost", dict(subject=html.escape(title, quote=True), username=username, body=html.escape(post, quote=True), tags=tags, errors=errors))

    # extract tags
    tags = html.escape(tags)
    tags_array = extract_tags(tags)

    # looks like a good entry, insert it escaped
    escaped_post = html.escape(post, quote=True)

    # substitute some <p> for the paragraph breaks
    newline = re.compile('\r?\n')
    formatted_post = newline.sub("<p>", escaped_post)

    permalink = posted.insert_postentry(title, formatted_post, tags_array, username)

    # now bottle.redirect to the blog permalink
    bottle.redirect("/post/" + permalink)



@bottle.post('/newcomment')
def post_new_comment():
    name = bottle.request.forms.get("commentName")
    email = bottle.request.forms.get("commentEmail")
    body = bottle.request.forms.get("commentBody")
    permalink = bottle.request.forms.get("permalink")

    post = posted.get_post_by_permalink(permalink)
    cookie = bottle.request.get_cookie("session")

    username = session.get_sessionusername(cookie)

    # if post not found, redirect to post not found error
    if post is None:
        bottle.redirect("/post_not_found")
        return

    if name == "" or body == "":
        # user did not fill in enough information

        comment = {'name': name, 'email': email, 'body': body}

        errors = "Post must have your name and an actual comment."
        return bottle.template("entry_template", dict(post=post, username=username, errors=errors, comment=comment))

    else:

        posted.add_postcomment(permalink, name, email, body)

        bottle.redirect("/post/" + permalink)

@bottle.get('/authorspecific')
def author_post():
    cookie = bottle.request.get_cookie("session")
    author = session.get_sessionusername(cookie)
    authorpost = posted.get_post_by_author(author)
    return bottle.template('homepage', dict(myposts= authorpost, username=author))

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.blog

user = users.User(database)
session = sessions.Session(database)
posted = posts.BlogPost(database)

bottle.debug(True)
bottle.run(host = 'localhost', port = 8080)