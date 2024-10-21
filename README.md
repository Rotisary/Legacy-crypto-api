This API was created to offer backend features such as user management, user authentication, wallet seed phrase storage and fund transfer for a crypto site.
It also interacts with CoinMarketCap's API to get prices of various cryptocurrencies and display them to the user.

It is fairly simple to integrate with the API, just follow the steps below:

User Creation and Management

  - To create an account, enter values for the fields below:
      
         {
            "email": "tester@gmail.com",
            "username": "tester",
            "name": "site tester",
            "password": "tst@01cr",
            "password2":"tst@01cr"
         }

      
  After entering values for the fields above, make a POST request to https://olumoroti.pythonanywhere.com/users/register/

  An example response is

    {
      "respone": "successfully registered user",
      "email": "tester@gmail.com",
      "username": "tester",
      "name": "site tester",
      "token": <generated token>
    }

  *Always remember to set the content-type header of the request being made to "application/json"

  *Take note of the generated token as it will be needed to authorize the requests that users will make to the API 

  - After an account has been created, users can log in by entering their email and password;

        {
            "email": "tester@gmail.com", 
            "password": "tst@01cr"
        }

  And then make a POST request to https://olumoroti.pythonanywhere.com/users/login/

  This is what your response would look like

      {
        "response": "Successfully Authenticated",
        "pk": 3,
        "email": "tester@gmail.com",
        "token": <generated token>
    }

- To get a response containing the details of a user, users should make a GET request to https://olumoroti.pythonanywhere.com/users/details/{username}/

You would get a response that looks like this

    {
        "user_id": <generated user id>,
        "email": "tester@gmail.com",
        "username": "tester",
        "name": "site tester"
    }

- To update user details, add the fields you want to update to your request's body and make a PUT request to https://olumoroti.pythonanywhere.com/users/details/{username}/update/

Note that only the email, username and name can be updated

*Always remember to add user's token to the request's header. Also set the content-type to "application/json" whenever a POST or PUT request is made

      headers = {
          "Authorization": "Token <generated token>",
          "Content-Type": "application/json"
      }

- After a user has been created, they get a profile that contains their wallet's seed phrase and shows their account balance.

  To access a user's profile, make a GET request to https://olumoroti.pythonanywhere.com/users/profile/{profile slug}/

  Response

      {
        "user": "https://olumoroti.pythonanywhere.com/users/details/tester/",
        "slug": tester-3
        "balance": 1200,
        "wallet": "https://olumoroti.pythonanywhere.com/users/wallet/{wallet slug}/"
      }

  - If a user wants to delete their account, make a DELETE request to https://olumoroti.pythonanywhere.com/users/{username}/delete/
 
  - To change a user's password, add the fields below to the body of the request
 
        {
          "old_password": <user's old password>,
          "password": <user's new password>,
          "confirm_password": <user's new password>
        }

    After the fields have been added, make a PUT request to https://olumoroti.pythonanywhere.com/change-password/

Wallets

  - To add a new wallet, add the fields below to the body of the request

        {
          "seed_phrase": "<user's wallet's seed phrase>",
          "external_wallet": "<the name of the external wallet provider e.g Trustwallet>"
        }

   After the fields have been added, make a POST request to https://olumoroti.pythonanywhere.com/users/add-wallet/

   Be sure to add the token of the user the wallet is being created for

   Response

        {
            "slug": "{wallet slug}",
            "seed_phrase": "<wallet seed phrase>",
            "owner": "https://olumoroti.pythonanywhere.com/users/profile/{profile slug}/"
        }

   *Note that when trying to add the seed_phrase field in your code, each word contained in the seed_phrase should be separated by an underscore(_).
   If they are not separated by an underscore, the wallet won't be saved

  - To get a user's wallet details, make a GET request to  https://olumoroti.pythonanywhere.com/users/wallet/{wallet slug}/

  Response

        {
            "slug": "{wallet slug}",
            "seed_phrase": "<wallet seed phrase>",
            "owner": "https://olumoroti.pythonanywhere.com/users/profile/{profile slug}/"
        }

- To delete a wallet, make a DELETE reqest to https://olumoroti.pythonanywhere.com/users/wallet/{username}/delete/

Funds

- To send funds to a user, add the amount field to the request's body

        {
            "amount": <the amount to be sent>
        }

  After the field has been added, make a POST request to  https://olumoroti.pythonanywhere.com/users/send-fund/{username}/ (the username needs to be the username of the user the money is being sent to)

  Response

      {
        "url": "https://olumoroti.pythonanywhere.com/users/fund/{id}/",
        "amount": <the amount that was sent>,
        "owner": "https://olumoroti.pythonanywhere.com/users/profile/{id}/",
        "created_at": "date and time when the fund was sent"
      }

- To get a fund's detail, make a GET request to https://olumoroti.pythonanywhere.com/users/fund/{id}/

  Response
  
        {
          "url": "https://olumoroti.pythonanywhere.com/users/fund/{id}/",
          "amount": <the amount that was sent>,
          "owner": "https://olumoroti.pythonanywhere.com/users/profile/{id}/",
          "created_at": "date and time when the fund was sent"
        }

- To get fund transfer history, make a GET request to https://olumoroti.pythonanywhere.com/users/funds/history/

  Response

      {
        "count": 7,
        "next": "https://olumoroti.pythonanywhere.com/users/funds/history/?page=2",
        "previous": null,
        "results": [
            {
                "url": "https://olumoroti.pythonanywhere.com/users/fund/{id}/",
                "amount": 1000,
                "owner": "https://olumoroti.pythonanywhere.com/users/profile/{id}/",
                "created_at": "2024-10-05T20:22:49.784479Z"
            },
            {
                "url": "https://olumoroti.pythonanywhere.com/users/fund/{id}/",
                "amount": 400,
                "owner": "https://olumoroti.pythonanywhere.com/users/profile/{id}/",
                "created_at": "2024-10-01T15:32:20.954002Z"
            },
        ]
      }

  *Note that the funds history response is paginated with a page size of 5, the link to the next page can be gotten from the "next" field in the response

  - The list can be filtered by the amount that was transferred or the name of the recipient.
    To do this, add a query parameter called "search" to the url and set it to the value you want to filter by

    The url should look like this https://olumoroti.pythonanywhere.com/users/funds/history/?search={amount or name to filter by}

Crypto

- To get the price of a cryptocurrency, make a GET request to https://olumoroti.pythonanywhere.com/crypto/price/?symbol={the symbol of the cryptocurrency}

  *the symbol is the abbreviation of the name of the cryptocurrency("BTC" for bitcoin, "USDT" for tether USD e.t.c)

  Response

      {
        "name": "<name of cryptocurrency>",
        "symbol": "<the cryptocurrency symbol>",
        "price": <the price of the cryptocurrency>
      }

*The Authorization header must be added to all requests made except when making requests to the user registration and log in endpoints

*The Content-Type header must be added when making requests to POST and PUT endpoints and must be set to "application/json"
