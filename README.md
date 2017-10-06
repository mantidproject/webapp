Git remotes
-----------
Generally I work with two remotes: one at github and one at openshift. To avoid confusion I
name the remotes `github` and `openshift` with openshift being the one that is configured
to be pushed to automatically.

Running Django locally using virtualenv
---------------------------------------
**Note:** This is the abbreviated/modified version of what is
[described elsewhere](http://www.jeffknupp.com/blog/2012/02/09/starting-a-django-project-the-right-way/).

First setup virtualenv with python3. This should be done in your source tree.
```
$ pip install virtualenv
$ virtualenv --version
15.1.0
$ virtualenv -p python3 `pwd`/venv
```

Start the [virtual environment](https://virtualenv.pypa.io/en/latest/index.html) and install
[setuptools and pip](https://pip.pypa.io/en/latest/installing.html)
```
$ source venv/bin/activate
$ wget https://bootstrap.pypa.io/ez_setup.py -O - | python
```
Before running the install script, you need to have `mysql_config`
installed. On fedora 25 it is contained in a package called
`community-mysql-devel`. For mac run `brew install mysql`. Then just
install all of the requirements listed in the setup file. Run the
command
```
python setup.py install
```
The virtual environment can be turned off using a simple `deactivate`.

Setup the database and copy static. This should follow closely to [`.openshift/action_hooks/deploy`](https://github.com/mantidproject/webapp/blob/master/.openshift/action_hooks/deploy)
```
$ wsgi/openshift/manage.py collectstatic --noinput
$ wsgi/openshift/manage.py syncdb --noinput
```

Setup built-in db migrations to do the right thing(tm)
```
$ ./wsgi/openshift/manage.py migrate
```
When asked for about creating an admin account, just say "no." The
`manage.py makemigrations services` is only necessary when updating
the models.

If you have a sql dump to ingest, this can be done using
```
$ wsgi/openshift/manage.py dbshell
SQLite version 3.20.1 2017-08-24 16:21:36
Enter ".help" for usage hints.
sqlite> .read filename.sql
...
sqlite> .quit
```
I get an error message when `sqlite3` exits, but all of the data is ingested.

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
$ rhc setup
```

Deploying new versions happens through `git push`

Develop local rendering using remote database
---------------------------------------------
***This should not be done when developing the posting capabilities***

This can be done using a
[simple port forwarding](https://blog.openshift.com/getting-started-with-port-forwarding-on-openshift/)
and configuring the mysql to point at that. First find out the
username/password for the database from `rhc apps`. Then start the
port forwarding of just the `mysql` connection
```
$ rhc port-forward -a django -s mysql
```
In a separate terminal start the webapp using
```
$ OPENSHIFT_MYSQL_DB_USERNAME=xxxxxxxx OPENSHIFT_MYSQL_DB_PASSWORD=xxxxxxxx wsgi/openshift/manage.py runserver
```
The username/password need to be injected via environment variables
otherwise the webapp will use the local (on disk) database. Don't
worry about warnings considering the database migration.

Working with docker
-------------------

After [installing docker](https://docs.docker.com/engine/installation/), verify the "hello world" image. [On fedora](https://docs.docker.com/engine/installation/linux/docker-ce/fedora/), the instructions are simply

```
$ sudo systemctl start docker
$ sudo docker run hello-world
```

To do build things with docker you will need to add yourself to the `docker` group
```
sudo usermod -aG docker $USER
```
You can try one of the variety of [quickstart
guides]https://docs.docker.com/get-started/part2/) to make sure that
your setup is otherwise working. Much of the following is heavily
adapted from the [docker django instructions](https://docs.docker.com/compose/django/).
