# Manx Airlines Travel Agent Booking System

[Live Link]

## Introduction

For my Code Institute Portfolio Project 4, 
I would like to implement a Booking/Reservation system so that a Travel Agent<br>can make a booking for passengers to travel with Manx Airlines,<br> with regards to flights between London and the Isle of Man.

Manx Airlines offer three flights everyday.

The Daily Flight Schedules are:

**London City Airport TO Douglas, Isle of Man - LCYIOM**
| Flight | Time of Departure | Time of Arrival |
| -------| -----------       | --------------- |
| XM465	| 08:00 | 9:45 |
| XM475	| 13:30 | 15:15 |
| XM485	| 18:30 | 20:15 |


**Douglas, Isle of Man TO London City Airport to  - IOMLCY**
| Flight | Time of Departure | Time of Arrival |
| -------| -----------       | --------------- |
| XM466	| 11:00 | 12:45 |
| XM476	| 16:00 | 17:45 |
| XM486	| 21:00 | 22:45 |

## User Stories

* As a **Site User** I want the navigation to be user-friendly so that I can easily create and amend bookings corrsponding to passengers' requests.
* As a **Site User** I can register, log-in and log-out from the website 
* As a **Site User** I can log in using my email and password so that I can access the system and make bookings 
* As a **Site User** I can **create a new bookings** by providing **Passenger Name(s) and Contact Details
* As a **Site User** I can optionally add the date of birth if Passenger is a child or infant.
* As a **Site User** I can optionally add whether Passenger(s) require bags and any special requirements such as wheelchairs
* As a **Site User** I can add a note to the Booking in reqards to any special requests required by the Passenger(s)
* As a **Site User** I can view bookings that have been made by myself or other users.
* As a **Site User** I can **edit bookings** that I have made** in regards to Passenger details such as Name, Contact Details, Number of Bags, Date of Birth
* As a **Site User** I can **delete bookings that I have made** when a booking is no longer applicable. For example, Passenger is no longer travelling or new parties need to be added
* As a **Site User** I can see the fees in regards to making a new booking
* As a **Site User** I can see the fees in regards to any amendments to the a booking

------

## UX

### Design

#### Home Page

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/24858511-6621-45e3-b1be-22c54d4c74a3)

#### Initial Create Booking Page

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/674a8c24-8e04-41a9-a6b9-4ab4c72e169d)



------

## Features

------

## Limitations

## Future Features
* Be able to add new passengers to an existing booking
* Be able to *change* passenger type e.g. *Adult to Child, Child to Infant, Child to Adult* and vice versa

------

## Data Model

### SQL Tables

![drawSQL-teamdg2-export-2023-10-19](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f52a38a1-2872-4f57-ad89-7546896e2f9c)

## Modules

## Testing

+ Passed the code through the PEP8 linter and confirmed there are no problems.
+ Carried out tests of the program on both the local terminal and the Code Institute Heroku terminal.

### Internal Errors

## Code Validation

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

## Languages, Libraries and Technologies

### Languages
* Python3

### Python Libraries

* os - I use this library for the *clear* function in order to clear the console before displaying an updated chessboard.
* re - I use *regular expressions* in order to validate user input of chess moves.
* time - I use the *sleep* function to cause the program to delay for a few seconds, in order so that the user can see the updated chessboard.

### Other tools

* [GitHub](https://github.com/) - for hosting the site
* [Gitpod](https://www.gitpod.io/) - for editing the files
* [Heroku](https://heroku.com) - for the deployment of the site
* [Code Institute's GitHub full template](https://github.com/Code-Institute-Org/python-essentials-template) - in order to run Python on Heroku

------

## Credits

+ [Flowchart Fun](https://flowchart.fun/) 
+ [Miro](https://miro.com/)
+ [drawSQL](https://drawsql.app/) was used to draw the SQL tables
        
## Acknowledgements    
