# Manx Airlines Travel Agent Booking System

[View live website]

## Table of Contents

1. [Introduction](#introduction)
2. [Glossary](#glossary)
3. [User Stories](#user-stories)
4. [UX - User Experience](#ux-user-experience)
   1. [Wireframes](#wireframes)
   3. [Agile Design](#agile-design)
   3. [Database Design](#database-design)
   4. [Data Models](#data-models)
5. [Features](#features)
   1. [Home Page](#home-page)
   2. [Create Bookings](#create-bookings)
   3. [Search Bookings](#search-bookings)
   4. [Edit Bookings](#edit-bookings)
   5. [Delete Bookings](#delete-bookings)
6. [Technologies Used](#technologies-used)
    1. [Languages](#languages)
    2. [Libraries and Frameworks](#languages-and-frameworks)
7. [Future Features](#future-features)
8. [Testing](#testing)
    1. [Please Go To TESTING.md](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/TESTING.md)
9. [Bugs](#bugs)
     1. [Known Bugs](#known-bugs)
     2. [Solved Bugs](#solved-bugs)
10. [Deployment](#deployment)
11. [Credits](#credits)
12. [Acknowledgements](#acknowledgements)

## Introduction

For my Code Institute Portfolio Project 4, 
I would like to implement a Booking/Reservation system so that a Travel Agent<br>can make a booking for passengers to travel with Manx Airlines, with regards to flights between London and the Isle of Man.

Throughout the travel industry, travel agents uses GDS ( [Global Distribution Systems](https://www.travelperk.com/corporate-travel-glossary/global-distribution-system/) ) and travel reservation system such as [Amadeus](https://amadeus.com/en/portfolio/hospitality/crs-central-reservation-system), [Galileo](https://en.wikipedia.org/wiki/Galileo_GDS) and [Sabre](https://en.wikipedia.org/wiki/Sabre_(travel_reservation_system)) in order to create travel bookings for passengers.

So my project is an attempt to create a *toy travel reservation/booking system* for a fictitious airline called **Manx Airlines**.<br>
Manx Airlines offer three flights everyday to the Isle of Man and vice versa.

The Daily Flight Schedules are:

**London City Airport TO Douglas, Isle of Man - LCYIOM**
| Flight | Time of Departure | Time of Arrival |
| -------| -----------       | --------------- |
| MX465	| 08:00 | 9:45 |
| MX475	| 13:30 | 15:15 |
| MX485	| 18:30 | 20:15 |


**Douglas, Isle of Man TO London City Airport to  - IOMLCY**
| Flight | Time of Departure | Time of Arrival |
| -------| -----------       | --------------- |
| MX466	| 11:00 | 12:45 |
| MX476	| 16:00 | 17:45 |
| MX486	| 21:00 | 22:45 |

## Glossary

Throughout this document I will be using typical airline terminology when referring to certain concepts.
Here are a sample of some of the terms used
* PAX - Short for Passenger(s)
* PRM - Passenger with Reduced Mobility
* WCHR
* WCHS
* WCHC
* WCMP
* WCLB
  
***

## User Stories

* As **Developer** I can **set up the workspace** so that **I can implement the necessary tools and start writing the code**

* As a **Developer** I can **set up a Mock Django Application** so that **I can test CRUD functionality before creating the Main App**

* As a **Developer** I can **set up a Mock Django Application** so that **I can test Search and View functionality**

* As a **Site User** I can **use the NavBar** so that **I have the option to Create and Search for Bookings**

* As a **Site User** I can **see a list of bookings** so that **I can select the one that I want to view or amend**

* As a **Site User** I can **create a booking** so that **I can make a booking for a passenger's flight**

* As a **Site User** I can **click on a booking view button** so that **I can view the full text of the booking**

* As a **Site User** I can **edit a booking** so that **I can make amendments as requested by a passenger**

* As a **Site User** I can **delete a booking** so that **I can cancel a passenger's proposed journey**

* As a **Site User** I can **add children to a booking** so that **children can be included with an adult on a flight**

* As a **Site User** I can **add an infant to a booking** so that **an infant can be included with an adult on a flight**

* As a **Site User / Admin** I can **Register, Login and Logout** so that **I can access and manage my account**

* As a **Site User / Admin** I can **amend my profile** so that **I can change my password**

------

## UX - User Experience

### Wireframes

<details>
<summary>Home Page - Create a new Booking or Enter an Existing Booking</summary>
<br/><br/>  

   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/24858511-6621-45e3-b1be-22c54d4c74a3)
</details>

<details>
<summary>Select Page for Flights' Date, Time and the Number of Passengers</summary>
<br/><br/>  

   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/dcb436d3-7314-4976-9132-6a1f872883a1)
</details>

<details>
<summary>Passenger Selection Summary Page</summary>
<br/><br/>  

   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/785e3fd8-ffdb-4e8b-a2f7-ad31d33abb71)
</details>

<details>
<summary>Sample of Entering Passenger(s) Details - Top of the Page</summary>
<br/><br/>  

   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/8bfd91ae-957e-4610-a7b6-9909c56b36db)
</details>

<details>
<summary>Sample of Entering Passenger(s) Details - Bottom of the Page</summary>
<br/><br/>  

   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/500cd571-e484-47b5-a722-4d3d56c17de1)
</details>


<details>
<summary>Supplementary Details Page</summary>
This Page is used so that the User can enter Contact and PRM details<br>
(PRM - Passenger with Reduced Mobility)
<br/><br/>  

   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b06afda9-46fd-4b46-a041-2014a39f254f)
</details>

<details>
<summary>Booking Review Page</summary>
<br/><br/>  

    
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2d0f303d-bf18-4977-9c9d-152c7df1d250)
</details>

<details>
<summary>Home Page</summary>
User has entered "DAX" - shows any matching Booking Refs with this Prefix<br>
User then can select which Booking Ref they would like to View
<br/><br/>  

   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2b735f8f-860e-4000-bbba-3f934e6ca3ff)
</details>

<details>
<summary>View Page - The User has the option to Edit or Delete the Booking</summary>
<br/><br/>  

   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9dfd9785-3294-4922-ae8c-a0d6b1af0a28)
</details>


<details>
<summary>Edit Page</summary>
The User can amend details such as name, contact details and number of bags, etc<br>
There is a checkbox supplied in order for the option to <i>remove a passenger from the booking</i><br>
When the User selects this checkbox - the passenger details are striked-out<br>to indicate that the passenger will be removed from the Booking after the User's confirmation
<br/><br/>  

   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/6c97ce8f-0629-4e5b-8c50-08322dc17f97)
</details>

------

### Agile Design

Agile Kanban Board</summary>

<details>
At the start of this project this is how the Kanban Board looked 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f4c23961-19b6-4172-bcc0-4d764d394567)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/4e94438d-35db-4a0e-8319-ba0138a18afd)

</details>

Epics, User Stories and their related Tasks are further explained in [TESTING.md](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/TESTING.md)

### Database Design

<details>
<summary>Mockup Database Schema</summary>
<br/><br/>  


![drawSQL-teamdg2-export-2023-10-23](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/bad6685a-cc79-4dc5-92ea-b057cee7a9d6)
</details>

----

### Data Models

## Features

### Home Page

### Create Bookings
### Search Bookings
### Edit Bookings
### Delete Bookings

------

## Technologies Used

### Languages
* Python3

### Libraries and Frameworks

#### Other tools and frameworks

* [GitHub](https://github.com/) - for hosting the site
* [Gitpod](https://www.gitpod.io/) - for editing the files
* [Heroku](https://heroku.com) - for the deployment of the site
* [Code Institute's GitHub full template](https://github.com/Code-Institute-Org/python-essentials-template) - in order to run Python on Heroku

------

## Future Features
* Be able to add new passengers to an existing booking
* Be able to *change* passenger type e.g. *Adult to Child, Child to Infant, Child to Adult* and vice versa

### Limitations

## Testing

Please refer to [TESTING.md](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/TESTING.md)


### Internal Errors

## Code Validation

------

## Bugs

### Solved Bugs


------

## Deployment

The project is deployed on Heroku. These are the steps in order to deploy on Heroku:
1. Regarding your project:
    + create a Procfile with the following one line entry
    ```
    web: node index.js
    ```

2. Then ensure that you have pushed your latest version including Procfile to GitHub

3. Create a Heroku account. You will need to enter 
* first name
* last name
* email address,  
* role e.g. *student*
* location
* primary development language i.e. *Python*

4. Click *Create free account*

5. Proceed with confirmation via email

6. Log into Heroku

7. Create a new application by clicking the *Create New App* button.<br>
You will need to enter
* The *App name*
* The region
* Then click the *Create app* button

8. Go into settings -> Config Var and add the following:
    +  key by the name of *PORT* with the value of *8000*.<p>

9. The next step is to add a couple of  buildpacks to your application.<br>Then click the *Add buildpack* button

10. Include the following buildpacks:
    + The first buildpack is *heroku/python* - then click "Save changes"
    + The second buildpack is *heroku/nodejs* - then click "Save changes"
    + Please note: the order is significant - the Python buildpack **must** appear on top before the NodeJs buildpack.<br>One can use the mouse to drag the buildpacks into the correct order<p>

11. Then click the *Deploy* option. This is where you choose the deployment method of *GitHub*

12. Find the repo with the project you want to deploy

13. Confirm that you want to connect to GitHub by clicking the *Connect* button

14. Scroll down to the two options, *Automatic deploys - Manual deploy*

15. In this section, you can click *Enable Automatic deploys* - Heroku will rebuild your app every time you push a new change  
to your code to GitHub

16. Or you can choose to *manually deploy* using the *Deploy Branch* option here 

17. Pick which branch you want to deploy -- Generally this would be **main**

18. Click **Deploy Branch** and wait until the project is built

19. Ensure there are no errors. Heroku will display the message **Your app was successfully deployed**

20. Click the *View* button and you will be taken to an URL of the form *https:\/\/\<project-name>.herokuapp.com/*<br>
This is your deployed app in operation


## Credits

+ [drawSQL](https://drawsql.app/) was used to draw the SQL tables
        
## Acknowledgements    


