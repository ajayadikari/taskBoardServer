from django.db import models


class UserManager(models.Manager):
    def create(self, kwargs):
        try:
            from .models import UserModel
            if kwargs.get('username', None) is None:
                raise Exception("username cannot be null")        
            password = kwargs.pop('password', None)
            if password is None:
                raise Exception("password cannot be None")
            if len(password) < 6:
                raise Exception("password should atleast contain 6 characters")
            if password.isalpha() or password.isdigit():
                raise Exception("password should contain mix of alphabets, numbers, and special characters")
            
            user = UserModel(**kwargs)
            user.set_password(password)
            user.save()

            return user
        
        except Exception as err:
            print("------------------------------")
            print("err--user/manager.py--create")
            print(err)
            raise Exception("errors while creating user")
    
    def create_user(self, kwargs):
        print(kwargs)
        kwargs["is_staff"] = False
        kwargs["is_active"] = True
        kwargs["is_superuser"] = False

        return self.create(kwargs)
    
    def create_superuser(self,kwargs):
        kwargs["is_staff"] = True
        kwargs["is_active"] = True
        kwargs["is_superuser"] = True

        return self.create(kwargs)
    
    def get_by_natural_key(self, username):
        """
        This method is necessary for the authentication system to look up a user by their 'username'.
        """
        return self.get(username=username)