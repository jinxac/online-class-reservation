# online-class-reservation
APIs to reserve and confirm booking of an online class. Includes an API for
listing the available classes, an API to reserve a seat in a selected class and confirm the
reservation.


Considerations
1. Each class will have a limited number of seats. This value will be stored in the DB.
2. Once the user reserves a seat, the reservation will be held for 5 mins. The user must
confirm his/ her reservation within 5 mins.
3. Develop a simple scheduler to keep track of reservations.
4. The user should receive an OTP or confirmation link via email.
5. Logging of API requests and responses where necessary.


### Features
  1. `GET /api/v0/classes/`


    Returns list of classes available. The possible filters are start date, type of class, status and page number.
    The filters can be passed as query parameters.

  2. `POST /api/v0/classes/`

    Create a new class

  3. `PUT /api/v0/classes/:class_id/`

    Update the class.

  4. `DELETE /api/v0/classes/:class_id/`

    Deletes a class.

  5. `POST /api/v0/classes/reserve-seat/`

    The required fields here are `class_id` and `user_id`. This reserves seat and
    sends an otp in the email.
    Example Payload:

    ```
      {
        class_id: 1,
        user_id: 1
      }
    ```
  6. `POST /api/v0/classes/confirm-seat/`

    The required fields here are `class_id` and `user_id`. This confirms the class seat
    Example Payload:


      {
        class_id: 1,
        user_id: 1
      }

  7. `POST /api/v0/classes/cancel-seat/`


   The required fields here are `class_id` and `user_id`. This cancels the class seat.
   Example Payload:

    {
      class_id: 1,
      user_id: 1
    }

  8. `POST /api/v0/report/`


    Returns a JSON with Total number of classes, Total number of users enrolled,
    Number of confirmed seats per class, Number of active classes,  Number of upcoming
    classes, Number of classes completed
  ### Steps

   1. `virtualvenv venv`
   2. `source venv/bin/activate`
   3. `Create a file in location /var/log/online_class/app/app.log` with suitable permissions for logging
   4. `pip install -r requirements.txt`
   5. `python -m scripts.init_db`
   6. `python manage.py runserver`