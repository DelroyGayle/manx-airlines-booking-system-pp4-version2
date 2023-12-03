# Manx Airlines Travel Agent Booking System
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/07ac5c40-4984-43df-9b3a-6c6688723c37)

[View live website](https://manx-airlines-bookings-c1e4c5533a20.herokuapp.com/)

## Table of Contents

1. [Introduction](#introduction)
2. [Glossary](#glossary)
3. [User Stories](#user-stories)
4. [UX-User Experience](#ux-user-experience)
   1. [Wireframes](#wireframes)
   3. [Agile Design](#agile-design)
   3. [Database Design](#database-design)
   4. [Data Models](#data-models)
   5. [Framework](#framework)
5. [Features](#features)
   1. [Airline Criteria](#airline-criteria)
   2. [Background Image](#background-image)
   3. [NavBar](#navbar)
   4. [Home Page](#home-page)
   5. [Create Bookings](#create-bookings)
   6. [Search Bookings](#search-bookings)
   7. [Edit Bookings](#edit-bookings)
   8. [Delete Bookings](#delete-bookings)
   9. [Validation and Messages](#validation-and-messages)
   10. [Registration](#registration)
   11. [LogIn/LogOut](#loginlogout)

   
6. [Technologies Used](#technologies-used)
    1. [Languages](#languages)
    2. [Libraries and Frameworks](#libraries-and-frameworks)
7. [Future Features](#future-features)
8. [Testing](#testing)
    1. [Please Go To TESTING.md](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/TESTING.md)
9. [Bugs](#bugs)
     1. [Solved Bugs](#solved-bugs)
     2. [Known Bugs](#known-bugs)
10. [Deployment](#deployment)
11. [Credits](#credits)
12. [Acknowledgements](#acknowledgements)

## Introduction

For my Code Institute Portfolio Project 4, 
I would like to implement a Booking/Reservation system<br>so that a Travel Agent<br>can make bookings for passengers to travel with Manx Airlines,<br>with regards to flights between London and the Isle of Man.

Throughout the travel industry, travel agents use GDS ( [Global Distribution Systems](https://www.travelperk.com/corporate-travel-glossary/global-distribution-system/) ) and travel reservation systems such as [Amadeus](https://amadeus.com/en/portfolio/hospitality/crs-central-reservation-system), [Galileo](https://en.wikipedia.org/wiki/Galileo_GDS) and [Sabre](https://en.wikipedia.org/wiki/Sabre_(travel_reservation_system)) in order to create travel bookings for passengers.

So, my project is an attempt to create a *toy travel reservation/booking system*<br/> for a fictitious airline called **Manx Airlines**.<br>
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
* INS - Infant On Seat
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
* WCMP - Manual operated wheelchair
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

------

## UX-User Experience

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

The site uses a Back-end database with the usage of ElephantSQL Postgres for the deployed site
<details>
<summary>Database Schema Diagram</summary>
<br/><br/>  

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fd990e02-df99-49f2-a8cf-c8856a337583)



</details>

----

### Data Models

The following data models were designed to represent the database usage for this project

#### User Model

The User Model contains information about the user. It is based upon Django's in-built authentication system
- username
- email
- password

#### Flight Model

This model contains the available Flight Routing offered by Manx Airlines
 - flight_number = CharField(6 characters, Primary Key) e.g. **MX0465**
 - flight_from = CharField(3 characters) e.g. **LCY**
 - flight_to = CharField(3 characters) e.g. **IOM**
 - flight_STD = CharField(4 characters) - Standard Time of Departure e.g. **0800**
 - flight_STA = CharField(4 characters) - Standard Time of Arrival e.g. **0945**
 - outbound = BooleanField(default=True) - **True** means a *Return* journey; **False** means a *One-way* journey
 - capacity = PositiveSmallIntegerField - represents the aircraft passenger capacity
 - - for this project, the capacity is **96**

#### Schedule Model

This model contains each scheduled flight as per Booking
- flight_date = DateTimeField
- flight_number = CharField(6 characters) e.g. **MX0465**
- total_booked = PositiveSmallIntegerField - the number of passengers booked for this schedule
- seatmap = CharField(24 characters)
- - the seatmap of the aircraft is represented by a *96-bit-string* which in turn is  represented as a *24-character hex-string*
- - see [TESTING.md](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/TESTING.md) further details

#### Booking Model

This model contains all the Bookings that are made by the user according to passengers' requests
- pnr = CharField(6 characters, unique=True) - Passenger Name Record
- created_at = DateField(auto_now=True)
- amended_at = DateField(auto_now_add=True)
- flight_from = CharField(3 characters) e.g. **LCY**
- flight_to = CharField(3 characters) e.g. **IOM**
- return_flight = BooleanField(default=True) - **True** means a *Return* journey; **False** means a *One-way* journey
- outbound_date = DateField
- outbound_flightno = CharField(6 characters) e.g. **MX0475**
- inbound_date = DateField
- inbound_flightno = CharField(6 characters) e.g. **MX0486**
- fare_quote = DecimalField(max_digits=6, decimal_places=2, default=0) - the actual price of the Booking
- ticket_class = CharField(max_length=1, default="Y") - always **Y** for economy
- cabin_class = CharField(max_length=1, default="Y") - always **Y** for economy
- number_of_adults = PositiveSmallIntegerField - the number of adults in the Booking
- number_of_children = PositiveSmallIntegerField - the number of children in the Booking
- number_of_infants = PositiveSmallIntegerField - the number of infants in the Booking
- number_of_bags = PositiveSmallIntegerField - baggage allowance as requested by the passenger
- departure_time = CharField(4 characters) - Standard Time of Departure e.g. **0800**
- arrival_time = CharField((4 characters) - Standard Time of Departure e.g. **0945**
- remarks = TextField - Remarks and SSRs added to the Booking

#### Passenger Model

This model contains each individual Passenger Details
- title = CharField(4 characters) - MR, MRS, MISS, etc
- first_name = CharField(40 characters)
- last_name = CharField(40 characters)
- pax_type = CharField(1 character, default="A") - **A=Adult C=Child I=Infant**
- pax_number = PositiveSmallIntegerField - The passenger number within the Booking
- - i.e. 1st passenger is 1, 2nd is 2, etc
- date_of_birth = DateField - **applicable to Children and Infants only**
- contact_number = CharField(40 characters)
- contact_email = CharField(40 characters)
- -  Either one of these two fields must be initialised for **Adult No. 1**
- -  For the other passengers, these fields are optional
- pnr = (ForeignKey - Booking) - Passenger Name Record
- outbound_seat_number = CharField(3 characters) - e.g. **24A, 24B, 24C, 24D, ...**
- - Passengers are allocated seats from the back of the aircraft onwards
- - That is, from *Row 24* onwards to *Row 1* - **96 seat capacity**
- inbound_seat_number = CharField(3 characters) - e.g. **1A, 1B, 1C, 1D, ...**
- status = CharField(4 characters)
- - HK1 for PAX 1, HK2 for PAX 2, etc., up to HK20
- - that is a maximum of 20 seated passengers per Booking
- - An Infant has the same status number as their accompanying Adult
- wheelchair_ssr = CharField(1 character) - Optional Wheelchair Information
- - That is, is this passenger a PRM?
- - *Blank for No, R for WCHR, S for WCHS, C for WCHC*
- wheelchair_type = CharField(1 character) - Optional Accompanying Wheelchair Information
- - Is this passenger travelling with their **own** wheelchair? If so, what type of wheelchair is it?
- - *Blank for No, M for WCMP, L for WCLB, D for WCBD, W for WCBW*

#### Transaction Model

This model contains all the fees and charges that the user has made<br/>
Such as the cost of the flight, extra baggage, editing changes
- pnr = CharField(6 characters) - Passenger Name Record
- amount = DecimalField(max_digits=6, decimal_places=2, default=0)
- date_created = DateField(auto_now=True)
- username = models.CharField(40 characters)

### Framework

I chose to use [Semantic UI](https://semantic-ui.com/) because of this framework's approach of using *natural languages like noun/modifier relationships, word order, and plurality to link concepts intuitively*. This approach resonated with me far better as opposed to using abbreviations as seen in other frameworks. Semantic UI also has a great variety of components to choose from when designing a website. Semantic UI therefore handles the rendering of the webpages of my project on the relevant media whether it be desktop, tablet or mobile. The fonts (e.g. Lato) and colours used come as part of this framework.

## Features

### Airline Criteria 

#### Infant Passengers Criteria
In the Airline Travel Industry, all airlines generally adhere to the following criteria regarding Infant Passengers :-

1. Infants are defined as passengers who are under 2 years of age.
2. There cannot be more infants on a booking than adults. That is, *one infant per one adult passenger*.
3. Infants must be seated on the adult's lap. That is, infants are not allocated seats.
4. If the passenger desires the infant to have their own seat - this seat must be purchased as a INS booking - Infant On Seat
   * For Manx Airlines, this means the user must enter the infant *as a **Child** in the Booking.*
5. If at the time of the *return flight* the infant would be **aged 2 years or above** then the infant must be booked *as a **Child***
   * For Manx Airlines, this means the user must enter the infant *as a **Child** in the Booking.* 

#### Criteria specific to Manx Airlines 
1. A maximum of 20 seated passengers are allowed per Booking. That is, both Adults and Children.
2. Which in turn means, a maximum of 20 infants are allowed per Booking.
3. A **Child** Passenger is defined as a passenger who is at least **2 years of age and under 16 years of age**.
4. The Departure Date cannot be made more than 180 days in the future from the date that the Booking was created.
5. A maximum interval of 180 days is allowed between the Departure Date and the Return Date.
6. The Return Time cannot be less than **90 minutes** from the Departure Time.
7. The Booking **must** contain at least **one Adult Passenger.** No Child nor Infant can travel on Manx Airlines without an Adult Passenger.
8. The First Passenger in the Booking *Adult 1* is designated as **the Principal Passenger of the Booking**.<br/>
   * As such, this passenger is a mandatory part of the booking and cannot be removed.
   * If for example, the passenger does need to be *removed* from the booking, then that booking needs to be **deleted** and a **new** booking altogether needs to be made.
   * However, *Adult 1's* name  can be edited with regards to a name of a new passenger.
9. An Infant Passenger must be at least 14 days old to travel.

### Fees

What follows are the fees regarding travelling with **Manx Airlines**
This application generates quotes according to these fees.

#### Create Booking Fees
| Passenger Type     | Age Group | Fee |
| ------------- | ------------- |------------- | 
| Adults | Age 16+ | £100 |
| Children | Age 2-15 | £60 |
| Infants | Age < 2 | £30 |
| | **Other Fees** | |
| Bags | | £30 |

- Please note: the price of a bag (£30) is the same regardless of whether a return or one-way journey.
- However, the passenger prices are for each *leg* of the journey, regardless of whether adult, child or infant.
- For example, 
- One adult on a return flight - the cost would be £200 - with a bag - £230
- One-way journey - £100 - with a bag - £130
- One adult and child on a return flight - the cost would be £320 - with a bag - £350
- One-way journey - £160 - with a bag - £190



#### Edit Booking Fees
| Edit    |  Fee |
| ------------- | ------------- |
| Passengers Details| £20 per passenger |
| Extra Bags | £30 each |
| Admin Fee | £20 | 
| Wheelchair Details | £0

**All *changes to/editing of* passenger details (*except for wheelchair*) are subject to fees**<br>
* If for example it is solely the passenger's wheelchair details that are changed the fee will be *GBP0.00*

All fees and charges made by this App are recorded in the Transaction database in order for an Audit Trail to be created.<br>Every transaction record contains: the date the transaction was made, the Booking PNR, the amount and the 'user name'.
  
### Background Image
Some of the images of the Features shown may differ slightly since the *Background Image* was added later on.

<details>
   <summary>
      The Background Image
   </summary>

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/93dd67af-1574-4704-a9b2-134e7b8e0f8f)

</details>

### NavBar

The navigation menu bar only shows up for logged in users.<br/>
From this point onwards, the user has the options to Create or Search for Bookings.<br/>
On the far left is **the Logo for the Isle of Man**.<br/>

<details>
   <summary>The Isle of Man Logo</summary>

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/929f5f14-552b-41c9-91bd-d9f0c4eef6b2)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fe5c4512-0e74-44ab-8809-0c7d22197e3a)


</details>

The logo acts as a *Home Button*. By clicking the logo, the user is returned to the Home Page.<br/>
On the far right is the option to Log Out.

If a user is not logged in the user will not be able to process any bookings! <br/>None of the above options will appear to a user who is not logged in.

<details>
   <summary>Navigation Bar</summary>

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/4d467cbb-4834-4399-a3a3-c9860e573ebe)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/c9a313c7-9e7a-4171-9aee-1bd223a915c4)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/93177538-fcca-45a3-b665-e5428859ae8f)

</details>

### Home Page

* The Home Page opens up with a *Welcome* from **Manx Airlines** directing the user to use the Navigation Menu Bar.
* The Footer Text serves as a reminder for the user to inform any potential passengers/customers that *fees are non-refundable, etc.*
* **The Logo for the Isle of Man** on the far left is the Home Button.  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2dd6f21b-1c8f-44f1-95fd-b3f8b9a6591d)
* Followed by the option to **Create Bookings**.
* Followed by the **Search Box**.
* The First Mentioned Passenger in a Booking is the *Principal Passenger*.

The search box enables users to search for Bookings by either 
1. The PNR - Passenger Name Record.
2. The Principal Passenger's First Name.
3. The Principal Passenger's Last Name.

In order to retrieve any Booking for *Viewing and Updating* the user must *Search* for the Booking using the designated Search Box.
<details>
   <summary>
      Home Page
   </summary>

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2f263ea9-80d1-4392-ae07-dd390d5fbfec)


</details>

### Create Bookings

Firstly, the user needs to enter the dates of travel and the number of passengers.</br>
**It is mandatory that there is at least one adult passenger in a booking.** <br/>
This passenger would be the *Principal Passenger* of the Booking; therefore, this passenger cannot be removed from the booking.**<br>

The user enters:
* the date of travel
* whether it is a return or one-way journey
* the number of adults (at least one)
* the number of children
* the number of infants - *there can only be one infant for each adult*

#### Create a Booking

<details>
<summary>Create a Booking - minimum one adult</summary>
<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ce98c050-33a0-42b1-bf2a-7538d08d0e78)

<br/>
<summary>Return or one-way journey</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ceb8e8b7-e55f-4c96-91a4-a8f6b8064d37)

<summary>Adults, Children and Infants - then click Continue</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ee9d7b31-7742-49d4-8980-d710a42a6fa7)


</details>

#### Enter Passenger Details

   For Adult Passengers, there is the option of either Telephone Number or Email Address<br>
   **At least one of these contact details are mandatory for the *Adult 1* Passenger** <br>
   Whilst for a Child or Infant Passenger, the Date of Birth needs to be entered

<details>
<summary>Enter the First and Last Name of each passenger</summary>
<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/cf138aa1-45df-4882-bfd0-19374ca50f01)

<br/>
<summary>Return or one-way journey</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ceb8e8b7-e55f-4c96-91a4-a8f6b8064d37)

<summary>Adults, Children and Infants - then click Continue</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ee9d7b31-7742-49d4-8980-d710a42a6fa7)

<summary>Wheelchair Information of a PRM</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5c461a66-db48-4389-b3b7-d7ebad6bab42)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/836cf440-3dc8-4287-868f-2b77917fc2ed)


</details>

#### Confirm the Booking

**Every Booking has its own unique PNR**

Note: the user has the option to *Cancel* proceeding with the Booking

<details>
<summary>A Fare Quote will be generated which needs confirmation - click Agree and pay now</summary>
<br/>
   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5a11c6ae-2524-4171-971b-46db46f37370)

<summary>Then a message will be displayed that the Booking has been made</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fbc27496-dd50-4c38-b1d7-b9b1eeeb5918)

</details>

   ---

### Search Bookings

Note: the Search option is *case-insensitive* <br>
Once the user has searched for the relevant booking, the user then has to click *View* to see the Booking

<details>
<summary>The user can search by PNR</summary>
<br/>
   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/28e910ee-8156-433d-af8b-6d5fadcdaa3e)

<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0393c2b9-9763-4f5c-8d75-fee1ad82b15a)

<summary>The user can search by the First Name of the Principal Passenger (Adult 1)</summary>

<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/46d99b88-b556-4a2e-94d8-0959e1574eac)

<summary>The user can search by the Last Name of the Principal Passenger (Adult 1)</summary>

<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/969d8de0-1f0d-4437-a762-42acbf4e17ad)

<br/>
In the above example, there are nine results - pagination has been incorporated, so that the user can turn to the relevant page<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/1078fea7-e3f0-4ba3-8dfa-c5b08dd553c4)

<br/>

Then the user has to click View to see the Booking
</details>

### View Bookings

The View shows
1. The Booking's 6-character PNR (Passenger Name Record)
2. The date the Booking was created
3. The flight(s) selected for the Booking - showing the dates

Then the Passengers' Details are shown as follows :-
1. The name of each passenger followed by their status
2.  * The status is of the form HK *\<number\>* - each adult and child passenger would be given their own number
    * Whilst an infant, will have the same status/number of the adult that the infant is assigned to
    * Passenger Type is shown as: **ADULT, CHILD or INFANT**
3. Date of Birth of a Child or Infant Passenger
4. Adult Passenger's Contact Details
5. Passenger's Allocated Seat Number(s) (An Infant sits on a passenger's laps i.e. Infants are not allocated seats)
6. Passenger's Wheelchair SSRs (Optional)
7. Purchased Baggage Allowance (Optional)
8. Any Remarks attached to the Booking (Optional)
   
Then the user has an option to *Edit* or *Delete* the Booking


<details>
<summary>View the selected Booking</summary>

<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2f551bc8-d144-427a-b219-943931d2bf94)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/bc1f53cb-3b35-4318-8008-1d45945a8e1a)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/876c50f4-1e8a-4004-87f3-564e21e4a079)

<br/><br/>

</details>

### Edit Bookings

All Passenger Details that had been previously entered are now available for editing

That is,
* Title
* First Name
* Last Name
* Contact Telephone Number/Email (for Adult Passengers)
* Date of Birth (for Child and Infant Passengers)
* Wheelchair Details
* Baggage Allowance
* Remarks

There is also the option to **remove a passenger** from the booking.<br/>This applies to all passengers *except for Adult 1* - *the Principal Pax* <br/>
(Note: **Adult 1** - the checkbox is both *disabled and hidden*)

**All *changes to/editing of* details (*except for wheelchair details*) are subject to fees.** <br/>
These fees also apply to the **removing of passengers** from the booking.<br/>
The fees are
* GBP 20.00 each - for changes to a passenger's details or removal of passenger
* GBP 30.00 for each extra bag purchased
* Some changes are subject to GBP20.00 Admin fee
* If for example it is solely the passenger's wheelchair details that are changed the fee will be *GBP0.00*
<br/><br/>


<details>
<summary>Edit Passenger Details</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/26711b57-2839-4c08-946e-19be7205dd0d)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/c63757ee-1517-49e6-a407-66db9c141626)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/539ffc70-d06f-4049-9fa3-38db30434be0)


<br/>

<summary>Removal of a Passenger</summary>

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

The user then clicks *Continue* to proceed with any edit changes

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

Change Fees will be generated which needs confirmation - click Agree and pay now

Note: the user has the option to *Cancel* changes

<details>
<summary>Change Fees will be generated which needs confirmation - click Agree and pay now</summary>
<br/>

Using the example above: **Booking CGF64F**

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/bb80a957-0962-460d-a661-8159dab32a13)

<summary>Then a message will be displayed that the Booking has been updated</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3caaa321-3b28-4ed9-a600-38270ca06439)

Now when the user views **Booking CGF64F** the user can see that *David Smith* has been removed. Moreover, baggage and remarks have been added to the booking

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f3340e60-f067-45c8-b221-4c0515b6939a)

</details>
  
### Delete Bookings

When viewing a Booking the user has the option to delete the Booking <br>
If the user clicks Yes, a message will be displayed to confirm that the Booking has been deleted <br>
Note: the user has the option to Cancel


<details>
<summary>When viewing a Booking the user has the option to delete the Booking</summary>
<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f3340e60-f067-45c8-b221-4c0515b6939a)

<summary>The user is prompted to confirm whether the user would like to proceed with the deletion - the option is present to Cancel</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/23661f04-e21e-4f9b-9175-4baa2f666f52)

<summary>If the user clicks Yes, a message will be displayed to confirm that the Booking has been deleted</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/00806c8d-dd4a-4761-a166-f5c0a78a8e42)

</details>

-----

### Validation and Messages

Validation is applied throughout the process of entering Booking and Passenger Details. Suitable messages, based on *Django Messaging system*, are displayed to guide the user accordingly.

#### Creating Bookings

<details>
   
<summary>Entering Past Dates</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/895384ff-32e5-4e5b-9956-d9f686ce9241)

<br/> 

Note: The same validation is applied to the *Returning Date*

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/c5ba3fe4-94bf-42db-b9ad-9210310dad08)


<summary>Illegal Dates</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/cfd46e5f-c44c-4d59-833a-b9087dbe2be2)

<summary>Same Day Return Journey - entering an earlier Return Time than the Departure Time e.g. 13:30pm and 11:00am</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fa80a9d7-0a96-475f-8a5f-e74f56810113)

   
<summary>Attempt to make a Booking with an interval of more than 180 days</summary>
<br/> 

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/10d838cf-a5c6-4069-aeb1-dac28771edce)

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0fa112c4-b722-44ca-b3a1-3f809c6b0e76)

<summary>Attempt to make a Booking too far into the future</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/4fde0e59-0cea-49c3-9737-a607c88ffe46)

<br/> 

<summary>Same Day Return Journey - The Return Time cannot be less than 90 minutes from the Departure Time e.g. 09:45am and 11:00am</summary>
<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/39d819b1-895e-4e27-97ec-0ef187d0b8e8)

</details>

#### Entering Passenger Details

<details>

   <summary>Attempt to add more infants than the number of adults</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/82522b91-5583-49c4-ad98-806712e280b0)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ef338adb-c6cc-4eb7-90e8-13e390864a07)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/eed0ff1d-c609-431c-afd2-644bd056f042)

   <summary>Zero number of Adults</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b3ae4c55-a2a8-45c6-bdff-969d1def16b3)

   <summary>Attempt to make a Child Booking with Zero Adults</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/8a552933-547d-4b97-84c8-5c858848404e)

   <summary>Attempt to enter more than 20 passengers in a booking </summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/dc5d8842-0fb0-42cf-8f1a-fba229ed6a02)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/317f579f-3749-4121-9348-7478a7e27dfb)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/31ce0552-ee93-438a-9ec4-e963c8833b5a)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2b2f222e-b654-455f-b471-6918b012992d)






 <summary>Entering a Blank Form or Blank Passenger Details</summary>
<br/> 

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/80992d59-a8a6-4527-88f2-5b9382359725)

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2aa78b99-9b8f-453d-9cb9-c07751b32f50)



<summary>Blank First Name</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9e137e6c-c89e-49a3-bc9c-a5cf29a4355e)

<summary>Blank Last Name</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/832b9aa2-d680-40d9-aff9-4c6f4842dce9)

<summary>Names must consist only of Letters, Apostrophes and Hyphens</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/e0f1fa9d-ca8a-4c9e-97ca-d6c85087f3e7)

<br/> 
<summary>Email Validation</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5900ed07-693b-4fa9-9af1-82cc71285d7c)

   <summary>Principal Passenger (Adult 1) Contact Details must be entered</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/1f6dcea1-e58d-4b35-bde6-aa0e1214659f)

   

   <summary>Erroneous Telephone Numbers</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b25fb09e-1d56-4dc0-99d0-3b3aaa3e72fb)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9e894431-939b-47be-a836-b520d02b48f8)


</details>

 #### Date of Birth Validation

<details>
   
 <summary>Future Date</summary>
<br/> 

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0fb63bf6-0349-42ee-b48d-e3752e0dc507)

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/e5e0ddad-05f1-485f-8e17-c641bd8aa264)


 <summary>Date of Birth cannot be Today's Date e.g.</summary>
<br/> 

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ef65f84a-1db9-4639-875d-64dce3916c1b)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a35b78ad-de90-4a91-9008-42fbe152668a)

   <summary>An Infant Passenger must be at least 14 days old to travel e.g. for the 19/11/2023</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/59ecaf0a-3049-4307-b37f-bb06134dbe03)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d60aa11b-6784-4996-88aa-4c4ef33f85e4)

   <summary>An Infant Passenger must be under 2 years of age at the time of the Departure Date of Travel e.g. for the 04/12/2023</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ad52263e-4074-4b12-9c33-00629f67822e)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/944fb559-bdb2-4ea3-8674-97df103b955d)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b2743b4d-36bb-4772-ab05-c19847e7b5dc)


<summary>An Infant Passenger must be under 2 years of age at the time of the Return Date of Travel e.g. for the 16/12/2023</summary>
<br/> 
   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/685a043b-f4b2-4343-8482-151ecc8bf46e)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/88c86db2-8764-4d9a-9601-35dff073b536)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a7e2cc9a-121a-4559-a4e7-f7a8003237d5)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/109dabe6-428e-40e4-ac2d-897178663591)

<summary>A Child Passenger must be under 16 years of age  at the time of the Departure Date of Travel e.g. for the 04/12/2023</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/7f0d29ca-8c32-4ec3-a87e-f75a54397c6e)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/15ba523d-ea89-4f27-9647-3d858e0edf8f)

<summary>A Child Passenger must be under 16 years at the time of the Return Date of Travel e.g. for the 24/11/2023</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b7ce3e44-db40-4e8b-9a38-37194b7026d5)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9bd59f1b-39b0-400d-8ee5-1edd4f917d8b)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/6bc4a6d7-f0bc-4bb8-b043-bb0cfe3b2798)


   </details>


------

### Registration

* In order for a user to be able to create, read, edit and delete bookings, the user will need to register on the site.
* Registration is based upon the Django's built-in authentication system.
* When the user registers the user will get a success message to confirm.

<details>
   <summary>Registration Form</summary>

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3e4c437e-711e-45c6-b1d4-094ee8e0aa72)

   <summary>Successful Registration</summary>

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/40f6a3ac-c663-4bd2-b7b4-d9e5a112f1e6)


</details>

### LogIn/LogOut

* In order for a user to be able to create, read, edit and delete bookings, the user will need to <br/>log into the App using their username and password.
* LogIn/LogOut is based upon the Django's built-in authentication system.
* When the user logs in, the Home Page will appear to the user.
* When the user logs out, the user will get a success message to confirm.

<details>
   <summary>Login Form</summary>

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/75fd5aff-c389-4cc9-a17c-46049e92df60)


   <summary>Successful Log Out</summary>

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/971ea8e7-e6ff-408e-ac18-20b4786ffef4)



</details>


## Technologies Used

### Languages
* [HTML5](https://en.wikipedia.org/wiki/HTML)
* [CSS3](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
  
### Libraries and Frameworks

* [Django](https://www.djangoproject.com/)   
    * Django was used as the web framework.
* [Semantic UI](https://semantic-ui.com/)
    * Semantic UI was used for the design, styling and responsiveness of the website.
* [Cloudinary](https://cloudinary.com/)
    * Cloudinary was used for image management.

#### Other tools and frameworks

* [GitHub](https://github.com/) for hosting the site
* [Gitpod](https://www.gitpod.io/) for editing the files
* [Heroku](https://heroku.com) for the deployment of the site
* [Jquery](https://jquery.com/) for scripting purposes
* [Balsamiq:](https://balsamiq.com/) was used to create the wireframes
* [DrawSQL](https://drawsql.app/) was used to draw the SQL tables
* [Am I Responsive](http://ami.responsivedesign.is/) was used for creating the multi-device mock-up shown at the top of this README.md file
* [Tiny PNG](https://tinypng.com/) was used to reduce the file size of the background image
* [Code Institute's GitHub full template](https://github.com/Code-Institute-Org/python-essentials-template) in order to run Django and Python on Heroku
* [RapidTables Hex to Binary converter](https://www.rapidtables.com/convert/number/hex-to-binary.html) in order to convert from hex numbers to binary & vice versa

#### requirements.txt

```
asgiref==3.7.2
bitarray==2.8.3
bitstring==4.1.3
cloudinary==1.36.0
dj-database-url==0.5.0
dj3-cloudinary-storage==0.0.6
Django==3.2.23
django-allauth==0.41.0
gunicorn==21.2.0
oauthlib==3.2.2
psycopg2==2.9.9
PyJWT==2.8.0
python-dateutil==2.8.2
python3-openid==3.2.0
pytz==2023.3.post1
requests-oauthlib==1.3.1
sqlparse==0.4.4
urllib3==1.26.15

```
------

## Future Features
* Fully Flexible Editing of Bookings without the constraint of a mandatory *Principal Pax*. That is,
* * Be able to add new passengers to an existing booking
* * Delete any passenger from a booking
* * Be able to *change* passenger type e.g. *Adult to Child, Child to Infant, Child to Adult* and vice versa
* Search for a booking by the name of any passenger who is part of the booking
* Give the user the option to change their password
* Warn users when leaving a page if there are any unsaved changes


### Limitations

## Testing

Please refer to [TESTING.md](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/TESTING.md)

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


### Known Bugs

If the user clicks the *back button* whilst navigating this App, such an action may cause an *Error 500*!<br/>
If this happens, press Ctrl-F5 and then hit the home button, in order to continue.<br/>
To avoid such an error, please use *the Home Button and the Create Booking* options to navigate this App.

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
+ I visited the websites of [BA](https://www.britishairways.com/travel/home/public/en_gb/) and [EasyJet](https://www.easyjet.com/en) to get an idea of the layout of forms and the phraseology of error messages
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

