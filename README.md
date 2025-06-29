# 📝 Content Curation API
A Content Curation API that enables efficient article management, including categorization, author tagging, and keyword-based search functionality.


## ⚙️ Features

- Users can sign up and log in using access and refresh tokens.
- Admins can manage user statuses and assist with user ID recovery.
- Users can create content with associated categories and tags.
- Users can update and delete their own content.
- All published content is publicly searchable.
- Logged-in users can summarize, analyze sentiment, and extract topics from any published content using our AI-Agent api.

## 🏗️ Tech Stack
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Alembic (for migrations)
- Pydantic
- Typer (for CLI)

## 🧪 Installation
```
git clone https://github.com/sajidurshajib/content-curation-api.git
cd content-curation-api
touch .env
```

### 🌴 Environment template
```
DEV=True
DOCS=/docs
REDOCS=None
DB_USER=fastuser
DB_PASSWORD=fastpassword!
DB_HOST=db
DB_NAME=fastdb
DB_PORT=5432
SECRET_KEY=p7dy3qua3jxkspo&=#0xd56t-3a7g0mnj_s5(2g=eh#)jd^!6y
ALGORITHM=HS256
GROQ_API_KEY=
```
**Note:** *Set up your GROQ API key.*  
I've simplified all important commands using a `Makefile`, so you can set up the project easily using the `make` command.   (Feel free to check the `Makefile` for available commands.)

### 🏡 Build

```
make build
make start
```
**Note:** These commands build and run your project in Docker.  
If you find that your database tables are not created, use `make restart`.  
(This may happen the first time you run the project.)


## 👨🏻‍💻 Setup and Seed
> sweager api doc:  http://localhost/docs

1. First, seed the roles. Make sure the project is running.  
   Use `make cli seed=roles` — this will create 4 default roles.  
   Now, use the signup API to create an `admin` user.  
   *(Only one admin user can be created.)*
2. Now seed categories and articles using the following commands one by one:  
   `make cli seed=categories`  
   then  
   `make cli seed=articles`  

   **Note:** If you encounter any permission-related issues, enter shell mode using `make shell`  
   and run: `chmod +x /app/cli.py`
3.  You're done!  
   Now you can test all APIs using the admin user, or you can create a normal user to test as well. 
   **Note:** Admins can deactivate users, and only *published* posts are searchable.


## 📡 Technical Note

1. I generate `requirements.txt` from `requirements.in` using `pip-tools`.  
   Whenever you update `requirements.txt`, rebuild the project using the `make rebuild` command.

2. For database migrations:  
   First, create your model and make sure to import it in `/model/__init__.py`,  
   then run `make migrate m="your message"`.  
   After that, restart the project using `make restart`.

3. I use `ruff` to format all code.  
   You can run the formatting with: `make ruff-all`

## ✅ Conclusion

This project was built as part of an assessment to demonstrate my understanding of authentication, role-based access control, content management, and AI-powered content analysis.  
It reflects a clean project structure, Dockerized setup, and efficient developer tooling with `Makefile` commands to simplify tasks like seeding, migration, formatting, and rebuilding.

Thank you for reviewing this project!
