# VM Control Panel (Django)
A simple Django website to control power ON/OFF actions for 5 virtual machines.
### Setup
To get this repository, run the following command inside your git enabled terminal
```bash
$ git clone https://github.com/shreys7/django-todo.git
```
You will need django to be installed in you computer to run this app. Head over to https://www.djangoproject.com/download/ for the download guide

Once you have downloaded django, go to the cloned repo directory and run the following command

```bash
$ python manage.py makemigrations
```

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command
```bash
$ python manage.py migrate
```

One last step and then our todo App will be live. We need to create an admin user to run this App. On the terminal, type the following command and provide username, password and email for the admin user
```bash
$ python manage.py createsuperuser
```

That was pretty simple, right? Now let's make the App live. We just need to start the server now and then we can start using our simple todo App. Start the server by following command

```bash
$ python manage.py runserver
```

Once the server is hosted, head over to http://127.0.0.1:8000/todos for the VM Control Panel.

## Configure real VM commands

By default, each VM action runs an `echo` command so you can test safely.
To run real commands, update `VM_CONTROL_COMMANDS` in `todoApp/settings.py` (or your environment-specific settings):

```python
VM_CONTROL_COMMANDS = {
    "vm1": {
        "name": "Virtual Machine 1",
        "power_on": ["virsh", "start", "vm1"],
        "power_off": ["virsh", "shutdown", "vm1"],
    },
    # vm2..vm5
}
```

You can also use a single shell command string if needed (for example on Windows):

```python
"power_on": r"C:\scripts\startvm1.bat"
```

Cheers and Happy Coding :)
