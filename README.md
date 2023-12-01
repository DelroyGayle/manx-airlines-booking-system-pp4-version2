# Manx Airlines Travel Agent Booking System
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/07ac5c40-4984-43df-9b3a-6c6688723c37)

[View live website](https://manx-airlines-bookings-c1e4c5533a20.herokuapp.com/)

## Table of Contents

1. [Introduction](#introduction)
2. [Glossary](#glossary)
3. [User Stories](#user-stories)
4. [UX - User Experience](#ux-user-experience)
   1. [Wireframes](#wireframes)
   3. [Agile Design](#agile-design)
   3. [Database Design](#database-design)
   4. [Data Models](#data-models)
   5. [Framework](#framework)
5. [Features](#features)
   1. [Home Page](#home-page)
   2. [Create Bookings](#create-bookings)
   3. [Search Bookings](#search-bookings)
   4. [Edit Bookings](#edit-bookings)
   5. [Delete Bookings](#delete-bookings)
   6. Validation and Messages(#validation-messages)
   7. Database Usage(#database-usage)
6. [Technologies Used](#technologies-used)
    1. [Languages](#languages)
    2. [Libraries and Frameworks](#languages-and-frameworks)
7. [Future Features](#future-features)
8. [Testing](#testing)
    1. [Please Go To TESTING.md](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/TESTING.md)
9. [Bugs](#bugs)
     1. [Solved Bugs](#solved-bugs)
10. [Deployment](#deployment)
11. [Credits](#credits)
12. [Acknowledgements](#acknowledgements)

## Introduction

For my Code Institute Portfolio Project 4, 
I would like to implement a Booking/Reservation system<br>so that a Travel Agent<br>can make bookings for passengers to travel with Manx Airlines,<br>with regards to flights between London and the Isle of Man.

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
Here are a sample of some of the terms used:
* OSI - Other Service Information
* PAX - short for Passenger(s)
* PNR - Passenger Name Record
* PRM - Passenger with Reduced Mobility
* SSR - Special Service Request
* STA - Standard Time of Arrival
* STD - Standard Time of Departure
* WCHR - Passenger cannot walk long distances but able to go up and down the aircraft steps
* WCHS - Passenger cannot walk long distances and cannot manage the aircraft steps
* WCHC - Passenger completely immobile, need assistance all the way, to and from the aircraft
* WCLB - Electric wheelchair operated by lithium ion battery
* WCBD - Electric wheelchair operated by a non-spillable ("dry") battery
* WCBW - Electric wheelchair operated by a spillable ("wet") battery
  
----

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

### Framework

I chose to use [Semantic UI](https://semantic-ui.com/) because this framework's approach of using *natural languages like noun/modifier relationships, word order, and plurality to link concepts intuitively*; resonated with me far better as opposed to using abbreviations as seen in frameworks. It also has a great variety of components to choose from when desigining a website. Semantic UI therefore handles the rendering of the webpages of my project on the relevant media whether it be desktop, tablet or mobile. The fonts (e.g. Lato) and colours used come as part of this framework.

## Features

### Home Page

### Create Bookings

Firstly, the user needs to enter the dates of travel and the number of passengers.</br>
**It is mandatory that there is at least one adult passenger on a booking.<br/>
This passenger would be the *Principal Passenger* of the Booking; therefore, cannot be removed from the booking.**<br>
The user enters:
the date of travel
whether it is a return or one-way journey
the number of adults (at least one)
the number of children
the number of infants - *there can only be one infant for each adult*

#### Create a Booking

<details>
<summary>Create a Booking - minimum one adult</summary>
<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ce98c050-33a0-42b1-bf2a-7538d08d0e78)

<br/>
<summary>Return or one-way journey</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ceb8e8b7-e55f-4c96-91a4-a8f6b8064d37)

<summary>Adults, Children and Infants - then Press Continue</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ee9d7b31-7742-49d4-8980-d710a42a6fa7)


</details>

#### Enter Passenger Details

<details>
<summary>Enter the First and Last Name of each passenger</summary>
<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/cf138aa1-45df-4882-bfd0-19374ca50f01)


   For Adult Passengers, there is the option of either Telephone Number or Email Address<br>
   **At least one of these contact details are mandatory for the *Adult 1* Passenger**

<br/>
<summary>Return or one-way journey</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ceb8e8b7-e55f-4c96-91a4-a8f6b8064d37)

<summary>Adults, Children and Infants - then Press Continue</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ee9d7b31-7742-49d4-8980-d710a42a6fa7)


</details>

#### Confirm the Booking

<details>
<summary>A Fare Quote will be generated which needs confirmation - Press Agree and pay now</summary>
<br/>
   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5a11c6ae-2524-4171-971b-46db46f37370)

<summary>Then a message will be displayed that the Booking has been made</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fbc27496-dd50-4c38-b1d7-b9b1eeeb5918)

**Every Booking has its own unique PNR**

Note: the user has the option to *Cancel* proceeding with the Booking
</details>

   ---

### Search Bookings

<details>
<summary>You can search by PNR</summary>
<br/>
   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/28e910ee-8156-433d-af8b-6d5fadcdaa3e)

<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0393c2b9-9763-4f5c-8d75-fee1ad82b15a)

<summary>You can search by the First Name of the Principal Passenger (Adult 1)</summary>

<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/46d99b88-b556-4a2e-94d8-0959e1574eac)

<summary>You can search by the Last Name of the Principal Passenger (Adult 1)</summary>

<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/969d8de0-1f0d-4437-a762-42acbf4e17ad)

<br/>
In the above example, there are nine results - pagination has been incorporated, so that the user can turn to the relevant page<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/1078fea7-e3f0-4ba3-8dfa-c5b08dd553c4)

<br/>

Then the user has to click View to see the Booking
</details>

### View Bookings

<details>
<summary>After a search the user has the option to View the selected Booking</summary>

<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2f551bc8-d144-427a-b219-943931d2bf94)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/bc1f53cb-3b35-4318-8008-1d45945a8e1a)


<br/><br/>
The View shows
1. The Booking's 6-character PNR (Passenger Name Record)
2. The date the Booking was created
3. The flight(s) selected for the Booking

Then the Passengers' Details are shown as follows :-
1. The name of each passenger followed by their status
2.  * The status is of the form HK *\<number\>* - each adult and child passenger would be given their own number
    * Whilst an infant, will have the same status/number of the adult that the infant is assigned to
3. Date of Birth of a Child or Infant Passenger
4. Adult's Passenger's Contact Details
5. Passenger's Wheelchair Details
6. Passenger's Allocated Seat Number (An Infant sits on a passenger's laps i.e. Infants are not allocated seats)
7. Purchased Baggage Allowance
8. Any particular Remarks attached to the Booking
   
Then the user has an option to *Edit* or *Delete* the Booking

</details>

### Edit Bookings

<details>
<summary>All Passenger Details that had been previously entered are now available for editing</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/26711b57-2839-4c08-946e-19be7205dd0d)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/c63757ee-1517-49e6-a407-66db9c141626)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/539ffc70-d06f-4049-9fa3-38db30434be0)


<br/>

That is,
* Title
* First Name
* Last Name
* Contact Telephone Number/Email (for Adult Passengers)
* Date of Birth (for Child and Infant Passengers)
* Wheelchair Details
* Baggage Allowance
* Remarks

**All *changes to/editing of* details (*except for wheelchair*) are subject to fees**<br>
The fees are
* GBP 20.00 each - for changes to a passenger's details
* GBP 30.00 for each extra bag purchased
* Some changes subject to GBP20.00 Admin fee
* If for example it is solely the passenger's wheelchair details that are changed the fee will be *GBP0.00*
<br/><br/>


<summary>Removal of Passengers</summary>

During Editing, Passengers can be removed from a Booking</br>(All *except* the Principal Passenger - **Adult 1** - the checkbox is both *disabled and hidden*)

Removal is done by clicking the Passenger's checkbox labelled **Remove Pax?**

When a passenger is selected for removal, a visual indicator of *red strike-through* of the name of the passenger is displayed

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/26bc6266-7bd9-4202-974e-1966f008cef2)

<summary>Removal of Adult and Infant</summary>

When a Booking is made, each infant is attached to a corresponding adult i.e.
1. One infant is attached to one passenger - *Adult 1 and Infant 1*
2. Two infants are attached to two adults - *Adult 1 and Infant 1, Adult 2 and Infant 2*
3. Three infants are attached to three adults - *Adult 1 and Infant 1, Adult 2 and Infant 2, Adult 3 and Infant 3*
4. etc.

So if the user *selects* an Adult to be removed the corresponding Infant is automatically *selected* e.g.

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/28e2e2f8-3412-4f9f-a814-9fef119cf159)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/1db170f7-0821-4c4d-acd0-cccb147d5704)

In like manner, if the Adult is *deselected* the corresponding Infant would be automatically *deselected* as well.

<summary>Removal of Individual Passengers</summary>summary>

That said, any individual passenger can be selected for removal from a booking e.g.
* The Infant travelling with Adult 1 can be removed without affecting Adult 1
  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5e1c6ee7-719f-4b4d-9b4e-e73d5b3128ce)

* Any individual Adult, Child or Infant can be selected by clicking its corresponding checkbox for removal

The user then presses *Continue* to proceed with any edit changes

</details>

#### Another Example

<details>

<summary>Remove the infant David Smith from this booking and add two bags and remarks</summary>

<br>   

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d6906169-2234-475a-9c61-6f739dcf8c96)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/58ad761b-786f-4bd9-b6c8-fce81ef610aa)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d805d213-b7b9-4fb5-94d0-a6ca99253485)

</details>

#### Confirm the Changes

<details>
<summary>Change Fees will be generated which needs confirmation - Press Agree and pay now</summary>
<br/>

Using the example above: **Booking CGF64F**

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/bb80a957-0962-460d-a661-8159dab32a13)

<summary>Then a message will be displayed that the Booking has been updated</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3caaa321-3b28-4ed9-a600-38270ca06439)

Note: the user has the option to *Cancel* changes

Now when the user views **Booking CGF64F** the user can see that *David Smith* has been removed. Moreover, baggage and remarks have been added to the booking

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f3340e60-f067-45c8-b221-4c0515b6939a)

</details>
  
### Delete Bookings

<details>
<summary>When viewing a Booking the user has the option to delete the Booking</summary>
<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f3340e60-f067-45c8-b221-4c0515b6939a)

<summary>The user is prompted to confirm whether the user would like to proceed with the deletion - the option is present to Cancel</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/23661f04-e21e-4f9b-9175-4baa2f666f52)

<summary>If the user presses Yes, a message will be displayed to confirm that the Booking has been deleted</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/00806c8d-dd4a-4761-a166-f5c0a78a8e42)

</details>

-----

### Validation and Messages

### Database Usage
------

## Technologies Used

### Languages
* [HTML5](https://en.wikipedia.org/wiki/HTML)
* [CSS3](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
  
### Libraries and Frameworks

* [Django](https://www.djangoproject.com/)   
    * Django was used as the web framework.
* [Semantic UI](https://semantic-ui.com/  
    * Semantic UI was used the design, styling and responsiveness of this website.
* [Cloudinary](https://cloudinary.com/)
    * Cloudinary was used for image management.

#### Other tools and frameworks

* [GitHub](https://github.com/) - for hosting the site
* [Gitpod](https://www.gitpod.io/) - for editing the files
* [Heroku](https://heroku.com) - for the deployment of the site
* [Jquery](https://jquery.com/) - for scripting purposes
* [Balsamiq:](https://balsamiq.com/) was used to create the wireframes
* [DrawSQL](https://drawsql.app/) was used to draw the SQL tables
* [Am I Responsive](http://ami.responsivedesign.is/) was used for creating the multi-device mock-up shown at the top of this README.md file
* [Tiny PNG](https://tinypng.com/) was used to reduce the file size of the background image
* [Code Institute's GitHub full template](https://github.com/Code-Institute-Org/python-essentials-template) - in order to run Django and Python on Heroku


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

#### 'Create Booking' Django Form

The fields appeared too long with the *help text* being shown adjacent to the fields as opposed to below the fields<br/>
However, there is a way of <em>overriding the default action of <strong>forms.as_p</strong></em>

<details>
<summary>Before this fix:</summary>
<br/><br/>  

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/05badf93-e91d-4c3d-9bdc-d0d1706f8fa1)

</details>

I found this solution at [Stack Overflow](https://stackoverflow.com/questions/7769805/editing-django-form-as-p )

I prefer this look:

<details>
<summary>After this fix:</summary>
<br/><br/>  
   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/49e3cb2a-307c-42e4-93b0-27c836ffccb0)


</details>

#### Footer at the Bottom of the Page

The Footer would not 'stay' at the bottom of the page depending on the view.
I did not want a **sticky** footer.</br>
I found this solution at [Stack Overflow](https://stackoverflow.com/questions/34250019/footer-semantic-ui)

<details>
<summary>Footer stays at the bottom of the page</summary>
<br/><br/>  

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b487677e-4a24-4c71-85f0-d01775c7e850)

</details>



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
+ I visited the websites of [BA](https://www.britishairways.com/travel/home/public/en_gb/)'s and [EasyJet](https://www.easyjet.com/en) to get an idea of layout the forms and the phraseology of error messages
+ The Isle of Man Logo was downloaded from [icon-icons](https://icon-icons.com/icon/isle-of-man/17195) - *Free for personal use*
+ The background image I used is courtesy of London City Airport
+ Used [Stack Overflow](https://stackoverflow.com/) to investigate various solutions especially
   + [Editing Django _form.as_p](https://stackoverflow.com/questions/7769805/editing-django-form-as-p)
   + [How to Validate an Email Address in Django?](https://stackoverflow.com/questions/3217682/how-to-validate-an-email-address-in-django)
   + [How can I compare a Date and a Datetime in Python?](https://stackoverflow.com/questions/3278999/how-can-i-compare-a-date-and-a-datetime-in-python)
   + [Pythonic difference between two dates in years?](https://stackoverflow.com/questions/4436957/pythonic-difference-between-two-dates-in-years)
   + [Execute document.ready even if user came to the page by hitting the back button](https://stackoverflow.com/questions/11871253/execute-document-ready-even-if-user-came-to-the-page-by-hitting-the-back-button)
        
## Acknowledgements
+ Cryce Truly's excellent tutorial [Python Django Web Framework](https://www.youtube.com/playlist?list=PLx-q4INfd95ESFMQ1Je3Z0gFdQLhrEuY7)
   + I used his approach as the layout for this project.
+ CodingEntrepreneurs' excellent tutorial [Try DJANGO Tutorial Series](https://www.youtube.com/playlist?list=PLEsfXFp6DpzTD1BD1aWNxS2Ep06vIkaeW) 
   + Very thorough explanations!
+ Tutor Support for their speedy help during this project especially John and Oisin.
+ Many thanks to my mentor Derek McAuley for his technical expertise and guidance.

