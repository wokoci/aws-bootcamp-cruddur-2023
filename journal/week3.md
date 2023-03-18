# Week 3 — Decentralized Authentication

## Setup Cognito userpool

- Log into aws and navigate to AWS cognito to create a cognito userpool
    - select `cogito user pool` as provider
    - select `email` & `username` as the cognito sign in option
    - specify user name requirements
        - like if case sensitive and contains upper case
        - we will not allow users to log in with preferred username
    - specify security requirements of default
    - specify the number of characters users can use for password
    - No mfa and sms delivery selected
    - enable self-service recovery
        - email only as delivery method for account recovery
            - emails are much cheaper , **62000** outgoing message per month
    - sign-up experience
        - self registration??
            - Note: self hosted UI not used for this project
        - attributes verification changes method
            - email
                - allows the system send email to user for verification
        - Required attributes
            - can include
                - photos
                - Gender
                - location
                - etc
            - we can select from the list of attributes
                - attributes cant’t be changed after they are created
    - configure message delivery
        - send mail with amazon SES
            - ses needs a custom domain
        - send email with cognitor (selected)
        - reply to email
            - provided by cognito
    - Integrate your app
        - user pool name:
            - `Cruddur-userpool` is what I use
            - We are not using hosted authentication pages
        - initial app client
            - public client
            - App client name:
                - `cruddur`
            - client secrete
                - No selected
    - The summary review page from setting up the user pool is as shown below: 
        
    
    - To integrate the code with cognito is to use the `amplify sdk`
        - we therefore need to install some packages
        - docs for ***amplify***  can be found [here](https://docs.amplify.aws/cli/auth/overview/) but this apply to the server side provisioning cognito
        - We need the frontend code for our work which can be found [***here***](https://docs.amplify.aws/lib/auth/emailpassword/q/platform/js/#sign-up)

![image](https://user-images.githubusercontent.com/1112540/226071784-4385080f-6349-4d05-914f-922d586b0478.png)

Cruddur-userpool is what I use

- To integrate the code with cognito is to use the `amplify sdk`
    - we therefore need to install some packages
    - docs for ***amplify***  can be found [here](https://docs.amplify.aws/cli/auth/overview/) but this apply to the server side provisioning cognito
    - We need the frontend code for our work which can be found [***here***](https://docs.amplify.aws/lib/auth/emailpassword/q/platform/js/#sign-up)
- Setup steps
    - setup the amplify library
        - this goes in the `react-frontend` service
        
        ```jsx
        npm i aws-amplify
        ```
        
    - the above should save the packege to `package.json` file as shown below:
        - this is not a development dependency

![image](https://user-images.githubusercontent.com/1112540/226071931-83d1023b-e67d-4801-8de4-757e0a19df66.png)

- after installing amplify, we need to open `app.js` and add the dependencies required for cognito
    - we import amplify into this file
    
    ```jsx
    import {Amplify} from 'aws-amplify'
    ```
    
- Next, we configure amplify with following code:
    - 
    
    ```jsx
    Amplify.configure({
      "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
      // "aws_cognito_identity_pool_id": process.env.REACT_APP_AWS_COGNITO_IDENTITY_POOL_ID,
      "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
      "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
      "aws_user_pools_web_client_id": process.env.REACT_APP_AWS_CLIENT_ID,
      "oauth": {},
      Auth: {
        // We are not using an Identity Pool
        // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
        region: process.env.REACT_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
        userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
        userPoolWebClientId: process.env.REACT_APP_AWS_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
      }
    });
    ```
    
    - next, we need to set the environment variables for:
        - env vars to set shown below which will be added to the `docker-compose.yml` file
        
        ```yaml
        REACT_APP_AWS_PROJECT_REGION: "${AWS_DEFAULT_REGION}"
        REACT_APP_AWS_COGNITO_REGION: "${AWS_DEFAULT_REGION}"
        REACT_APP_AWS_USER_POOLS_ID: "us-east-1_NoBGt9lLg"
        REACT_APP_AWS_CLIENT_ID: "5n0v7oqq1pirg8pf6m37ppcquu"
        ```
        
        - recall that we only created a userpool in aws cognito. and not identity pool, so the env for identity pool does not apply and has to be removed.
        - the entry into `docker-compse.yml` file is shown below:
            - entry in the frontend section of the file
            
            ```jsx
            frontend-react-js:
                environment:    
                  REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
                  REACT_APP_AWS_PROJECT_REGION: "${AWS_DEFAULT_REGION}"
                  REACT_APP_AWS_COGNITO_REGION: "${AWS_DEFAULT_REGION}"
                  REACT_APP_AWS_USER_POOLS_ID: "us-east-1_NoBGt9lLg"
                  REACT_APP_AWS_CLIENT_ID: "5n0v7oqq1pirg8pf6m37ppcquu"    
                build: ./frontend-react-js
                ports:
                  - "3000:3000"
            ```
            
    - Note: REACT_APP is needed in front of the env vars to allow for the app to load the variables
    - the clientId is not sensitive and can be committed to git. It could have been passed as env vars if it was considered as sensitive

- with the above in place
    - we need to update the Homepagefeed.js with amplify auth as follows:
     ![image](https://user-images.githubusercontent.com/1112540/226071988-4182b5a2-fba0-4969-89bf-9f9854513b8a.png)
     
     - we also set the state as we need to manage the users state
    - 

```yaml
// set a state
const [user, setUser] = React.useState(null);
```

- This goes under the HomeFeedPage function

![image](https://user-images.githubusercontent.com/1112540/226072004-165442ee-20a9-4ac9-8468-50f010cd9a9f.png)

- nest step is to add the checkAuthCode for cognito

```jsx
// check if we are authenicated
const checkAuth = async () => {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {
    console.log('user',user);
    return Auth.currentAuthenticatedUser()
  }).then((cognito_user) => {
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
  })
  .catch((err) => console.log(err));
};
```

- Updating profileinfo.js
    - we add the amplify import to above page
        - 
        
        ```jsx
        import {Auth} from 'aws-amplify';
        ```
        
        - In addition the the amplify import, we also update the file with
        - 
        
        ```jsx
        const signOut = async () => {
          try {
              await Auth.signOut({ global: true });
              window.location.href = "/"
          } catch (error) {
              console.log('error signing out: ', error);
          }
        }
        ```
        
        - the above function signed the user out globally from the application when called
    - We also update the sign in page with the cognito imports and code that will allow the user sign in if they have an account in cognito
        - Import shown above
        
        ```jsx
        import { Auth } from 'aws-amplify';
        ```
        
        - Next, we update the the page with the sign in code replacing the cookie code, replacing cookies on that page with following method for sign in
        
        ```jsx
        const onsubmit = async (event) => {
          setErrors('')
          event.preventDefault();
          try {
            Auth.signIn(username, password)
              .then(user => {
                localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
                window.location.href = "/"
              })
              .catch(err => { console.log('Error!', err) });
          } catch (error) {
            if (error.code == 'UserNotConfirmedException') {
              window.location.href = "/confirm"
            }
            setErrors(error.message)
          }
          return false
        }
        ```
        
    - Note that we are using email for sign in as it was set in cognito. The docs may suggest the use of username though.
    - With the above code, we can try signing in
    
- Updates to the `signinPage.js`
    - The following is the change made to the `signinPage.js` singinPage function:
        - 
        
        ```jsx
        export default function SigninPage() {
        
          const [email, setEmail] = React.useState('');
          const [password, setPassword] = React.useState('');
          const [errors, setErrors] = React.useState('');
        
        const onsubmit = async (event) => {
          setErrors('')
          event.preventDefault();
            Auth.signIn(email, password)
              .then(user => {
                localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
                window.location.href = "/"
              })
              .catch(error => { 
                if (error.code == 'UserNotConfirmedException') {
                  window.location.href = "/confirm"
                }
                setErrors(error.message)
               });
          return false
        }
        ```
        
        - With the above changes, when the user tries to login with an incorrect username & password will give the message shown below in the browser
            - 
            
          ![image](https://user-images.githubusercontent.com/1112540/226072056-161bf3dd-8c42-4e3c-9c90-6b4cdc386811.png)

            
    - To test connection to aws cognito, we can add a user to cognito and try to sign in with that user

- To test connection to aws cognito, we can add a user to cognito and try to sign in with that user
- create a user in amazon cognito with following details:
    - username: JameLast
    - email: jlast@gmail.com
    - password: Password123*

![image](https://user-images.githubusercontent.com/1112540/226072097-638dd10c-1da0-4361-8d1d-8d87f89180d3.png)

- login attempt with the newly added user failed with
    - ***Cannot read properties of null (reading 'accessToken')***
- The user account needed to be verified and required a password change
- Command to force change password from cli
    
    ```jsx
    aws cognito-idp admin-set-user-password --username <username_here> --password Rest123* --user-pool-id us-east-1_UJFaCGGGg --permanent
    ```
    
- User is verified in AWS cognito

![image](https://user-images.githubusercontent.com/1112540/226072119-0e44de8b-5703-4898-9f86-cc94afa79ef3.png)

- With the password confirmed with the above command, User is logged into the application
    - Natifications and other menu items are also displayed on the left

![image](https://user-images.githubusercontent.com/1112540/226072137-81309108-10d6-41cd-8135-d668d9c9b021.png)

- Checking it the `sign out` functionality works by clicking on sign out
    - And the user is signed out and the menu items on the left menu are removed
- outputing `console.log("User", user)` producess the following output in the console:

![image](https://user-images.githubusercontent.com/1112540/226072154-9f4448a1-bc72-480b-91dc-b384ae1ad8e8.png)


- Setting the user details that should show up after login
    - go back to aws cognito and set
        - name
        - prefared_name
    - log into the application again
        - the values should be displayed as shown below:

![image](https://user-images.githubusercontent.com/1112540/226072181-231768e6-9590-4801-a18c-58abc3f97252.png)



- Setting up the signup page for new users
    - first we delete the user from aws cognito
    - code changes to the signup page
        - Following are changes made in signup page for user signup:
        
        ```jsx
        const onsubmit = async (event) => {
            event.preventDefault();
            setErrors('')
            try {
                const { user } = await Auth.signUp({
                  username: email,
                  password: password,
                  attributes: {
                      name: name,
                      email: email,
                      preferred_username: username,
                  },
                  autoSignIn: { // optional - enables auto sign in after user is confirmed
                      enabled: true,
                  }
                });
                console.log(user);
                window.location.href = `/confirm?email=${email}`
            } catch (error) {
                console.log(error);
                setErrors(error.message)
            }
            return false
          }
          
          // let errors;
          if (errors){
            errors = <div className='errors'>{errors.message}</div>;
          }
        ```
        
        - if signup is successful the user is taken to the confirmation page to confirm their details.
- Update to confirmation page
    - the following updates are made on the confirmations page:
        - 
        
        ```jsx
        const resend_code = async (event) => {
            setErrors('')
            try {
              await Auth.resendSignUp(email);
              console.log('code resent successfully');
              setCodeSent(true)
            } catch (err) {
              // does not return a code
              // does cognito always return english
              // for this to be an okay match?
              console.log(err)
              if (err.message == 'Username cannot be empty'){
                setCognitoErrors("You need to provide an email in order to send Resend Activiation Code")   
              } else if (err.message == "Username/client id combination not found."){
                setCognitoErrors("Email is invalid or cannot be found.")   
              }
            }
          }
          
        
          const onsubmit = async (event) => {
          event.preventDefault();
          setErrors('')
          try {
            await Auth.confirmSignUp(email, code);
            window.location.href = "/"
          } catch (error) {
            setErrors(error.message)
          }
          return false
        }
        ```
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/aee1c010-dcea-4648-a25a-122bfc62d35c/Untitled.png)
        
        - After updating aws cognito to use email address and prefared email. the login when through and a verification code delivered to the provided email address:
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/183769b5-90d9-4401-a378-ba00664b1c56/Untitled.png)
        
        - verification email
        - 
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/647fb98c-9c9d-4200-8714-7b92f6806e2c/Untitled.png)
        
        - The user account was also confirmed in aws cognito user-pool
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b65b84ec-d6ef-4122-8fc7-dc8468ceab84/Untitled.png)
        
    - update the password recovery details on the `RecoveryPage.js` file
        - The following changes to be made to the page to allow users that don’t recall their passwords get a password reset.
        - 
        
        ```jsx
        // add imports
        import { Auth } from 'aws-amplify'
        
        //Udpdate methods
        const onsubmit_send_code = async (event) => {
            event.preventDefault();
            setErrors('')
            Auth.forgotPassword(username)
            .then((data) => setFormState('confirm_code') )
            .catch((err) => setErrors(err.message) );
            return false
          }
          
        
          const onsubmit_confirm_code = async (event) => {
            event.preventDefault();
            setErrors('')
            if (password == passwordAgain){
              Auth.forgotPasswordSubmit(username, code, password)
              .then((data) => setFormState('success'))
              .catch((err) => setErrors(err.message) );
            } else {
              setCognitoErrors('Passwords do not match')
            }
            return false
          }
        ---------Below to be passed along via backend_url in HomefeedPage.js
        ``js
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        ```
        
        trying out the recovery flow delivered a reset code and allow for password reset
        
        ![image](https://user-images.githubusercontent.com/1112540/226072216-0e3d86af-f8d8-41f8-bc84-b9ea91243957.png)
        
        New password page
        
       ![image](https://user-images.githubusercontent.com/1112540/226072233-72ffdec7-e88d-4405-a583-671dfa911dd0.png)
       
       verification email 
       
       ![image](https://user-images.githubusercontent.com/1112540/226072257-96accecf-919c-461a-ac94-e35cc0e18fb7.png)


- update the password recovery details on the `RecoveryPage.js` file
    - The following changes to be made to the page to allow users that don’t recall their passwords get a password reset.
    - 
    
    ```jsx
    // add imports
    import { Auth } from 'aws-amplify'
    
    //Udpdate methods
    const onsubmit_send_code = async (event) => {
        event.preventDefault();
        setErrors('')
        Auth.forgotPassword(username)
        .then((data) => setFormState('confirm_code') )
        .catch((err) => setErrors(err.message) );
        return false
      }
      
    
      const onsubmit_confirm_code = async (event) => {
        event.preventDefault();
        setErrors('')
        if (password == passwordAgain){
          Auth.forgotPasswordSubmit(username, code, password)
          .then((data) => setFormState('success'))
          .catch((err) => setErrors(err.message) );
        } else {
          setCognitoErrors('Passwords do not match')
        }
        return false
      }
    ---------Below to be passed along via backend_url in HomefeedPage.js
    ``js
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      }
    ```
    
    trying out the recovery flow delivered a reset code and allow for password reset
    
   ![image](https://user-images.githubusercontent.com/1112540/226072293-10d96735-c49a-45c7-9963-280bee534eaf.png)

    
    New password page
    
 ![image](https://user-images.githubusercontent.com/1112540/226072307-628d7dcf-9b90-4557-96bd-37e4d6fbf57f.png)

- Approaches to verifying JWTs - Backend implementation
    - this is a way to protect out backend APIs
    - we need to pass the token along when it is set
        - via the `backend_url` value
    - this is added to `HomeFeedpage.js` as follows:


![image](https://user-images.githubusercontent.com/1112540/226072321-6fdb9e7b-1b9f-4ac0-a08d-ae62c8284b53.png)

- the request is next picked up in the backend-flask part of the application
- this change required CORs changes with following:
    
    ```jsx
    cors = CORS(
      app, 
      resources={r"/api/*": {"origins": origins}},
      headers=['Content-Type', 'Authorization'], 
      expose_headers='Authorization',
      methods="OPTIONS,GET,HEAD,POST"
    )
    ```
    
    - in app.py
        - inside `data_home()` method
            - outputting the content of AUTH into the docker console confirms that the content of AUTH is being passed along to the backend.
            - view container logs with the below code to see `AUTH` value
            
            ```jsx
            def data_home():
              app.logger.debug("AUTH HEADER")
              app.logger.debug(request.headers.get('Authorization'))
              print(request.headers.get('Authorization'))
              data = HomeActivities.run()
              return data, 200
            ```
            
        - the auth value is sensitive and should be kept private
            - it is a good practice to remove the debug value so that it does not get logged anywhere
            - The token needs to be decoded in the backend rather than going out to cognito all the time
        - we will be using `Flask-AWSCognito` for this
            - install the above package in the backend-flask codebase
            - add to requirements.txt file
    - Configure the package to work with flask
        - we need to add a number of env vars into `docker-compose.yml`
            - see image of changes below
        
       ![image](https://user-images.githubusercontent.com/1112540/226072346-c616e3b7-0eb4-4171-b18e-8fa8fda8f728.png)

- The env vars are added next to the top of the `[app.py](http://app.py)` file in backend
    - we add the congnitotAuthentication method next:
    
    ```python
    aws_auth = AWSCognitoAuthentication(app)
    ```
    
    - We also add claims call to homeActivity
        - 
        
        ```python
        @app.route("/api/activities/home", methods=['GET'])
        # @xray_recorder.capture('activities_home')
        def data_home():
          access_token = extract_access_token(request.headers)
          try:
            claims = cognito_jwt_token.verify(access_token, None)
            # authenticated request
            app.logger.debug("Authenticated")
            app.logger.debug(claims)
            app.logger.debug(claims['username'])
            data = HomeActivities.run()
          except TokenVerifyError as e:
            # unauthenticated request
            app.logger.debug(e)
            app.logger.debug("Unauthenticated request")
            data = HomeActivities.run()
          return data, 200
        ```
        
- With the above changes, we are able to see the content of claims.
- The FlaskCognito package that was used in saved locally in the `lib` folder with the content shown below. The content was modified a bit to meet the needs of obtaining and decoding the token
- The output from the docker container log is shown below:

![image](https://user-images.githubusercontent.com/1112540/226072364-52c2e79e-3102-459c-bfa5-81fb5616cb9c.png)


```python
import time
import requests
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode

class FlaskAWSCognitoError(Exception):
  pass

class TokenVerifyError(Exception):
  pass

def extract_access_token(request_headers):
    access_token = None
    auth_header = request_headers.get("Authorization")
    if auth_header and " " in auth_header:
        _, access_token = auth_header.split()
    return access_token

class CognitoJwtToken:
    def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
        self.region = region
        if not self.region:
            raise FlaskAWSCognitoError("No AWS region provided")
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.claims = None
        if not request_client:
            self.request_client = requests.get
        else:
            self.request_client = request_client
        self._load_jwk_keys()

    def _load_jwk_keys(self):
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        try:
            response = self.request_client(keys_url)
            self.jwk_keys = response.json()["keys"]
        except requests.exceptions.RequestException as e:
            raise FlaskAWSCognitoError(str(e)) from e

    @staticmethod
    def _extract_headers(token):
        try:
            headers = jwt.get_unverified_headers(token)
            return headers
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    def _find_pkey(self, headers):
        kid = headers["kid"]
        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(self.jwk_keys)):
            if kid == self.jwk_keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise TokenVerifyError("Public key not found in jwks.json")
        return self.jwk_keys[key_index]

    @staticmethod
    def _verify_signature(token, pkey_data):
        try:
            # construct the public key
            public_key = jwk.construct(pkey_data)
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit(".", 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise TokenVerifyError("Signature verification failed")

    @staticmethod
    def _extract_claims(token):
        try:
            claims = jwt.get_unverified_claims(token)
            return claims
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    @staticmethod
    def _check_expiration(claims, current_time):
        if not current_time:
            current_time = time.time()
        if current_time > claims["exp"]:
            raise TokenVerifyError("Token is expired")  # probably another exception

    def _check_audience(self, claims):
        # and the Audience  (use claims['client_id'] if verifying an access token)
        audience = claims["aud"] if "aud" in claims else claims["client_id"]
        if audience != self.user_pool_client_id:
            raise TokenVerifyError("Token was not issued for this audience")

    def verify(self, token, current_time=None):
        """ https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py """
        if not token:
            raise TokenVerifyError("No token provided")

        headers = self._extract_headers(token)
        pkey_data = self._find_pkey(headers)
        self._verify_signature(token, pkey_data)

        claims = self._extract_claims(token)
        self._check_expiration(claims, current_time)
        self._check_audience(claims)

        self.claims = claims 
        return claims
```

- The username is passed to the HomeActivity service as shown below:

![image](https://user-images.githubusercontent.com/1112540/226072401-8a8151ce-bae4-4f2d-a8ce-ef7bdefcaa08.png)

When the user is authenticated, the extra_crud object is pushed into the arrays

![image](https://user-images.githubusercontent.com/1112540/226072416-bdb8ac81-e9b2-4f04-afad-e5796e03b55f.png)

















