Hello, in this blog, iam going give instructions on how to run my application in your local server

requirements:- you should have these softwares in your server to run both client and server applications
1. node
2. pip
3. python
4. msys2 (follow the official documentation)
5. bash(if possible)
6. npm

instructions: (blindly copy paste these cmds)
1. clone my client repo and move into it
2. run - py -m venv myenv (whatever name or enviroment you want to use)
3. run - source myenv/Scripts/activate (if you use bash)
4. run - myenv/Scripts/activate (if you use powershell)
5. run  - pip install -r requirements.txt
6. run - py manage.py makemigrations
7. run - py manage.py migrate
8. run - py manage.py runserver

that's it, the server/backend is running in your server at localhost:8000, now follow the client instruction. link to client app: [https://github.com/ajayadikari/taskBoardServer](https://github.com/ajayadikari/taskBoardClient)
