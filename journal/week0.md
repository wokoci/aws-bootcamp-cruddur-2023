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




## Set a billing alarm, Set a AWS Budget




## Well Architected Tool Review



## AWS Service limits Research


## Opening a support ticket and request a service limit

## Recreate logical Architecture diagram from Week 0

Below is the recreated logical architecture diagram from week 0 classes as well as url to lucid chart

![Logical Architecture from Week 0](https://user-images.githubusercontent.com/1112540/219733326-20ad6aaa-6d15-4df7-9f81-a14aaa835d7e.png)

Link to lucid chart for Logicak Architecture can be found here: https://lucid.app/lucidchart/2dc82e5e-c1fb-4fe2-aff8-c7c9421eafe3/edit?page=0_0&invitationId=inv_77797f32-1129-43a1-a570-f22f2b230c8b#

