# Interakt Track Python

# Getting Started

Install `interakt-track-python` using pip

    pip install interakt-track-python
    
Inside your app, you’ll want to **set your** `write_key` before making any track calls:

    import track
    
    track.write_key =  "YOUR_WRITE_KEY"


## Development Settings

The default initialization settings are production-ready and queue messages to be processed by a background thread.

In development you might want to enable some settings to make it easier to spot problems. Enabling `track.debug` will log debugging info to the Python logger. You can also add an `on_error` handler to specifically print out the response you’re seeing from our API.
```
def on_error(error, items):
    print("An error occurred:", error)


track.debug = True
track.on_error = on_error

```

# Identify
The `identify` lets you tie a user to their actions and record traits about them. It includes a unique **User ID** or **Phone Number and Country Code** any optional traits you know about them.

Either of the two for user identification is required:

 - **user_id**
 - **phone_number** with **country_code**

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

# Event
`event` lets you record the actions your users perform. Every action triggers what we call an “event”, which can also have associated properties.

Example `event` call:
```
track.event(
	user_id="<USER_ID>",
	event="Add to Cart",
	traits={"amount": 200}
)
```
