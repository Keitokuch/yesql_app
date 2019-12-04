from model import User
import service.user_service as users

#  user = User()

#  user.passwd = "goodone"

#  print(user.passwd)

#  user = users.signup_user("first_user", "mypassword")
#  print(user.id)

user = users.login_user("first_user", 'mypassword')
if user:
    print(user.id, user.is_authenticated)
