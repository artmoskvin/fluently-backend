# fluently-backend

## Development

1. Install [pyenv](https://github.com/pyenv/pyenv)
2. Install [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
3. Clone project `git clone git@github.com:artmoskvin/fluently-backend.git`
4. Go to the project root `cd fluently-backend`
5. Create new virtualenv `pyenv virtualenv 3.10 fluently-be`
6. Make it default for the project `pyenv local fluently-be`
7. Install dependencies `pip install -r requirements.txt`
8. Run tests `pytest`
9. Run server locally `flask --app fluently.app run`
