# Interakt Track Python
SDK : [interakt-track-python](https://pypi.org/project/interakt-track-python/)

# Getting Started

Install `interakt-track-python` using pip

    pip install interakt-track-python
    
## Authentication
Inside your app, you’ll want to **set your** `write_key` before making any track calls:
```
import track

track.write_key =  "YOUR_WRITE_KEY"
```
Interakt Track APIs uses HTTP Basic Auth, which involves a `‘username:password’` that is **base64 encoded** and prepended with the string `‘Basic ‘`. 

Your **write_key** is your `username` and `password` is empty. Which means if your **write_key** is `'abcd123'`,  a colon is added to it, and then the password field is left empty. 

After base64 encoding `'abcd123:'` becomes `'YWJjZDEyMzo='`; and this is passed in the authorization header like so: `'Authorization: Basic YWJjZDEyMzo='`



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
|Settings name|Type|Default value|Description|
|--|--|--|--|
|sync_mode|bool|False|When `True`, calls the track API **synchronously**. When `False`, calls the track APIs **asynchronously** using a Queue.|
|debug|bool|False|To turn on debug logging|
|timeout|int|10|Timout for track API calls|
|max_retries|int|3|Number of API retries in case API call fails due to some error|
|max_queue_size|int|10000|Max Queue size|
|on_error|function|None|Callback function which is called whenever an error occurs in **asynchronous** mode


# APIs
## Identify
The `identify` lets you tie a user to their actions and record traits about them. It includes a unique **User ID** or **Phone Number and Country Code** any optional traits you know about them.

Example `identify` call:
```
track.identify(
	user_id="<USER_ID>",
	traits={
		"name": "John Doe",
		"email": "john@email.com",
		"age": 24
	}
)
```
The `identify` call has the following fields:
|Field|Data type|Description|
|--|--|--|
|user_id|str or int|The ID for the user in your database.|
|country_code|str|country code for the phone_number (default value is "+91")|
|phone_number|str|phone_number without country_code (eg: "9876598765")|
|traits|dict|A dict of traits you know about the user. Things like: `email`, `name` or `age`|

**NOTE:** Atleast one of these two is required for user identification :

 - **user_id**, OR
 - **phone_number** with **country_code**




## Event
`event` track API lets you record the actions your users perform. Every action triggers what we call an “event”, which can also have associated properties.

Example `event` call:
```
track.event(
	user_id="changu_mangu",
	event="Product Added",
	traits={"price": 200}
)
```
The `event` call has the following fields:
|Field|Data type|Description|
|--|--|--|
|user_id|str or int|The ID for the user in your database.|
|event|str|Name of the event you want to track, For eg: "Product Added".|
|traits|dict|dictionary of properties for the event. If the event was **Product Added**, it might have properties like `price` or `product_name`.|
