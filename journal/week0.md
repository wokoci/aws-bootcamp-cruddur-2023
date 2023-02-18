# Week 0 — Billing and Architecture


## CI/CD architecture diagrame 
The link to the CI/CD pipeline can be found at https://lucid.app/lucidchart/463a3bef-14a6-49ec-aca8-b670d5da902b/edit?beaconFlowId=E3E276CB50736FA3&invitationId=inv_7471f433-f243-4190-a386-3476400dec7d&page=0_0#

![Ci/CD pipeline](https://user-images.githubusercontent.com/1112540/219514021-f841b1da-5012-4e7b-9508-4a2274e39785.png)


## EventBridge Health Dashboard SNS notification system via email
Steps to setup Event notification when AWS expeirnced an issue with any of it's services are outlined as follows:

- Setup sns notification to deliver emial to and email address of your choice and confirm the email address

![SNS](https://user-images.githubusercontent.com/1112540/219746659-8e8021eb-85f7-4134-94a0-e76e3f76e190.png)

- Seach to health dashboard and click on and click on Configure to start setting up event bridge notification

![Health Dashboard page](https://user-images.githubusercontent.com/1112540/219747409-95e5b2d7-5000-4965-8b7d-df6595a4a48b.png)

- Name the rule ans slect Rule with an event pattern

  ![setup rule](https://user-images.githubusercontent.com/1112540/219747994-bf889fc1-373f-44fb-a25e-6de9d2c315f7.png)

- select health event as outlined below and click on next

![Event pattern](https://user-images.githubusercontent.com/1112540/219748534-cdaec27d-e683-4bd2-a34a-103988dcc9fa.png)


- Select aws service and select sns topic and the email target previously specified and click on next

![Target](https://user-images.githubusercontent.com/1112540/219749439-145efdee-4c3f-4aa8-aa64-49ceaeace84e.png)

- skip tags and click on next  and then create rule

It is expected that whenever aws has an issue with any of it's ervice, and email will be sent with the issue they are having

## Destroy your root account credentials| Set MFA. IAM role

The root account is too powerful to be used for day to day administration and management of an aws account. It is recommended to create another account with Administrative acces that  should be used instead. 
Go to IAM and create an admin account woth admin acces and enable MFA on the account as well as the root account
Use the newly created account for daily management and administration of the account going forward.
Add the user to group if needed or attach a policy that grants the user admin access and click on create to create the account


![image](https://user-images.githubusercontent.com/1112540/219851430-bb9bacde-c2eb-485f-9279-23d87b6f2475.png)

![image](https://user-images.githubusercontent.com/1112540/219851497-84440f6a-4860-4df4-8764-2c61b6e03fe5.png)



## Set a billing alarm, Set a AWS Budget

To set a budget I search for billing and select Budget on the left

- click on create budge
- Select Monthly budget from the template
- Give the budget a name 
- enter an email address that will recieve the budget notification
- enter a limit in USD that will triggere and email to be sent when the amount is reached
- click on create budget

![creating budget](https://user-images.githubusercontent.com/1112540/219850347-a78581ee-71a2-4441-890b-0b118fd34f32.png)


## Well Architected Tool Review



## AWS Service limits Research and research on service limit
AWS places restriction on the maximum number of the compute resources that any user or organisation cab use. This is to reduce the rist of over spend by an intruder gaining access that another users account and spinning up multiple resources. 
To reqyest a service limit increate from aws, do the following:
- search for Service Quotas
- select the service that you want to be increaed like compute 
- click on Request quota increase
- enter the new value you want the quota increase to be
- click on Request to submit the request


![image](https://user-images.githubusercontent.com/1112540/219850807-43601a65-cdd2-4ed6-b89e-6206a8f9f4e7.png)

![image](https://user-images.githubusercontent.com/1112540/219850915-f3836b6d-2b39-4dc5-a946-2d5305e669d4.png)

![image](https://user-images.githubusercontent.com/1112540/219850994-bbda98e5-da09-491e-80ac-1d49e7895692.png)


## Opening a support ticket and request a service limit

## Recreate logical Architecture diagram from Week 0

Below is the recreated logical architecture diagram from week 0 classes as well as url to lucid chart

![Logical Architecture from Week 0](https://user-images.githubusercontent.com/1112540/219733326-20ad6aaa-6d15-4df7-9f81-a14aaa835d7e.png)

Link to lucid chart for Logicak Architecture can be found here: https://lucid.app/lucidchart/2dc82e5e-c1fb-4fe2-aff8-c7c9421eafe3/edit?page=0_0&invitationId=inv_77797f32-1129-43a1-a570-f22f2b230c8b#

