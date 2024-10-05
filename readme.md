# Zelf Hackathon Backend 🚀

Welcome to the second exciting adventure of the Zelf Hackathon! You've made it through the selection process, impressing us with your experience and expertise—congratulations on making it to the top! 🎉

But now, the real challenge begins. 💻 This is the final step in the hackathon journey, where your skills will be put to the ultimate test. Think of it as the start of an exhilarating quest 🏞️, where every decision, every line of code you write could unlock new possibilities and set the stage for something amazing at Zelf. 🔑

Your adventure starts now—let’s see what you’re made of! 💪 Good luck! 🍀


## Instructions

### 🚀 Setting up the containers and environment
- Clone this repository to your local machine.
- Ensure that Docker and Docker Compose are installed and ready to use. 🐳
- Start the Docker containers by running the docker-compose.yaml file.
- Go to the following web [HackAPI](https://hackapi.hellozelf.com/login/?next=/home/) and create an account

### 🛠️ Initialize the Django project

- Migrate the Django models to set up your database schema.


### 🌱 Export the Seed Data

Download the SQL data dump file and import it into the database.

- Seed SQL File: [Google Drive](https://drive.google.com/file/d/1KPg0kk6B_b7kR1qpZ58Q7wgR2rsuzW7A/view?usp=sharing)


1. Before downloading the sql file, run the docker compose to start the container 
```shell
docker-compose up -d --build
```
2. Now run the migrations
```shell
docker-compose exec app python /src/manage.py migrate
```
3. Download the sql file in the following directory
> /db/data/<sqlfile.sql>

4. Open the db container shell
```shell
docker-compose exec db sh 
```
5. Run the sql file
```shell
psql -d contentapi -U django -f /var/lib/postgresql/data/<downloaded sql file.sql>
```

Now, you’re all set! 🎉

##  Tasks
### Task 1: Code Review and Refactoring ⚙️

Navigate through the contents app and review the TODO comments to get an understanding of the pending tasks. Your goal is to refactor and optimize the code for better performance and maintainability.


`Refactor models.py`: 🗂️ Review and optimize the models, ensuring they are normalized and structured to efficiently handle the required API use cases. Consider creative solutions to enhance performance and speed. 🚀

`Refactor views.py`: 📑 Refactor the API implementations in views.py as per the TODO comments. Make necessary adjustments to streamline and optimize the APIs for better efficiency and scalability. ⚡

`Fix tasks.py`: 🛠️ Investigate the Celery task in tasks.py that is not running properly. Identify the issue, implement the necessary fixes, and ensure smooth task execution. 🌀
The given task continuously grabs content from ContentAPI [API Docs](https://www.postman.com/hellozelf/workspace/zelf-hackathon-backend/request/22135478-2cd2a12e-9e3e-4cc5-98e8-6628c40a0522?action=share&source=copy-link&creator=22135478&ctx=documentation)
This api is open, it has no restriction.


### Task 2: Implement the third party api

First Go through the documentation of this api. 

[HackAPI Docs](https://www.postman.com/hellozelf/workspace/zelf-hackathon-backend/collection/22135478-b612fc0d-d351-4deb-ae8a-ac9a92e2aa77?action=share&creator=22135478)

Gist of the task: 
1. Create a system where it will continuously pull AIGenerated comment from the api, but make sure not to get rate limit error. 
2. After storing the AIGenerated Comments use these `ai generated comment` to post the comment using the `Comment Posting` api.
3. The Comment posting api has a rate limit, you can only post one comment per 30 seconds. 

Now design and write an elegant system, with less error and fallback options. 

#### Details:

> Part 1 - The Pull

An automated system to pull `AIGeneratedComment` from the api, (See docs [Docs](https://www.postman.com/hellozelf/workspace/zelf-hackathon-backend/request/22135478-3c29af00-5b13-451e-8262-b5285d39b338?action=share&source=copy-link&creator=22135478&ctx=documentation))
Always pull comments for the most recent contents.

> Part 2 - The Push

After getting the ai generated comments, send the content and the comment for comment push operation.

## To Do:

1. You will only be able to post 1 comment per 30 seconds. so make your design in that way.
2. If you face Errors like
 - `Something went wrong`
 - `Service Unavailable'
Then retry for another 2-3 times.

3. If you face errors like
- `This content is not availalbe for commenting` then do not retry

4. Make an api ( Post Request ), that will trigger comment posting, make sure to add authentication middleware. 
Only authenticated users can trigger comments posting