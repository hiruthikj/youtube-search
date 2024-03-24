# Youtube Search API
Run background task to fetch Recent Youtube Videos on a topic and exposes a paginated API to search it

# Setup
1. Create .env from .example.env and fill in the CONNECTION_STR (use postgres) and GOOGLE_DEVELOPER_KEY for calling youtube API
2. Install docker-compose and run `docker-compose up --build`

# Endpoints
* Refer Docs http://localhost:8089/docs

# Sidenote
* Runs jobs async in background
* Swagger Docs, pre-commit hooks

# Future Plans
* Add full text search
* Configurable Search Query in Background Job
* Multiple Developer Keys
* Make API Call to Youtube API async
