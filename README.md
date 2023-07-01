# Customer Management
This is a Django web application that allows customer to register and login to maintain their profile

## Installation

Follow these steps to install and run the Django app:

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username//CustomerInformation.git
   ```
2. Navigate to the project directory:
   ```shell
   cd CustomerManagement

   ```
3. Install Poetry:
   ```shell
      pip install poetry

   ```
4. The environment related file .env file needs to configured for the below secrets . Please note the values are sample
   ```shell
   SECRET_KEY="django-insecure-^@_7wm(f#*bo^x83ziowrg-c7iljj8bdin&&1d!cml_ie%5%gd"
   ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1
   DATABASE_NAME="CustomerManagement"
   DB_USER=postgres
   
   DB_PASSWORD=Vinod
   
   HOST="localhost"
   PORT="5433"
   ```
5. Apply the database migrations:
   ```shell
   poetry run python manage.py migrate
   
   ```
## Usage
To run the Django app locally, execute the following command:
   ```shell
   poetry run python manage.py runserver
   
   ```
The app will be accessible at http://localhost:8000.

## For Building Docker and Run
1. Build the Docker image:
   ```shell
   DOCKER_BUILDKIT=1 docker  build -t customer-management:latest --platform linux/amd64 .
   ```
2. Run the Docker container:
```shell
   docker run  8000:8000 customer-management
```