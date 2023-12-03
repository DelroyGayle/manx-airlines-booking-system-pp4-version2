# Testing

## HTML Validation
This was performed using [W3C HTML Validator](https://validator.w3.org/nu/)

* There were confilcts with the validator and Django Template Language, for example

* Spaces following % produced "Non-space characters found without seeing a doctype first."

* Besides these conflicts I changed all my <article>'s and <section>'s to <div>'s

* Warning: The type attribute is unnecessary for JavaScript resources.

## CSS Validation

This was performed using [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)

 - No issues flagged during CSS validation

## JavaScript Validation

This was performed using [JSHint](https://jshint.com/)

- infantsCheck is not unused since it is needed in ...templates/booking/create-booking-form.html

 ## Python Validation

This was performed using Code Institute's [PEP8 Linter](https://pep8ci.herokuapp.com/)

- No issues flagged during JS validation

## Lighthouse

I used Lighthouse within the Chrome Developer Tools to test the performance, accessibility and SEO of the website.
This test was performed before the authentication profile was added.

<details>
  <summary>Lighthouse Report</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/09b1697c-a33e-42ee-b9f4-9dcf1fa07283)

</details>

## Additional Testing Comments
+ Carried out tests of the program on both the local terminal and the Code Institute Heroku terminal.
+ Chrome DevTools was used throughout the development process for testing purposes.
+ Added Custom [404](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/templates/includes/404_not_found.html) and [500](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/templates/includes/500_error.html) pages just in case such errors occur.
  
## Manual Testing - Mock Employer App to begin with

### Epic: *Set up a mock-up system to begin with that demonstrates CRUD functionality*

This is broken down into the following

<details>
  <summary>User Stories</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a542b30f-f782-4cf1-a2b2-c8fdfa597f5c)

</details>

**User Tasks:**
1. Right at the onset, deploy the App on Heroku to ensure that it runs correctly on Heroku
2. Demonstrate that records can be created
3. Demonstrate that records can be searched for by a reference or by names
4. Demonstrate that records can be edited and updated.
5. Demonstrate that records can be deleted


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T01 | Install Django  | Install Django, psycopg2. Create requirements.txt. Name the Project **manxairlines**. Create the App and name it **booking**. Deploy locally. | Expected to see the webpage showing the following message: *The install worked successfully!* | PASS |

<details>
<summary>Screenshot</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9fab1caa-a916-4c8e-a733-0e420a65d671)
  
</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T02 | Heroku Deployment  | Create App on Heroku. Call it **manx-airlines-bookings**. Setup a Database Instance on [ElephantSQL](https://www.elephantsql.com/). Set up the following Heroku Config Vars: <br>1) Copy the generated URL into **DATABASE_URL**; <br>2) Copy Secret Key into **SECRET_KEY**; <br>3) Set **PORT to 8000**; <br>4) Set **DISABLE_COLLECTSTATIC to 1**. <br>Connect Heroku App to GitHub. Deploy. | Expected to see the webpage showing the following message: *The install worked successfully!* As in the above screenshot. | PASS |

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T03 | Display Home Page  | Set up the relevant Django directories, views and urls to display **index.html**. | Expect to see the home page with the ubiquitous **Hello World** message. | PASS |

<details>
<summary>Screenshot</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5e82ae15-1dfd-4424-8fef-71d027c6dc3f)

</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T04 | Include 'base.html' | Update index.html to use **base.html**.<br>It contains H1 Tagged: *HELLO WORLD*. Whilst **index.html** contains  *{% block content %}* of H3 tagged: *GOODBYE!* | Expect to see both sentences:<br>**Hello World** followed by **GOODBYE!** | PASS |

<details>
<summary>Screenshot</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fba9f7f3-008d-48c9-aea0-4dca6f7312a4)

</details>


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T05 | Create Booking | Create a template and update views.py in order to be able to create a Booking.| In Admin, expect to see a created record. | PASS |

<details>
<summary>Form used to Create a Mock Record</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0e2e9151-74af-401b-a791-bb95c8b220bc)

<summary>Admin Views showing that the Record had been created</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/526f16b7-c657-4a5e-914f-ca5bfd9ec438)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d510ad5b-ccca-4788-b653-2b99a1c660c4)

</details>

----

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T06 | Search Bookings | Create a Searchbar in order to be able to search for created bookings. Searches are *case insensitive*. | Expect to see matching records or a message showing that no matching criteria found. | PASS |

<details>
<summary>Searchbar - Demonstrate when no matching records found</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/bee4f3f5-abcc-4959-b767-cd5067f5294f)

</details>

<details>
<summary>Demonstrate when search text "wa" is entered - case insensitive - three matches found</summary>
  
  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2bc24dc8-5c36-41b8-b98a-d94af6e71cf8)

</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T07 | View Bookings | Once a Booking has been found, view the Booking. | Click the View Button to see a matched record. | PASS |

<details>
  <summary>View Waterstons record by clicking the View button. Showing the Edit and Delete options</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a4a584fd-6e97-4fa7-8294-297a28fd8c6f)

</details>


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T08 | Delete Bookings | Implement the functionality to delete a record. Give the user the option to cancel the 'Delete' command. | Click the Yes Button to delete a record . | PASS |

<details>
  <summary>Showing Yes/Cancel options</summary> 

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/8e9b2c0c-4789-47a8-a075-adff7f57fd51)

  <summary>Record deleted - originally three records, now two</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5a5a41e4-026d-41aa-8111-230e4239f7e7)

  <summary>Delete the other two - confirm that there are no further records that match "wa"</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/c357e514-2256-48f9-9101-083a353c51f4)

</details>

----

## Manual Testing of the Manx Airlines Travel Agency Booking System

### Epic: *Create Bookings*

This is broken down into the following
<details>
  <summary>User Stories</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d02560ce-863d-46e5-b13d-90082efb77a5)

</details>

User Tasks:
1. Implement Navbar with Isle of Man Logo
2. Demonstrate the forms used to create a booking
3. Show each stage of a Booking being created
4. Demonstrate the validation of the fields entered

<details>
  <summary>Navbar</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/94f86cd6-17c0-4488-8ca5-39fbb4525f7c)

</details>


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T09 | Create Booking | Create a Booking with 3 PAX, bags and remarks.| Confirmation Form regarding Booking | PASS |

<details>
 
  <summary>Creating a Booking - First Page - Flight Details and Number of PAX</summary>
  
  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9f48c63f-af8e-4134-8791-52535c96d320)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/16b90e4e-9128-4a74-824f-16038e4b5006)

<summary>Creating a Booking - Second Page - Enter Passenger Details - Adult, Child, Infant, Bags and Remarks</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fad66edc-fc39-44dd-b4fe-0e45d6057dbc)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/27d2220d-4974-4d98-8fdc-a1eb34321906)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ae233a53-3a3e-4060-b47b-8f3f8eea0dd5)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/daa38270-6e9a-4718-a774-8fcc08bc95cb)

</details>


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T10 | Confirm Booking | Make a Booking then Click *Agree and pay now* | Booking created. In Admin, expect to see all the records created by this action. | PASS |

<details>

<summary>Confirmation Form of the Booking being made</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f8d0031a-dd58-42f6-9584-e402022d3a85)

<summary>Success Message showing that the Booking has been made</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a79e7ee2-c7c5-4b34-935b-bb81e9c3d80c)

</details>

Admin View of the Booking and Passengers Records

<details>
<summary>Admin view of the Booking record</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/564be75a-8a37-40e2-8a91-d8e4635dee82)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/6878835d-b191-4fad-b0b0-e9b02b349b1e)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/74d78d46-02bc-4d7c-86ce-2793b3cf3693)

<summary>Admin view of the Passenger records</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/dd51e2ec-69a8-4180-ac45-24d54ea32fdf)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3cccbf1a-ea40-4707-a9d4-52fea8efa175)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/81fbecbe-2bdb-4a83-8468-d4e8d9720fd6)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/69ce8b19-454c-489d-95e5-4fc5e5c99f9d)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/49d3efc2-f1ad-429c-a5e0-aa56a49a02ef)

</details>

Admin View of the Transaction and Schedule Records
<details>
<summary>Admin view of the Transaction record</summary>

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a5779787-cbfc-4a00-9918-9c93c3dea426)

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f423230d-be3f-4ae3-b110-896e01373d22)

<summary>Admin view of the Schedule records and Seatmaps</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/82969fd2-b940-44c4-b06d-b38cecd698f7)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a0d21ac1-e688-41e4-9ceb-31400fba1ab4)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ecd0b996-860a-4ac2-81a6-b73302a7881c)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/cb95778e-79b2-4b14-be24-c71f7b2e124c)

</details>


---


