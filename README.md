# Interakt Track Python
SDK : [interakt-track-python](https://pypi.org/project/interakt-track-python/)

# Getting Started

Install `interakt-track-python` using pip

    pip install interakt-track-python

## Authentication
Inside your app, you’ll want to set your `api_key` before making any track calls:

To find your API key,

- go to your interakt account's Settings --> Developer Settings

- copy the Secret Key.

- Make sure you base64 decode this Secret Key (you may choose to do that from [Base64 Decode and Encode- online](https://www.base64decode.org/) )

- Erase the ':' at the end of the base64 decoded key

- Use this key

```
import track

track.api_key =  "YOUR_API_KEY"
```


## Development Settings

The default initialization settings are production-ready and queue messages to be processed by a background thread.

In development you might want to enable some settings to make it easier to spot problems. Enabling `track.debug` will log debugging info to the Python logger. You can also add an `on_error` handler to specifically print out the response you’re seeing from our API.
```
def on_error(error, queue_msg):
    print("An error occurred", error)
    print("Queue message", queue_msg)

track.debug = True
track.on_error = on_error
```
### All Settings:
| Settings name  | Type     | Default value | Description                                                                                                              |
| -------------- | -------- | ------------- | ------------------------------------------------------------------------------------------------------------------------ |
| sync_mode      | bool     | False         | When `True`, calls the track API **synchronously**. When `False`, calls the track APIs **asynchronously** using a Queue. |
| debug          | bool     | False         | To turn on debug logging                                                                                                 |
| timeout        | int      | 10            | Timout for track API calls                                                                                               |
| max_retries    | int      | 3             | Number of API retries in case API call fails due to some error                                                           |
| max_queue_size | int      | 10000         | Max Queue size                                                                                                           |
| on_error       | function | None          | Callback function which is called whenever an error occurs in **asynchronous** mode                                      |


# APIs
## User
The user track API allows customers to record the attributes specific to the user. They can record specific user properties (attributes) such as user id, email id, phone number, name etc. Customers can call the usertrack API when a new user account is created on their website/app/CRM. For example:


**For adding a new user to your interakt dashboard**, the following payload could be sent in the API call:

```
track.user(
	user_id="<user_id in your db>",
	country_code="+91",
	phone_number="9999999999",
	traits={
		"name": "John Doe",
		"email": "john@email.com",
		"age": 24,
		“dob”: “1998-01-01”
	}
)
```

The different user attributes (traits) can be of the following data types: String, Numbers, Boolean, Datetime, List. **Check out the different filter options available in interakt, for different trait types -** [link](https://ik.imagekit.io/z4utvq9kty5/interakt_filters_K5dMwG4qe.pdf).
‍<br/>
<br/>
**Note\*\***: Specifying either the **user Id** or **phoneNumber (with countryCode)** is **Mandatory**
<br/>
‍<br/>
The above API call records the “userId” or “phoneNumber” (with “countryCode”) as a unique identifier for the user and also adds attributes such as name, email, dob.



<table>
<tr>
<th>Event Property </th>
<th>Type </th>
<th>Status	 </th>
<th>Description
</tr>

<tr>
<td>user_id</td>
<td>String</td>
<td><strong>Optional**</strong></td>
<td>	The userId can take any string value that you specify. This will henceforth be used as a unique identifier for the user.
<br/>
The user id parameter will remain the same throughout the lifetime of the customer & cannot be updated. It is recommended that you use your database id instead of a plain username, as database ids generally never change.</td>
</tr>

<tr>
<td>phone_number</td>
<td>String</td>
<td><strong>Mandatory**</strong></td>
<td>phone number of the user without the country code (we recommend that you send the Whatsapp phone number of the user, so that you can send messages to that user via interakt, else the messages won’t get sent)

</td>
</tr>

<tr>
<td>country_code</td>
<td>String</td>
<td><strong>Mandatory**</strong></td>
<td>Country code of the phone number. The default value is “+91”.

</td>
</tr>

<tr>
<td>traits	</td>
<td>Object</td>
<td>Optional</td>
<td>User attributes such as name, email id etc.</td>
</tr>

<tr>
<td>created_at</td>
<td>Date</td>
<td>Optional</td>
<td>Timestamp of the event in ISO-8601 format date string. If you have not passed the “createdAt” property, we will automatically use the current utc server time as the value of “createdAt”
</td>
</tr>

</table>



**To update attributes for the above user**, the following payload could be sent in the API call: (suppose the “dob” attribute needs to be changed to “1997-12-01”).
‍
```
track.user(
	user_id="<user_id in your db>",
	country_code="+91",
	phone_number="9999999999",
	traits={
        “dob”: “1997-12-01”
    }
)
```
‍
**To add a new attribute for the above user**, the following payload could be sent in the API call: (suppose the “pin code” attribute needs to be added).
‍
```
track.user(
	user_id="<user_id in your db>",
	country_code="+91",
	phone_number="9999999999",
	traits={
    	“Pin code”: “400001”
    }
)
```
‍
‍**Note**:

1. In case, the above user had originally been added via the interakt dashboard (and not by calling the User Track API), then, no userId would exist for that user. In that case, you could either:
- Call the User Track API without specifying a “userId” (and only specifying the “phoneNumber” & “countryCode”), or,
- Include a userId in the API call, which will then get added for that user, and you could use that userId to reference that user in future API calls.*
‍
2. Currently, we don’t provide the option for deleting any user / user attribute.

**Please make sure the added userId doesn’t belong to an already existing user in your interakt account, else the API will throw an error.*





## Event
The event track API allows customers to record user actions. Each user action (such as a new order created, new user sign up, and so on) will trigger an event to the endpoint. For example:

**For adding a new event for a particular user**, the following payload could be sent in the API call:

```‍

track.event(
	user_id="<user id in your db>",
	event="Order Placed",
	“traits”={
		“orderCreatedBy”: “Gavin Roberts”,
		“orderCreatedDate”: “2020-11-01T012:10:26.122Z”,
		“orderNumber”: “CUS001”,
		“orderValue”: “50.00”
	},
	country_code="+91",
	phone_number="9999999999",
)
```

The above API call triggers an OrderPlaced event when your user makes an order on your website/app. The API call passes the event properties orderCreatedBy, orderCreatedDate, orderNumber and orderValue to the API endpoint.
‍<br>
**Please note:** In case userId doesn't exist for a user, "phoneNumber" & "countryCode" would need to be specified in the above Event Track API Call.



<table>
<tr>
<th>Event Property </th>
<th>Type </th>
<th>Status	 </th>
<th>Description
</tr>

<tr>
<td>user_id</td>
<td>String</td>
<td>Optional</td>
<td>Unique identifier for the user.</td>
</tr>

<tr>
<td>event</td>
<td>String</td>
<td>Optional</td>
<td>The action that the user has performed. It’s important to give meaningful names for your events. Example: OrderCreated, NewSignUp, OrderExecuted, etc.
</td>
</tr>

<tr>
<td>traits</td>
<td>Object</td>
<td>Optional</td>
<td>Properties are additional bits of information corresponding to the user action that is performed. They provide detailed information about user actions.
</td>
</tr>

<tr>
<td>created_at	</td>
<td>Date</td>
<td>Optional</td>
<td>Timestamp of the event in ISO-8601 format date string. If you have not passed the “createdAt” property, we will automatically use the current utc server time as the value of “createdAt”
</td>
</tr>

<tr>
<td>phone_number</td>
<td>String</td>
<td><strong>Mandatory**</strong></td>
<td>phone number of the user without the country code (we recommend that you send the Whatsapp phone number of the user, so that you can send messages to that user via interakt, else the messages won’t get sent)

</td>
</tr>

<tr>
<td>country_code</td>
<td>String</td>
<td><strong>Mandatory**</strong></td>
<td>Country code of the phone number. The default value is “+91”.

</td>
</tr>

</table>

