# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* geotracker/*.py

black:
	@black scripts/* geotracker/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr geotracker-*.dist-info
	@rm -fr geotracker.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=castoldie
PACKAGE_NAME=geotracker

build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

REQ_FILENAME=request

make_request:
	@python -m ${PACKAGE_NAME}.api.${REQ_FILENAME}

streamlit:
	@streamlit run geotracker/website/app.py

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------
heroku_login:
	-@heroku login
heroku_create_app:
	-@heroku create ${APP_NAME}
deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1
# ----------------------------------
#    LOCAL INSTALL COMMANDS
# ----------------------------------

clean:
    #@rm -fr */__pycache__
	@rm -fr __init__.py
    #@rm -fr build
    #@rm -fr dist
    #@rm -fr *.dist-info
    #@rm -fr *.egg-info
    #-@rm model.joblib
