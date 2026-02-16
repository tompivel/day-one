## Manual review

The authentication works! I can register and it automatically logs in after a successful register. Then, the JWT token is saved on local storage sucessfully. However, an already logged in user can access to the login page and register page. This is a security issue. Fix this issue.

Also, I've noticed there are several constants like "localhost:8000" or "localhost:5173" hardcoded across the codebase. This is not a good practice. I suggest creating a .env file to store these constants and using a library like python-dotenv to load them if pertinent. Also, move the secret key for JWT tokens to a .env file.

Additionally, create a .gitignore file on the root directory to ignore the .env file, the .venv directory, the __pycache__ directory, the node modules directory and all other temporary or restricted files like the database.

Finally, git-add and git-commit the project in an orderly way. The repo is: "git@github.com:tompivel/day-one.git". Push the changes to the repository.