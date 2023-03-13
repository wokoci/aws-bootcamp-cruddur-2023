# Week 2 — Distributed Tracing

## Honeycomb
- Honeycomb comes with a default env called test
- we make one called `BootCamp`
    - Add your own environment
    - The Api key determines where the logs are delivered
    - The Api key can be obtained after registering for the service and loging in
![Environment setup](https://user-images.githubusercontent.com/1112540/224670963-6b08afc4-f67e-4b37-b44e-c4a13b3a3063.png)

### Install the required honeycomb packages for the backend
- log in to honeycomb (**Honeycomb.io) —- https://[ui.honeycomb.com](http://ui.honeycomb.com)**
    - get your API key
    - install the honeycomb client on your computer
        - details available from your honeycomb page
    - the packages used for thie backend is for python
  ~~~
  pip install opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp-proto-http \
    opentelemetry-instrumentation-flask \
    opentelemetry-instrumentation-requests
  ~~~
  To get the packages written to the requirements.txt file we freeze the packages
  ~~~
  pip freezr >> requirements.txt
  ~~~
  
  We next add import the packages into the `app.py` file and add the initialisation and instrumentation code provided by honeycomb on there website
  ~~~
  from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Initialize automatic instrumentation with Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

![image](https://user-images.githubusercontent.com/1112540/224676362-e43c4ea2-6e6d-44f6-b61c-f4a764ba3873.png)

To check if logs are been produced by your code, the following can be added in addition to the spaneEsporteds for writting to Honeycomb

~~~
from opentelemetry.sdk.trace.export import SimpleSpanProcessor,ConsoleSpanExporter

simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)
~~~



After the above is done, we need to set the environment variables for honeycomb so that the trace data can be written to the correct account
The header of `x-honeycomb-team` is your API key. Service name will be used as service Dataset and in this case, `Cruddur` was used
~~~
export OTEL_EXPORTER_OTLP_ENDPOINT="https://api.honeycomb.io"
export OTEL_EXPORTER_OTLP_HEADERS="x-honeycomb-team=gtCxL9KRKdsertOxDQT0OsyA"
export OTEL_SERVICE_NAME="Cruddur"
~~~
In addition to exporting the above env vars, an additional export is also done to Gitpod so as not to re-enter each time a new workspace 
is created in git pod. The vars as set as follows:
~~~
gp env HONEYCOMB_API_KEY="YVxzp7pP5RqKUqeB"efq
gp env HONEYCOMB_SERVICE_NAME="Cruddur"
~~~

The best practice relating to the service name & OTEL_EXPORTER_OTTLP_ENDPOINT is to set it in the `docker-compose.yml` file as follows
![image](https://user-images.githubusercontent.com/1112540/224674487-9276bc59-be10-4981-912a-86b607c303a7.png)

### Checking your traces
After all the above has been done, traces should be available in honeycomb

![image](https://user-images.githubusercontent.com/1112540/224678380-fa3de202-e87f-4f70-b68d-87fd3e4c4764.png)

If no data is delivered to honeycomb, and there are no errors, you can check where your traces are being delivered to by navigating to the following site and entering your `honeycomb` api key
~~~
https://honeycomb-whoami.glitch.me/trace
~~~

We can instrument specific activitities or components of our app. I am adding code to instrument the HomeActivity page of the app as shown below:

~~~
from opentelemetry import trace
trace = trace.get_trace("home.activity.trace")

class HomeActivities:
  def run():
    # tracerf or home. activity to send spans to honeycomb
    with tracer.start_as_current_span("home-activity-mock-data-data") as outer_span:
      outer_span.set_attribute("outer", True)
      now = datetime.now(timezone.utc).astimezone()
      results = [{
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Andrew Brown',
        'message': 'Cloud is fun!',
        'created_at': (now - timedelta(days=2)).isoformat(),
        'expires_at': (now + timedelta(days=5)).isoformat(),
#some code omitted
~~~
With the above entries into the HomeActivity page, we can see traces related to home activity as shown in image below:

![image](https://user-images.githubusercontent.com/1112540/224680283-3fa7e394-20b5-4379-a74c-d8d5e4f69c0c.png)


### Opentelemetry
Honeycomb uses the Opentelemetry standard the is maintained by CNCF and supportedby a number of organisations. the architecture is shown below

![image](https://user-images.githubusercontent.com/1112540/224675742-120cfe5c-d33a-4aab-a647-bf61955b2715.png)



## Instrument with x-ray
- requires the aws sdk installed in the dev env
- boto3 is the sdk used for python in aws
- install the sdk with pip
    - `aws-xray-sdk`

~~~

pip install aws-xray-sdk
pip freeze >> requirements.txt

~~~

- ecs container are not very easy to instrument
- lambda and others are easier to instrument
- Setup
    - requires a daemon to work
        - see xray arch image below

![image](https://user-images.githubusercontent.com/1112540/224686344-260bb80e-88dc-44e1-be4c-2808a5ab7d60.png)

- Middleware
    - an application that seats in front of your app to receive process and distribute requests
    - can do thinks like
        - auth
        - whitelisting
        - filtering
        - processing traces
        - etc
- Add the following to the `[app.py](http://app.py)` file in backend
    - recorder & middleware imported below

~~~

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

~~~

The recorder and middleware are configured as shown below with the `aws-xray-url`

~~~

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='Cruddur', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)

~~~


- Ensure the x-ray url is specified after creating x-ray which is done with:
    - the json below is named: `xray.json`
    - the json doc can be found in aws docs

~~~
{
    "SamplingRule": {
        "RuleName": "base-crussar",
        "ResourceARN": "*",
        "Priority": 9000,
        "FixedRate": 0.1,
        "ReservoirSize": 5,
        "ServiceName": "Crussar",
        "ServiceType": "*",
        "Host": "*",
        "HTTPMethod": "*",
        "URLPath": "*",
        "Version": 1
    }
}
# this is for creatig the sampling rule
Save to a json file within the aws folder, eg `sample.json`
~~~

New, we creare a group for x-ray from the commandline with the following aws cli command and the add the samplging rule:

~~~

#we create a group with following first:
$ aws xray create-group --group-name "Cruddur" --filter-expression "service(\"backend-flask\")"

# then run the following aws cli command to create the sampling rule pointing it to the a
#  above json file

aws xray create-sampling-rule \
    --cli-input-json file://xray.json

~~~
If the above command is successful, will produce the following json:

~~~

{
    "SamplingRuleRecord": {
        "SamplingRule": {
            "RuleName": "Cruddur",
            "RuleARN": "arn:aws:xray:us-east-1:14751634523295:sampling-rule/Cruddur",
            "ResourceARN": "*",
            "Priority": 9000,
            "FixedRate": 0.1,
            "ReservoirSize": 5,
            "ServiceName": "backend-flask",
            "ServiceType": "*",
            "Host": "*",
            "HTTPMethod": "*",
            "URLPath": "*",
            "Version": 1,
            "Attributes": {}
        },
        "CreatedAt": "2023-03-12T15:21:08+00:00",
        "ModifiedAt": "2023-03-12T15:21:08+00:00"
    }
}

~~~
The output for the group is shown below:

~~~

{
    "Group": {
        "GroupName": "Cruddur",
        "GroupARN": "arn:aws:xray:us-east-1:14423586541195:group/Cruddur/LWSL2ZADCIGGQG3SM7EGHDKHH6UMKB5QCCDAOOIT6JXVJ2CDDO2A",
        "FilterExpression": "service(\"backend-flask\")",
        "InsightsConfiguration": {
            "InsightsEnabled": false,
            "NotificationsEnabled": false
        }
    }
}

~~~

Navigating to x-ray in the AWS console should show something similar to the following:

![image](https://user-images.githubusercontent.com/1112540/224688190-54728657-bc2c-456a-9d2e-9a7e36ed2c3c.png)


Next step is to setup the x-ray daemon. Do this by adding the following to `docker-compose.yml` file

~~~
xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "us-east-1"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000/udp
~~~
The above will pull the x-ray docker image and collect end send traces to xray from the application


We also need to add the env vars for x-ray into our workspace, we neeed to add the followinf to our `docker-compose.yml` file

~~~

AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"

~~~

- Bringing up the application produced some traces as shown below
- for every event, a segment is sent to xray via the container, Looking at the container logs shows the following:

![image](https://user-images.githubusercontent.com/1112540/224689358-d999ce79-07c1-4e5b-b8e0-9fd370d7da80.png)

looking at the x-ray console in aws show the following:
![image](https://user-images.githubusercontent.com/1112540/224689437-2bcb8d2a-4e80-4425-a2ad-a79eaacf390d.png)

Service map produced by the trace is shown below:

![image](https://user-images.githubusercontent.com/1112540/224689558-91cd8d37-e4a3-4a9b-9747-6c14a8493bcc.png)

To get segments from specific activities in the application, we can add the following code into the user activity

~~~

from aws_xray_sdk.core import xray_recorder
with xray_recorder.in_segment('user.activity') as segment:
dict = {
        "user":"Jeffrey",
        "now":now.isoformat()
      }
    
      segment.put_metadata('key', dict, 'namespace')

~~~

### **Instrumenting with Cloudwatch logs**

- Requires the installation of `watchtower`
    - python code to install watchtower with pip below:

~~~
pip install watchtower
pip freeze >> requirements.txt
# the freeze line ensures the added packages are added to the requirements.txt file with the installed versions
~~~

Add the watchtower imports into the `app.pya file

~~~

# aws watchtower import details below ------------
import watchtower
import logging
from time import strftime

~~~

Next, we initialise the logger
~~~
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("some message if you want to pass this in")

~~~

We can also force it to log error after request with the following:
~~~

@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

~~~
After bringing up the app with docker compose, the following entries can be viewed in aws cloudwatch logs
![image](https://user-images.githubusercontent.com/1112540/224690744-33efdff2-297f-4995-87df-1ce6517e811a.png)


Logstream shown below
![image](https://user-images.githubusercontent.com/1112540/224690887-38e0f665-fe39-4e01-b942-08b97aaa9323.png)


Log events shown below from app

![image](https://user-images.githubusercontent.com/1112540/224690987-bae945af-b40d-48cb-b9b0-6636fe70e514.png)


Subsegments shoen below with custom values:

![image](https://user-images.githubusercontent.com/1112540/224691069-7f208137-b8c9-4450-a914-0023adc41988.png)



### **Rollbar setup

- Log into [*Rollbar*](https://app.rollbar.com/onboarding)
    - select apps to be instrumented - flask & react in this case
        - select flask and continue
        - only one SDK can be selected at a time

![image](https://user-images.githubusercontent.com/1112540/224691271-3ef2d5a0-5048-49f1-bfa6-9dbc95ae803c.png)

Rollbar requires rollbar python package to be installed: 
the packages to be install are
  - rollbar
  - blinker

~~~

pip install rollbar blinker
pip freeze >> requirements.txt

~~~

After setup, the following page with your config. details are displayed which includes instructions on how to configure rollbar

![image](https://user-images.githubusercontent.com/1112540/224692252-fd59fb9a-0c7a-4707-b07b-6479c1f034e0.png)

Note: your api key can be found in theprovided steps

The actual steps used to configure rollbar is show in code below which is different from what's provided by rollbar

~~~

from flask import Flask
app = Flask(__name__)

## Rollbar init code. You'll need the following to use Rollbar with Flask.
## This requires the 'blinker' package to be installed

import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception


@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        'e7fe94fde24345134d2ab1c6e4c4wee223b',
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

## Simple flask app

@app.route('/')
def hello():
    print "in hello"
    x = None
    x[5]
    return "Hello World!"

~~~

We also have to include the access token for rollbar into the gitpod and workspace envs as shown below:

~~~

export ROLLBAR_ACCESS_TOKEN="e7fe94fde2434b4c8feb1c6e4c49e1db"
gp env ROLLBAR_ACCESS_TOKEN="e7fe94fde2434b4c8feb1c6e4c49e1db"

~~~

We also have to add the initilisation code as shown below:

~~~

# Rollbar init script below -------------
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

~~~
The following can be used to test rollber by calling the `/rollbar/test` endpoint

~~~

@app.route('/rollbar/test')
def rollbar_test():
    rollbar.report_message('Hello World!', 'warning')
    return "Hello World!"

~~~

After interacting with the application to generate some activities, the following values were seen in rollbar:

![image](https://user-images.githubusercontent.com/1112540/224693543-4efe728d-6c72-44cf-ae59-d52f2402e736.png)


Details show for error with show activity

![image](https://user-images.githubusercontent.com/1112540/224693617-b06a911d-ed85-4e0c-87d0-2a59a21548d6.png)



## Spening considerations for Honeycomb

- log in to honeycomb
- check usage
    - 20 million requests are free

   Spending consideration for Rollbar:

- provides 5000 events per month
- data is retained for a month

 Spending consideration for AWS:

- 100k traces free for x-ray
- cloudwatch gives 5gb of data & logs




## Security considerations for observability
- Logging enables you to identify and resolve issues with your system
- needed for distributed systems
- there are challenges which are different for infrastructure
![image](https://user-images.githubusercontent.com/1112540/224681460-7bd963f0-9964-4bef-bee6-0000000d0980.png)

- logging take time to analyse
- loads of data is produced which makes it hard

**Hence Observability**

- looks at the entire system including system health
- Observability vs Monitoring
    - Monitoring checks a system at intervals to see if its ok, eg health checks
        - need to identify noise from monitoring

![image](https://user-images.githubusercontent.com/1112540/224683305-0c11ec64-8ef8-4fc0-9b9a-458feadb0281.png)

Above are some items to consider about security when it comes to observability

We need visibility on all processes running in AWS. Observability is the way you break down the data from logging through the systems
There are 3 pillars of Observibility which are
  - Metrics
  - Traces
  - Logs

Enabling cloud-watch
 - logs are written for events performed in the system

 - use metric filter to filter out what you want

    - outcome from filter can be used for

    - notification

    - alarming

 - log groups can be written to by unified cloudwatch logging agent

 - other tools include

   - inspector

   - meice

   - x-ray

   - aws distro for open telemetry

- **Observability from AWS perspective**
    - AWS CloudWatch Logs
    - AWS CloudWatch Metrics
    - AWS X Ray Traces
![image](https://user-images.githubusercontent.com/1112540/224684800-ca451db7-72fe-4a6d-8d58-539a100af243.png)

notice the absence of security in the above. This does not indicate that AWS is not interested in security.

- In AWS, cloudtrail logs all API activities made by a user. This can be loaded to S3 or cloudwatch.
    - To enable this in cloudtrail
        
        in cloudwatc log section of cloudtrail, create a **log-group**
        
        need correct role to perform needed actions
        
- We can create metrics from logged entries
    - the metrics can be used to create metric filter
        - when specified item is found in logs
            - will trigger a desired action
            - eg
                - security group changes
                - important service disabled. or deleted
        - Amazon detector can also help with security
    - Note: X-ray can only do tracing at the moment

- **Use AWS Eventbridge to alert for alerts**
    - Event Driven Architecture using Serverless
    - Auto Remediation with Amazon EventBridge and AWS Security Hub
    - AWS Services for Threat Detection - Amazon GuardDuty,3rd Party etc

![image](https://user-images.githubusercontent.com/1112540/224685603-d33c059a-26cf-436c-a29f-ca2344e9a04f.png)



