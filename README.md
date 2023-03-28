# Paxxo-Oils-Manager

Paxxo Oils is a Django project that includes an app and an API for managing customer enquiries about the company's products and services. The app allows anyone to submit an enquiry from the comfort of their home, and the admin can login to check and respond to messages.

## Features
The Paxxo Oils app includes the following features:

- Enquiry submission form: Customers can submit enquiries about the company's products and services by filling out a form in the app.
- Admin login: The admin can log in to the app to view, reply to, and delete messages submitted by customers.
- Email notifications: When a customer submits an enquiry, the admin receives an email notification with the details of the enquiry. When the admin responds to the enquiry, the customer receives an email notification with the admin's response.

# Installation
To install the project, follow these steps:

1. Clone the repository
2. Install the dependencies by running pip install -r requirements.txt
3. Create a .env file and add your environment variables
4. Run migrations with python manage.py migrate
5. Start the server with python manage.py runserver


## Usage

Once the server is running, you can access the web application at http://127.0.0.1 and the API at http://127.0.0.1/api/.

Use the registration form to submit resumes as a student, and login as an admin or staff member to access the relevant panels. Staff members can only access approved resumes and can send emails to selected candidates.


### To use app

```sh
docker-compose -f docker-compose-deploy.yml build
```

### To start app

```sh
docker-compose -f docker-compose-deploy.yml up
```