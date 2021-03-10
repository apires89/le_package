# ----------------------------------
#          INSTALL & TEST
# ----------------------------------

# project id
PROJECT_ID=leading-enterprise  # Replace with your Project's ID

# bucket name
BUCKET_NAME=leading-enterprise-wagon-apires89 # Use your Project's name as it should be unique

REGION=europe-west1 # Choose your region https://cloud.google.com/storage/docs/locations#available_locations

# path of the file to upload to gcp (the path of the file should be absolute or should match the directory where the make command is run)
LOCAL_PATH='/Users/andrecabralpires/code/apires89/le_package/raw_data/ecs2019_mm_ukds.csv' # Replace with your local path to the `train_1k.csv` and make sure to put it between quotes

# bucket directory in which to store the uploaded file (we choose to name this data as a convention)
BUCKET_FOLDER='data'

# name for the uploaded file inside the bucket folder (here we choose to keep the name of the uploaded file)
# BUCKET_FILE_NAME=another_file_name_if_I_so_desire.csv
BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})

##### Package params  - - - - - - - - - - - - - - - - - - -

PACKAGE_NAME=le_package
FILENAME=trainer

##### Job - - - - - - - - - - - - - - - - - - - - - - - - -

JOB_NAME=leading_enterprise_training_pipeline_$(shell date +'%Y%m%d_%H%M%S')


# REGION=europe-west1

PYTHON_VERSION=3.7
FRAMEWORK=scikit-learn
RUNTIME_VERSION=1.15

upload_data:
	@gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* le-package/*.py

black:
	@black scripts/* le-package/*.py

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
	@rm -fr le-package-*.dist-info
	@rm -fr le-package.egg-info

install:
	@pip install . -U

all: clean install test black check_code


uninstal:
	@python setup.py install --record files.txt
	@cat files.txt | xargs rm -rf
	@rm -f files.txt

run_api:
	uvicorn api.fast:app --reload

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
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

run_locally:
	@python -m ${PACKAGE_NAME}.${FILENAME}

