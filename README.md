# fastapi-proj

/api/v1/signup
--------------
A request which is sending to this endpoint create a user in MySQL db.

/api/v1/login
-------------
When you send request to this endpoint with your credentials, it returns access token and 
refresh token(it is used to refresh your token with request to "/api/v1/refresh" ) in response

/api/v1/refresh
---------------
And this endpoint is used to refresh your access token

/api/v1/user
------------
With sending your access token in the header of request, you can see your user informations

/api/v1/task
------------
When you send request with your access token in the header, it create and save a task in MySQL db 
with the informations which are task id and authorized user`s ip address. It fetches ip data
from https://ipdata.co/

/api/v1/status/:id
------------------
You can check out tasks which you create, just you need to send access token in the header of request.
And give the id of task to the endpoint


P.S. you should use Postman or another application like Postman,
in Swagger you can`t pass the access token to the header of request
