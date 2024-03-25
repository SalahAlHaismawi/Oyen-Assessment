### Prerequisites
1. Python 3
2. Pip to install packages.
   
### Packages Used
1. FastAPI: For creating and managing API's.
2. SQLAlchemy: For SqlLite Implementation.
3. python-jose: To create and verify JWT Tokens
4. Uvicorn: Light weight ASGI Server
   
### Installation
1. Clone the Repo: **git clone <repo-url>**
2. Navigate to the project directory: cd
3. Install required packages: **"pip install -r requirements.txt"**
   
### Running the Application
1. Start the Application using Uvicorn : "uvicorn main:app --reload"
2. Visit the application at **`http://127.0.0.1:8000/static/index.html`**
3. Register a new user in the database by using this command in a unix terminal: **curl -X POST http://localhost:8000/add_user/ -F "username=pickUsername" -F "password=pickPassword"** . For windows systems use Postman and paste the unix command to the postman url with POST Method. **Sample database is provided to skip this step**
4. after registering a user you should expect to see credentials.db, login the application to generate a JWT Token that will be stored in localStorage and will remember the user.
5. Please Refresh the page after login to get the confirmation prompt that the user is still logged in, and  to render the logout button for further login attempts.


This program is tested for both Windows and Unix Systems.



