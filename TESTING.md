# Testing

+ Passed the code through the PEP8 linter and confirmed there are no problems.
+ Carried out tests of the program on both the local terminal and the Code Institute Heroku terminal.
  
## Manual Testing

### Epic: *Set up a mock-up system to begin with that demonstrates CRUD functionality*

This is broken down into the following User Stories:
US

User Tasks:
1. Right at the onset, deploy the App on Heroku to ensure that works correctly
2. Demonstrate that records can be created
3. Demonstrate that records can be searched for by a reference or by names
4. Demonstrate that records can be edited and updated.
5. Demonstrate that records can be deleted


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
|  T01 | Install Django  | Install Django, psycopg2. Create requirements.txt. Name the Project **manxairlines**. Create the App and name it **booking**. Deployed locally.  | Expected to see the webpage showing the following message: *The install worked successfully!*  | PASS |

<details>
<summary>Screenshot</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9fab1caa-a916-4c8e-a733-0e420a65d671)
  
</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
|  T02 | Heroku Deployment  | Create App on Heroku. Call it **manx-airlines-bookings**. Setup a Database Instance on [ElephantSQL](https://www.elephantsql.com/). Set up the following Heroku Config Vars: <br>1) Copy the generated URL into **DATABASE_URL**; <br>2) Copy Secret Key into **SECRET_KEY**; <br>3) Set **PORT to 8000**; <br>4) Set **DISABLE_COLLECTSTATIC to 1**. <br>Connect Heroku App to GitHub. Deploy.  | Expected to see the webpage showing the following message: *The install worked successfully!* As in the above screenshot. | PASS |

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
|  T03 | Display Home Page  | Set up the relevant Django directories, views and urls to display **index.html**.  | Expect to see the home page with the ubiquitous **Hello World** message. | PASS |

<details>
<summary>Screenshot</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5e82ae15-1dfd-4424-8fef-71d027c6dc3f)


</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
|  T04 | Include 'base.html'  | Update index.html to use **base.html**.<br>It contains H1 Tagged: *HELLO WORLD*. Whilst **index.html** contains  *{% block content %}* of H3 tagged: *GOODBYE!*| Expect to see both sentences:<br>**Hello World** followed by **GOODBYE!** | PASS |

<details>
<summary>Screenshot</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fba9f7f3-008d-48c9-aea0-4dca6f7312a4)

</details>


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
|  T05 | Create Booking  | Create a template and update views.py in order to be able to create a Booking.| In Admin, expect to see a created record. | PASS |

<details>
<summary>Form used to Create a Record</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0e2e9151-74af-401b-a791-bb95c8b220bc)

<summary>Admin Views showing that the Record had been created</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/526f16b7-c657-4a5e-914f-ca5bfd9ec438)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d510ad5b-ccca-4788-b653-2b99a1c660c4)


</details>

----

### Epic: *Create Bookings*

This is broken down into the following User Stories:
US

User Tasks:
1. Demonstrate the forms used to create a booking
2. Show each stage of a Booking being created
3. Demonstrate the validation of the fields entered

   
## Automated Testing
