
if __name__ == '__main__':
   import os
   os.system("rm -rf {}/home/migrations".format(os.getcwd()))
   os.system("python manage.py makemigrations home")
   os.system("python manage.py migrate auth")
   os.system("python manage.py migrate home")
   os.system("python manage.py migrate")
