# fluently-backend

## Development

1. Install [pyenv](https://github.com/pyenv/pyenv)
2. Install [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
3. Clone project `git clone git@github.com:artmoskvin/fluently-backend.git`
4. Go to the project root `cd fluently-backend`
5. Install Python 3.10 `pyenv install 3.10`
6. Create new virtualenv `pyenv virtualenv 3.10 fluently-be`
7. Make it default for the project `pyenv local fluently-be`
8. Install dependencies `pip install -r requirements.txt`
9. Run tests `pytest`
10. Run server locally `flask --app fluently run --debug`
