# Data analysis
- Document here the project: le-package
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for le-package in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/le-package`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "le-package"
git remote add origin git@github.com:{group}/le-package.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
le-package-run
```

# Install

Go to `https://github.com/{group}/le-package` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/le-package.git
cd le-package
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
le-package-run
```



http://127.0.0.1:8000/predict_clusters/?digital_transformation=2&employee_engagement=3&employee_satisfaction=4&innovation=5&internationalization=4&market_competitiveness=2&people_management=2&people_structure=3&recruitment=4&training_and_development=5&work_processes=4


http://127.0.0.1:8000/predict_clusters/?digital_transformation=0&employee_engagement=3&employee_satisfaction=0&innovation=5&internationalization=0&market_competitiveness=0&people_management=0&people_structure=3&recruitment=0&training_and_development=5&work_processes=0

http://127.0.0.1:8000/predict_cluster/?digital_transformation=2&employee_engagement=3&employee_satisfaction=2&innovation=2&internationalization=2&market_competitiveness=2&people_management=2&people_structure=3&recruitment=2&training_and_development=2&work_processes=2


http://127.0.0.1:8000/predict_cluster/?digital_transformation=2&employee_engagement=3&employee_satisfaction=2&innovation=3&internationalization=2&market_competitiveness=3&people_management=5&people_structure=3&recruitment=2&training_and_development=2&work_processes=2
