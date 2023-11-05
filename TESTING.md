# Testing

## Manual Testing

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
|  T01 | Install Django  | Install Django, psycopg2. Create requirements.txt. Name the Project **manxairlines**. Create the App and name it **booking**. Deployed locally.  | Expected to see the webpage showing the following message: *The install worked successfully!*  | PASS |

<details>
<summary>Screenshot</summary>
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a36de784-ce15-4163-b176-8a8080cbb3df)
</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
|  T02 | Heroku Deployment  | Create App on Heroku. Call it **manx-airlines-bookings**. Setup a Database Instance on [ElephantSQL](elephantsql.com). Set up the following Heroku Config Vars: <br>1) Copy the generated URL into **DATABASE_URL**; <br>2) Copy Secret Key into **SECRET_KEY**; <br>3) Set **PORT to 8000**; <br>4) Set **DISABLE_COLLECTSTATIC to 1**. <br>Connect Heroku App to GitHub. Deploy.  | Expected to see the webpage showing the following message: *The install worked successfully!* As in the above screenshot | PASS |

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
|  T03 | Display Home Page  | Set up the relevant Django directories, views and urls to display **index.html**  | Expect to see the home page with the ubiquitous **Hello World** message. | PASS |

<details>
<summary>Screenshot</summary>
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/8ce86214-4762-4695-9bf0-25fb974d0f80)

</details>


## Automated Testing
