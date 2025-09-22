# Plan That Week! ![xxx](https://img.shields.io/badge/sad-asdas-asdas)
![xxx](/codecov/c/:vcsName/:user/:repo?flag=flag_name&token=a1b2c3d4e5)


/codecov/c/:vcsName/:user/:repo?flag=flag_name&token=a1b2c3d4e5

The task planner that you did not knew you were missing :)

## What's that?

Plan That Week is a task planner that allows to manage tasks by week. The interface always displays an entire week. Each day can hold individual tasks, plus there is a section for the tasks that do not neccessarily need to be done/finished on a specific day.

Tasks can be moved from day to day by dragging them where you want them to be. Also dragging tasks to other weeks is easily done by dragging it to the appropriate week number in the header section. 

There is no priority, tags, task owner and so forth (yet).

## Why?

Why would anybody want to code a to-do app when there is already at least a thousand out there?
Well, first of all I never found something that allowed me to plan for the entire week without distraction and a lot of back and forth, second I might just have looked for something to go a little deeper with python and flask and refredh some old html/css/javascript knowledge. Here we go.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- python
- flask
- ...

### How to install and run

Initially I was tempted to create another container on my smarthome rapsi to host the app as web service. Since I purposly don't expose anythin from my local network to the outside world - I would not be able to access my tasks while not in the home office. Ouch!

Therefore I decided to keep it as a python project sitting on my synced OneDrive-folder to be able to run it from any location and any end device.

If you want to give it a try, copy the repository to the location of your preference, and run
``` cmd
pip install -r requirements.txt
```

Create a database with
``` cmd
python initdb.py
```

and start th application with
``` cmd
python app.py
```

You should see an output including a line like this
``` cmd
Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

If not already occupied or specified otherwise, the app should become accessible at [localhost:5000](http://127.0.0.1:5000).


### How to use the app

Create new tasks by clicking into the input fields, start typing and press enter or click the button right next to the input field.

Move tasks to different positions within the day, to different days or weeks by dragging them where you want them to be.

Edit tasks by dragging them to the edit field in the top right corner of the window. This allows to change the title of the tasks as well as to add an url that will be accessible together with the task.

Delete unneccesary tasks by dragging them to the delete field in the top right corner of the window.

Close (mark done) tasks by clicking into the square in front of the task name.
Undo tasks by clikcing the checked square again.

That's it. Nothing more, nothing less. 


## License

https://choosealicense.com/licenses/

GNU GPLv3

## Badges

https://shields.io/category/dependencies

## How to contribute

## Run Tests

