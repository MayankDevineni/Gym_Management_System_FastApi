Gym Management System (FastAPI Backend)

Overview
This project is a backend system built using FastAPI to simulate a real-world gym management service. It provides APIs for managing gym plans, memberships, and class bookings with proper validation and business logic.

Features

Core Features

* RESTful API development using FastAPI
* Pydantic validation for request data
* CRUD operations for gym plans
* Membership enrollment system
* Class booking system with eligibility checks
* Automatic membership fee calculation with discounts and charges

Business Logic

* Duration-based discounts (10% for 6 months, 20% for 12 months)
* Referral discount (5%)
* EMI processing fee
* Discount breakdown included in response
* Plan deletion restricted if active members exist
* Class booking allowed only for eligible members
* Membership freeze and reactivate functionality

Advanced Features

* Search plans by keyword
* Filter plans based on price, duration, classes, and trainer
* Sort plans by price, name, and duration
* Pagination support
* Combined browsing endpoint with search, filter, sort, and pagination

Project Structure

fastapi-gym-management-system/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/

Setup and Run Instructions

Clone the Repository
git clone https://github.com/MayankDevineni/Gym_Management_System_FastApi
cd Gym_Management_System_FastApi

Create Virtual Environment
python -m venv venv

Activate environment

Windows
venv\Scripts\activate

Mac/Linux
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Run the Server
uvicorn main:app --reload

API Base URL
http://127.0.0.1:8000

API Documentation
http://127.0.0.1:8000/docs

API Overview

Plans

* Get all plans
* Get plan by ID
* Create new plan
* Update plan
* Delete plan

Memberships

* Create membership
* Get all memberships
* Freeze membership
* Reactivate membership
* Search memberships
* Sort memberships
* Paginate memberships

Classes

* Book class
* Get all bookings
* Cancel booking

Advanced Endpoints

* /plans/search
* /plans/filter
* /plans/sort
* /plans/page
* /plans/browse

Screenshots
All API endpoints have been tested using Swagger UI. Screenshots are available in the screenshots folder.

Future Enhancements

* AI chatbot integration
* Authentication system (JWT)
* Notification system
* Frontend dashboard

Author
Mayank Devineni
