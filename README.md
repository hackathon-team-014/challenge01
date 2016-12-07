# challenge01

#create a virtual environmnent
virtualenv venv

#activate this environmnent
venv\Scripts\activate

#install the requirements
pip install -r requirements.txt

#run locally 
python main.python

#deploy
gcloud app deploy --project=hackathon-team-014 --version=v1 ./app.yaml