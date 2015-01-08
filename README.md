Git remotes
-----------
Generally I work with two remotes: one at github and one at openshift. To avoid confusion I
name the remotes `github` and `openshift` with openshift being the one that is configured
to be pushed to automatically.

Running Django locally using virtualenv
---------------------------------------
**Note:** This is the abbreviated/modified version of what is
[described elsewhere](http://www.jeffknupp.com/blog/2012/02/09/starting-a-django-project-the-right-way/).

First setup virtualenv
```
$ pip install virtualenv
$ virtualenv --version
12.0.4
$ virtualenv `pwd`/venv
```

Start the [virtual environment](https://virtualenv.pypa.io/en/latest/index.html) and install
[setuptools and pip](https://pip.pypa.io/en/latest/installing.html)
```
$ source venv/bin/activate
$ wget https://bootstrap.pypa.io/ez_setup.py -O - | python
$ easy_install pip
```
Then just install all of the requirements listed in `setup.py`. The virtual environment can be
turned off using a simple `deactivate`.

Setup the database and copy static. This should follow closely to `.openshift/action_hooks/deploy`
```
$ wsgi/openshift/manage.py collectstatic --noinput
$ wsgi/openshift/manage.py syncdb --noinput
```

Setup south to do the right thing
```
$ ./wsgi/openshift/manage.py schemamigration services --initial
$ ./wsgi/openshift/manage.py migrate services --fake
$ ./wsgi/openshift/manage.py syncdb
```

Finally, start the django server itself
```
$ wsgi/openshift/manage.py runserver
```

Connecting to openshift
-----------------------
First install rhc
```
$ sudo gem install rhc
```
Then you can configure it for connecting to the app
```
rhc setup
```

Deploying new versions happens through `git push`

Develop local rendering using remote database
---------------------------------------------
***This should not be done when developing the posting capabilities***

This can be done using a simple port forwarding and configuring the mysql to point at that.
First find out the username/password for the database from `rhc apps`. Then this should be
set as the username/password for the database via the environment variables
`OPENSHIFT_MYSQL_DB_USERNAME` and `OPENSHIFT_MYSQL_DB_PASSWORD`. I do this in a shell script
so I don't have to track down the information every time. Then start the port forwarding
by runing `rhc port-forward -a django`. Finally, start the server using the normal
`manage.py runserver`. Don't worry about warnings considering the database migration.
