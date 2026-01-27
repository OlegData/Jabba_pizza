#This is Jabba Pizza portal

##Run locally

CLI: uvicorn web.app.main:app --reload --host 127.0.0.1 --port 8000
Python: python -m web.app.main --debug


##Development 
Before pushing changes to repo update Build file 
pants tailor web::

##Run tests 
Run all test
pants test web::

run specific test
pants test web/app/home:tests -- -k HomeRouteTest
