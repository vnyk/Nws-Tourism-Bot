
$ hasura microservice open app

```python
# hasura.py

@hasura_examples.route("/get_articles")
def get_articles():
    query = {
        "type": "select",
        "args": {
            "table": "article",
            "columns": [
                "*"
            ]
        }
    }

    response = requests.post(
        dataUrl, data=json.dumps(query)
    )
    data = response.json()

    return jsonify(data=data)
```

This snippet of code returns a JSON similar to the following format:

```json
{
  "data": [
    {
      "author_id": 12,
      "content": "Vestibulum accumsan neque et nunc. Quisque...",
      "id": 1,
      "rating": 4,
      "title": "sem ut dolor dapibus gravida."
    },
    {
      "author_id": 10,
      "content": "lacus pede sagittis augue, eu tempor erat neque...",
      "id": 2,
      "rating": 4,
      "title": "nonummy. Fusce fermentum fermentum arcu."
    }, 
    ...
  ]
}
```

### Internal & External URLs

If you look closer in `hasura.py`, `dataUrl` is defined in two different ways, internal and external. When your app is running inside the cluster, it can directly contact the Data APIs without any authentication. On the other hand, external URLs always go through the API Gateway, and hence special permissions will have to be applied over table for a non-authenticated user to access data.

- `http://data.hasura` - internal url
- `http://data.[cluster-name].hasura-app.io` - external url

*PS*: [Hasura Data APIs](https://docs.hasura.io/0.15/manual/data/index.html) are really powerful with nifty features like relationships, role based row and column level permissions etc. Using the APIs to their full potential will prevent you from re-inventing the wheel while building your app and can save a lot of time. 

*TIP*: Use `hasura ms list` to get all internal and external URLs available in your current cluster.

## Add authentication

When your app needs authentication, [Hasura Auth APIs](https://docs.hasura.io/0.15/manual/users/index.html) can be used to manage users, login, signup, logout etc. You can think of it like an identity service which takes away all the user management headaches from your app so that you can focus on your app's core functionality.

Just like the Data APIs, you can checkout and experiment with the Auth APIs using [Hasura API Console](https://docs.hasura.io/0.15/manual/api-console/index.html).

Combined with database permission and API gateway session resolution, you can control which user or what roles have access to each row and column in any table.

### API gateway & session middleware

For every request coming through external URL into a cluster, the API gateway tries to resolve a user based on a `Cookie` or an `Authorization` header. If none of them are present or are invalid, the following header is set and then the request is passed on to the upstream service:

- `X-Hasura-Role: anonymous`


But, if the cookie or the authorization header does resolve to a user, gateway gets the user's ID and role from auth microservice and add them as headers before passing to upstream:

- `X-Hasura-User-Id: 3`
- `X-Hasura-Role: user`

Hence, other microservices need not manage sessions and can just rely on `X-Hasura-Role` and `X-Hasura-User-Id` headers.

## Customize

Hasura runs [microservices](https://docs.hasura.io/0.15/manual/custom-microservices/index.html) as Docker containers on a Kubernetes cluster.
You can read about [Hasura architecture](https://docs.hasura.io/0.15/manual/cluster/architecture.html) in case you want to know more.

### Add a python dependency

In order use new python package in your app, you can just add it to `src/requirements.txt` and the git-push or docker build process will
automatically install the package for you. If the `pip install` steps thorw some errors in demand of a system dependency,
you can install those by adding it to the `Dockerfile` at the correct place.

```
# src/requirements.txt:

flask
requests
gunicorn

# add your new packages one per each line
```

### Add a system dependency

The base image used in this boilerplate is [python:3](https://hub.docker.com/_/python/) debian. Hence, all debian packages are available for installation.
You can add a package by mentioning it in the `Dockerfile` among the existing `apt-get install` packages.

```dockerfile
# Dockerfile

FROM python:3

# install required debian packages
# add any package that is required after `python-dev`, end the line with \
RUN apt-get update && apt-get install -y \
    build-essential \
    python-dev \
&& rm -rf /var/lib/apt/lists/*

# install requirements
COPY src/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# set /app as working directory
WORKDIR /app

# copy current directory to /app
COPY . /app

# run gunicorn server
# port is configured through the gunicorn config file
CMD ["gunicorn", "--config", "./conf/gunicorn_config.py", "src:app"]

```

### Deploy your existing Flask app

If you already have a Flask app and want to deploy it onto Hasura, read ahead:

- Replace the contents of `src/` directory with your own app's python files.
- Leave `k8s.yaml`, `Dockerfile` and `conf/` as it is.
- Make sure there is already a `requirements.txt` file present inside the new `src/` indicating all your python dependencies (see [above](#add-a-python-dependency)).
- If there are any system dependencies, add and configure them in `Dockerfile` (see [above](#add-a-system-dependency)).
- If the Flask app is not called `app`, change the last line in `Dockerfile` reflect the same.
  For example, if the app is called `backend`, the `CMD` line in `Dockerfile` will become:
  ```dockerfile
  CMD ["gunicorn", "--config", "./conf/gunicorn_config.py", "src:backend"]
  ```

## Local development

With Hasura's easy and fast git-push-to-deploy feature, you hardly need to run your code locally.
However, you can follow the steps below in case you have to run the code in your local machine.

### Without Docker

It is recommended to use a [Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for Python when you are running locally.
Don't forget to add these directories to `.gitignore` to avoid committing packages to source code repo.

```bash
# setup pipenv or virtualenv and activate it (see link above)

# go to app directory
$ cd microservices/app

# install dependencies
$ pip install -r src/requirements.txt

# Optional: set an environment variable to run Hasura examples 
# otherwise, remove Hasura examples, 
#   delete lines 5-8 from `src/__init__.py`
#   remove file `src/hasura.py`
$ export CLUSTER_NAME=[your-hasura-cluster-name]

# run the development server (change bind address if it's already used)
$ gunicorn --reload --bind "0.0.0.0:8080" src:app
```

Go to [http://localhost:8080](http://localhost:8080) using your browser to see the development version on the app.
You can keep the gunicorn server running and when you edit source code and save the files, the server will be reload the new code automatically.
Once you have made required changes, you can [deploy them to Hasura cluster](#deploy).

### With Docker

Install [Docker CE](https://docs.docker.com/engine/installation/) and cd to app directory:

```bash
# go to app directory
$ cd microservices/app

# build the docker image
$ docker build -t hello-python-flask-app .

# build the docker imageupdated on the running app.

