#!/usr/bin/env python3
import sys

login_page = '''\
<html>
<body>
<p>Hello userID {0}, you have logged in using a "POST" form. <br>
This is safer than GET,  as your password {1} is <b> NOT </b> in your URL bar.
<br> Thank you! <br>
Click <a href=/test_form_post.html> HERE </a> to return to the login page. <br>
</p>
</body>
</html>
'''
add_page = '''\
<html>
<body>
<p>Thank you for creating your account on <b>not_a_security_breach.com</b>,  {0}.<br>
Your userid is <b>{1}</b> and your password is <b>{2}</b>, and is safe from
the world. <br>
Thank you! <br>
Click <a href=/test_form_post.html> HERE </a> to return to the login page. <br>
</p>
</body>
</html>
'''
delete_page = '''\
<html>
<body>
<p>
You have deleted your account with userID {0} <br>
Thank you for securing your details! <br>
Click <a href=/test_form_post.html> HERE </a> to return to the login page. <br>
</p>
</body>
</html>
'''

args = sys.argv

arg_dict = {"action": -1,
            "userid": -1,
            "password": -1,
            "name": -1,
            "newuserid": -1,
            "newpassword": -1,
            "deluserid": -1}


for e in args:
    if "=" in e:
        tmp = e.split("=")
        arg_dict[tmp[0]] = tmp[1]

# print(arg_dict, file=sys.stderr)
rv = ""
if arg_dict["action"] == "login":
    # assumes 'userid' and 'password' is set, ignores everything else.
    rv = login_page.format(arg_dict["userid"], arg_dict["password"])

elif arg_dict["action"] == "add":
    rv = add_page.format(arg_dict["name"], arg_dict["newuserid"], arg_dict["newpassword"])

elif arg_dict["action"] == "delete":
    rv = delete_page.format(arg_dict["deluserid"])


print(rv)
