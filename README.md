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
|Settings name|Type|Default value|Description|
|--|--|--|--|
|sync_mode|bool|False|When `True`, calls the track API **synchronously**. When `False`, calls the track APIs **asynchronously** using a Queue.|
|debug|bool|False|To turn on debug logging|
|timeout|int|10|Timout for track API calls|
|max_retries|int|3|Number of API retries in case API call fails due to some error|
|max_queue_size|int|10000|Max Queue size|
|on_error|function|None|Callback function which is called whenever an error occurs in **asynchronous** mode


# APIs
## User
go to [WhatsApp Business API Documentation  | How to use WhatsAPP API for your Business](https://www.interakt.ai/resource-center/api-doc#User-Track-API)  and add the entire content till before “Where can you see the added Users in your interakt dashboard?”




## Event
go to [WhatsApp Business API Documentation  | How to use WhatsAPP API for your Business](https://www.interakt.ai/resource-center/api-doc#Event-Track-API)   and add the entire content till before “Where can you see the added Events in your interakt dashboard?”
