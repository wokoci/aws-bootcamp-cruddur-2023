# Week 4 — Postgres and RDS

# Week 4 - Postgresql

- Requires postgresql setup
    - provision a RDS Instance
        - use standard create option as against easy create in RDS
    - use free tiers to reduce cost
    - good practice to use secrete manager to manager you DB password
        - this cost $1 / month I think
        - command to provision an instance
        
        ```bash
        aws rds create-db-instance \
          --db-instance-identifier cruddur-db-instance \
          --db-instance-class db.t3.micro \
          --engine postgres \
          --engine-version  14.6 \
          --master-username root \
          --master-user-password Jame34qrq4f3q4q** \
          --allocated-storage 20 \
          --availability-zone us-east-1a \
          --backup-retention-period 0 \
          --port 5432 \
          --no-multi-az \
          --db-name cruddur \
          --storage-type gp2 \
          --publicly-accessible \
          --storage-encrypted \
          --enable-performance-insights \
          --performance-insights-retention-period 7 \
          --no-deletion-protection
        ```
        
    - it is a good practice to use a different port from your Postgresql port to reduce attack surface area
        - default port is `5432`
    - user secrete manager to maintain password and rotate the passwords to improve security
    - authentication methods provided by AWS RDS include
        - Password authentication
            - choose your passwords to use
        - Password and IAM authentication
            - provided by IAM
            - may be good for low use applications maybe inside a VPC
        - Password and Kerberos authentication
            - using active directory
    - good idea in practice to enable deletion protection
    - good idea to set character set when creating your instance
    - good practice to take backed up database before delete in case you need it back at some point
- Create a postgresql instance
    - paste the command from above
        - should create an RDS instance
            - part output
            
            
           ![image](https://user-images.githubusercontent.com/1112540/230208592-a6839a82-74d2-44fb-8480-ef74c03b3ca7.png)

            

- Bring up the app with `docker compose up`
    - confirm that the RDS instance is up
    - temporarily stop your RDS instance
        - note that it will restart after 7 days
- Access Postgres running locally in docker
    - connect to postgresql with `psql`
        - 
        
        ```bash
        psql -Upostgres --host localhost
        # enter password when prompted to login 
        ```
        
    - `\l` to see a list of databases
    - `\dt` to describe tables
    - see postgresql doc for more info on commands to use
- create database
    - use `CREATE database cruddur;`
        - listing with database created
        
        ![image](https://user-images.githubusercontent.com/1112540/230208700-a9b1085a-b81e-4eb9-8eb8-561cb60007a1.png)

        
- Next, we need to seed the cruddur database
    - create a folder called db and put schema.sql in that folder
    - sql command to import the `.sql` script is
        - the sql file needs to be populated and needs a UUID
        
        ```bash
        psql cruddur < db/schema.sql -h localhost -U postgres
        # data will be imported after providing password
        ```
        
    - uuid will be created with an extension
        - uuid makes identiying users more difficult
        
        ```sql
        CREATE EXTENSION "uuid";
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        ```
        
    - Postgresql comes with extensions that can be turned on like the above
    - They also need to be turned on in AWS
    - Add the above lines for extensions into the schema.sql file
        - 
        
        ```sql
        
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        ```
        
    - run the following command to execute the above in Postgress
        - `psql cruddur < backend-flask/db/schema.sql -h localhost -U postgres`
    - connecting to the postgres server with connection url string
        - use :
            - 
            
            ```sql
            export CONNECTION_URL="postgresql://postgres:paSSmord@localhost:5432/cruddur
            ```
            
        - exporting this will allow for easier access to postgress
        - to test, run as follows”
            - `psql postgresql://postgres:password@localhost:5432/cruddur`
        - if logged in automatically, then the connection string works
        - Log in using the connection url
            - `psql CONNECTION_URL`
    - Connection to aws Postgresql connection can also be setup using connection url as follows:
        - test in same way as local postgresql
        
        ```sql
        PRODUCTION_CONNECTION_URL=CONNECTION_URL="postgresql://crudduradmin:GoodPassord@cruddur-db-instance.cf2feuqesjfr.us-east-1.rds.amazonaws.com:5432/cruddur"
        ```
        
- We also need some bash scripts to perform some needed actions
    - create a bin folder in backend-flask
        - add a shell script in the above folder name
            - `db-create`
                - 
                
                ```bash
                #!/usr/bin/bash
                
                echo "CREATE-DB"
                NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
                psql $NO_DB_CONNECTION_URL -c "CREATE database cruddur;"
                ```
                
            - `db-drop`
                - make file executable `chmod u+x ./bin/db-drop`
                - execute script `./bin/db-drop`
                
                ```bash
                #!/usr/bin/bash
                
                echo "DB-drop"
                NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
                psql $NO_DB_CONNECTION_URL -c "DROP database cruddur;"
                ```
                
            - `schema-load`
                - With this we load seed data into the database
                - also note that the db has to exist before you can load it with seed data
                
                ```bash
                #!/usr/bin/bash
                
                echo "DB-Schema-load"
                psql $CONNECTION_URL cruddur < db/schema.sql
                ```
                
        - note: files have no extension
        - The bash files are not executable outside the location where thy are saved
            - to be able to execute script from other location
                - we can use `realpath`
                - example
                    - `echo $(realpath .)` will show the oath to location of  file
                        - This can be used to get the real location of the script
                            
                            ![image](https://user-images.githubusercontent.com/1112540/230208894-a202e31a-ac74-463a-bc07-7771f7960fdb.png)
                            
                    - with the final location of the script obtained, we can feed it into the `psql` connection call as shown below:
                        - 
                        
                        ```bash
                        #!/usr/bin/bash
                        schema_path=$(realpath .)/backend-flask/db/schema.sql
                        echo $schema_path
                        echo "DB-Schema-load"
                        psql $CONNECTION_URL cruddur < $schema_path
                        ```
                        
                    - this can then be called as:
                        - `backend-flask/bin/db-load`
        - Checking if env is prod
            - should check if the env is production or development and connect to the correct instance
            - the script from above is rewritten to the following
                - 
                
                ```bash
                #!/usr/bin/bash
                schema_path=$(realpath .)/backend-flask/db/schema.sql
                echo $schema_path
                echo "DB-Schema-load"
                if [ "$1" = "prod" ]; then
                echo "Connecting to production instance of DB instance"
                    CON_URL = $PROD_CONNECTION_URL
                else
                    echo "Connection to development instance"
                    CON_URL=$CONNECTION_URL
                fi
                psql $CONNECTION_URL cruddur < $schema_path
                ```
                
            - the above is called with prod if it’s to connect to prod
                - `./backend-flask/bin/db-load`
                - Note that the db needs to have been created and running
        - `creating tables
            - we will beed 2 tables
                - users
                - activities
            - The following will be used to create the tables.
            - table names are prefixed with public which is a concept specific to Prostgresql
            
            ```bash
            CREATE TABLE public.users (
              uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
              display_name text,
              handle text
              cognito_user_id text,
              created_at TIMESTAMP default current_timestamp NOT NULL
            );
            
            CREATE TABLE public.activities (
              uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
              message text NOT NULL,
              replies_count integer DEFAULT 0,
              reposts_count integer DEFAULT 0,
              likes_count integer DEFAULT 0,
              reply_to_activity_uuid integer,
              expires_at TIMESTAMP,
              created_at TIMESTAMP default current_timestamp NOT NULL
            );
            ```
            
        - content of the table is driven by the `openapi` doc for the application
        - we check if the table exists before loading or creating table
            - us `DROP TABLE IF Exists` for both tables as follows:
                - has to be at top of scripts above tables to be manipulated
                
                ```bash
                DROP TABLE IF EXISTS public.user;
                DROP TABLE If EXISTS  public.activities ;
                ```
                
        - We can also create another bash script to connect automatically to the database
            - 
            
            ```bash
            #!/usr/bin/bash
            psql $CONNECTION_URL
            ```
            
    - the application also need actual data to work with
        - we need to seed the database
    - we create a script for this with the following content
        - 
        
        ```bash
        #!/usr/bin/bash
        
        CYAN='\033[1;36m'
        NO_COLOR='\033[0m'
        LABEL="db-seed"
        printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
        echo "== db-Seed"
        
        seed_path=$(realpath .)/backend-flask/db/seed.sql
        echo $seed_path
        echo "== db-seed"
        
        if [ "$1" = "prod" ]; then
        echo "Connecting to production instance of DB instance"
            CON_URL = $PROD_CONNECTION_URL
        else
            echo "==Connection to development instance"
            CON_URL=$CONNECTION_URL
        fi
        psql $CONNECTION_URL cruddur < $seed_path
        ```
        
    - above script will load seed data from the seed.sql file
        - sql file loaded
        
        ```bash
        -- this file was manually created
        INSERT INTO public.users (display_name, handle, cognito_user_id)
        VALUES
          ('Andrew Brown', 'andrewbrown' ,'MOCK'),
          ('Andrew Bayko', 'bayko' ,'MOCK');
        
        INSERT INTO public.activities (user_uuid, message, expires_at)
        VALUES
          (
            (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
            'This was imported as seed data!',
            current_timestamp + interval '10 day'
          )
        ```
        

- Query database & select from table
    - start and load data into db instance
    - 
    
    ```bash
    ./backend-flask/bin/db-create
    ./backend-flask/bin/db-load
    ./backend-flask/bin/db-seed
    select * from Users;
    ```
    
    - 
    
      ![image](https://user-images.githubusercontent.com/1112540/230209026-a0fbcac4-f87f-40fa-a919-701f5269df1f.png)

    
    - Connection to the db can also be done with other graphical tools and VSCode provides a convenient one we can use
- See DB processes
    - It is not possible to drop a db that has other connections to it
    - to see the connections, we can use:
        - can be put in a bash file for convinience
        
        ```bash
        #!/usr/bin/bash
        
        CYAN='\033[1;36m'
        NO_COLOR='\033[0m'
        LABEL="db-sessions"
        printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
        echo "== db-sessions"
        
        if [ "$1" = "prod" ]; then
        echo "Connecting to production instance of DB instance"
            URL = $PROD_CONNECTION_URL
        else
            echo "==Connection to development instance"
            URL=$CONNECTION_URL
        fi
        
        # psql $CONNECTION_URL cruddur < $seed_path
        
        NO_DB_URL=$(sed 's/\/cruddur//g' <<<"$URL")
        psql $NO_DB_URL -c "select pid as process_id, \
               usename as user,  \
               datname as db, \
               client_addr, \
               application_name as app,\
               state \
        from pg_stat_activity;"
        ```
        
        - running the above produces the connections to the the db
            - 
            
            ![image](https://user-images.githubusercontent.com/1112540/230209116-253d12a1-9945-4124-bdfd-a208c5e00508.png)
            
    - setup a `db-setup` script to setup all needed content in db
        - the script with drop and recreate the db instance
        
        ```bash
        #!/usr/bin/bash
        
        -e.   # do not proceed to next step on failure
        
        CYAN='\033[1;36m'
        NO_COLOR='\033[0m'
        LABEL="db-setup"
        printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
        echo "== db-setup"
        
        # bin-path="$(realpath .)/backend-flask/bin
        bin_path="$(realpath .)/backend-flask/bin"
        
        source "$bin_path/db-drop"
        source "$bin_path/db-create"
        source "$bin_path/db-load"
        source "$bin_path/db-seed"
        ```
        
        - the above script can be executes as
            - `./backend-flask/bin/db-setup`
            - this most not be run in production
- Drivers to connect to postgres
    - postgres uses psycoppg 3
    - add to `requirements.txt` files
        - install with pip
        
        ```bash
        psycopg[binary]
        psycopg[pool]
        ```
        
    - good idea to use connection pooling with the db connection
    - create a file named `[db.py](http://db.py)` and add the following content into it
        - connection url has to be passed in via docker compose file
            - 
            
            ![image](https://user-images.githubusercontent.com/1112540/230209210-b3656fd4-354c-46cd-9d43-3c3232fa8b8b.png)
            
        - the connection pool can then be used inside the activities in the backend
        - the connection pool can be defined in `lib.db` folder
            - 
            
            ```bash
            from psycopg_pool import ConnectionPool
            import os
            
            def query_wrap_object(template):
              sql = f'''
              (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
              {template}
              ) object_row);
              '''
              return sql
            
            def query_wrap_array(template):
              sql = f'''
              (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'{{}}'::json) FROM (
              {template}
              ) array_row);
              '''
              return sql
            
            connection_url = os.getenv("CONNECTION_URL")
            pool = ConnectionPool(connection_url)
            ```
            
        - import into `home.activities.py`
            - the pool can then be imported into the home activity and the dummy code replaces as shown below:
            
            ```python
            from datetime import datetime, timedelta, timezone
            from lib.db import pool, query_wrap_array
            
            # from opentelemetry import trace
            # tracer = trace.get_tracer("home.activity.tracer")
            class HomeActivities:
              def run(cognito_user_id = None):
                  print("******HOME ACTIVITY? **********")
                #logger.info("HomeActivities")
                  # with tracer.start_as_current_span("home-activites-mock-data"):
            
                  sql = query_wrap_array("""
                  SELECT
                    activities.uuid,
                    users.display_name,
                    users.handle,
                    activities.message,
                    activities.replies_count,
                    activities.reposts_count,
                    activities.likes_count,
                    activities.reply_to_activity_uuid,
                    activities.expires_at,
                    activities.created_at
                  FROM public.activities
                  LEFT JOIN public.users ON users.uuid = activities.user_uuid
                  ORDER BY activities.created_at DESC
                  """)
                  print(sql)
                  with pool.connection() as conn:
                    with conn.cursor() as cur:
                      cur.execute(sql)
                      # this will return a tuple
                      # the first field being the data
                      json = cur.fetchone()
                      print(json)
                  return json[0]
            ```
            
        - with the above changes, data will be returned to the home activity
            - 
            
            ![image](https://user-images.githubusercontent.com/1112540/230209388-88849c34-0ba8-4517-8979-2096d82475d8.png)

            
- Connecting and using aws RDS from local env
    - set the env vars for prod rds instance
        - 
        
        ```python
        export PROD_CONNECTION_URL="postgresql://root:Jaergaefaaafad@cruddur-db-instance.cf2feuqesjfr.us-east-1.rds.amazonaws.com/cruddur"
        gp env PROD_CONNECTION_URL="postgresql://root:Jaergaefaaafad@cruddur-db-instance.cf2feuqesjfr.us-east-1.rds.amazonaws.com/cruddur"
        ```
        
    - We are not able to connect to the remote instance as there is no firewall permission from gitpod
        - specify firewall rules in EC2>Security groups
            - the IP of gitpod can be sound and set as an env var using
                - export `GITPOD_IP=$(curl ifconfig.me)`
                
                ```
                #! /usr/bin/bash
                
                -e
                CYAN='\033[1;36m'
                NO_COLOR='\033[0m'
                LABEL="rds-SG-update"
                printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
                echo "== rds-SG-update"
                
                aws ec2 modify-security-group-rules \
                	--group-id $DB_SG_ID \
                	--security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
                ```
                
            - We also need to set the env vars for the seciruty group ID
                - SG ID :  `sgr-0999e25140cd8d648`
                
                ```python
                export DB_SG_ID="sg-08dcba5316ae3aedf"
                gp env DB_SG_ID="sg-08dcba5316ae3aedf"
                export DB_SG_RULE_ID="sgr-0999e25140cd8d648"
                gp env DB_SG_RULE_ID="sgr-0999e25140cd8d648"
                ```
                
                To make the IP dynamic, use the following aws cli Commanf
                
                ```bash
                #!/bin/bash
                aws ec2 modify-security-group-rules \
                    --group-id $DB_SG_ID \
                    --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
                ```
                
            - The above can be tested by changing the IP of rds and running the command to see if it is set to the IP of gitpod
                - this needs to run each time gitpod starts up
                - we need to update gitpod.yml for this to work
                - changes to gitpod below
                
                ![image](https://user-images.githubusercontent.com/1112540/230209514-cdaa69c6-85a4-41d0-bfb6-2e3bf6b6e393.png)

                
            - The output of the above needs to be dynamically set in the securlty group based on the security group ID
            - when gitpod starts up will update the SG
                
                ![image](https://user-images.githubusercontent.com/1112540/230209570-0f1d2cd5-1a0a-401c-8db3-b4ef1f5b0b22.png)

                
        - Below is the security group setting
        
        ![image](https://user-images.githubusercontent.com/1112540/230209626-792bd989-727b-44b8-bf0a-fdf1eff12b7b.png)
        
        - attempting to connect with firewall rule will resulting hanging connection attempt
    - With all the above setting, it will be possible to connect to the remote rds instance
        
        ![image](https://user-images.githubusercontent.com/1112540/230209685-e818ef22-a3cb-479f-b117-120e9607ab2c.png)

        

- Update DB_CONNECT script to allow for selective connection to prod or dev instance of postgresql
    - 
    
    ```bash
    #!/usr/bin/bash
    
    CYAN='\033[1;36m'
    NO_COLOR='\033[0m'
    LABEL="DB-Connect"
    printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
    echo "== DB-Connect"
    
    if [ "$1" = "prod" ]; then
    echo "==Connecting to production instance of DB instance"
        CON_URL=$PROD_CONNECTION_URL
    else
        echo "==Connection to development instance"
        CON_URL=$CONNECTION_URL
    fi
    psql $CON_URL
    ```
    
- Connecting to prod rds instance will not return any data as there is no data in that environment
    - to load data to the remote rds
        - we use `load load` shell script pointing to `prod`
        - the below can be called using `./db-load prod` to load data into prod
        
        ```bash
        #!/usr/bin/bash
        
        CYAN='\033[1;36m'
        NO_COLOR='\033[0m'
        LABEL="db-schema-load"
        printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
        echo "== DB-Schema-load"
        
        schema_path=$(realpath .)/db/schema.sql
        echo $schema_path
        echo "== DB-Schema-load"
        
        if [ "$1" = "prod" ]; then
        echo "Connecting to production instance of DB instance"
            CON_URL=$PROD_CONNECTION_URL
        else
            echo "==Connection to development instance"
            CON_URL=$CONNECTION_URL
        fi
        psql $CONNECTION_URL cruddur < $schema_path
        ```
        
        - 
- **Using Lambda function to add data to RDS using a custom authoriser**
    - we need to be able to add the cognito user as well as that users id to
    - this needs to be compiled into the lambda function
    - steps
        - create lambda function in same VPC
        - add lambda layer of `psycopg2`
        - add the following env vars
            - we export the following env vars for the lambda function code
            - these have to be set for the lambda function
            
            ```bash
            PG_HOSTNAME='cruddur-db-instance.cf2feuqesjfr.us-east-1.rds.amazonaws.com'
            PG_DATABASE='cruddur'
            PG_USERNAME='root'
            PG_PASSWORD='Jaergaefaaafad'
            ```
            
        - 
        - 
        - the following is the lambda function code
            - 
            
            ```python
            import os
            import psycopg2
            
            def lambda_handler(event, context):
                user = event['request']['userAttributes']
                user_display_name = user['name']
                user_email = user['email']
                user_handle = user['preferred_username']
                user_cognito_id = user['sub']
            
                print('userAttributes')
                print(user)
                
                try:
                    sql = """  
                        INSERT INTO users (
                            display_name, 
                            email,
                            handle, 
                            cognito_user_id) 
                        VALUES (
                            %s, 
                            %s, 
                            %s, 
                            %s
                        )
                    """
                    conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
                    with conn.cursor() as cur:
                        print(conn)
                        cur.execute(sql, (user_display_name, user_email, user_handle, user_cognito_id))
                        conn.commit()
                        print(f"{cur.rowcount} row(s) inserted.")
                
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                    
                finally:
                    if conn is not None:
                        conn.close()
                        print('Database connection closed.')
                        
                return event
            ```
            
        - add a reference to the lambda code
        - `arn:aws:lambda:ca-central-1:<aws_account_num_here>:layer:psycopg2-py38:1`
            - this should be under `specify an arn`
                - more layers for other regions can be found [here](https://github.com/jetbridge/psycopg2-lambda-layer)
        - Add trigger
            - we need a cognito trigger to perform the action
            - go to cognito user pool properties
                - add a  trigger
                - should take place on post confirmation trigger
                
                ![image](https://user-images.githubusercontent.com/1112540/230210949-dd3d47e7-82e6-4dd2-ad35-db113d20ff96.png)
                
            - If all the code is entered correctly should allow the user sign up
                - 
                
                ![Untitled](Week%204%20-%20Postgresql%203a34140070574c54ba30c7dd4cb93806/Untitled%2012.png)
                
                - and the user should be logged in, though there will be not content on first login
                - the table in aws rds is updated as shown below:
                    - 
                    
                    ![image](https://user-images.githubusercontent.com/1112540/230210375-f8406222-e1bb-4208-9177-af74fedc6255.png)
                    
                - we can also do a `select * from users` and get the details that were inserted into the users tables
                
                ![image](https://user-images.githubusercontent.com/1112540/230210335-9ae730b6-1131-4d4e-abc8-7d4897b03135.png)
                
                - The database has to exist for data to be inserted into it
    - **Adding repost**
        - we need to update [createActivity.py](http://createActivity.py) file with the needed sql to polulate the table and return data
        - The following changes are made to allow for activities to be created
            - `create activity`
                - 
                
                ```python
                from datetime import datetime, timedelta, timezone
                
                from lib.db import db
                
                class CreateActivity:
                  def run(message, user_handle, ttl):
                    model = {
                      'errors': None,
                      'data': None
                    }
                
                    now = datetime.now(timezone.utc).astimezone()
                
                    if (ttl == '30-days'):
                      ttl_offset = timedelta(days=30) 
                    elif (ttl == '7-days'):
                      ttl_offset = timedelta(days=7) 
                    elif (ttl == '3-days'):
                      ttl_offset = timedelta(days=3) 
                    elif (ttl == '1-day'):
                      ttl_offset = timedelta(days=1) 
                    elif (ttl == '12-hours'):
                      ttl_offset = timedelta(hours=12) 
                    elif (ttl == '3-hours'):
                      ttl_offset = timedelta(hours=3) 
                    elif (ttl == '1-hour'):
                      ttl_offset = timedelta(hours=1) 
                    else:
                      model['errors'] = ['ttl_blank']
                
                    if user_handle == None or len(user_handle) < 1:
                      model['errors'] = ['user_handle_blank']
                
                    if message == None or len(message) < 1:
                      model['errors'] = ['message_blank'] 
                    elif len(message) > 280:
                      model['errors'] = ['message_exceed_max_chars'] 
                
                    if model['errors']:
                      model['data'] = {
                        'handle':  user_handle,
                        'message': message
                      }   
                    else:
                      expires_at = (now + ttl_offset)
                      uuid = CreateActivity.create_activity(user_handle,message,expires_at)
                
                      object_json = CreateActivity.query_object_activity(uuid)
                      model['data'] = object_json
                    return model
                
                  def create_activity(handle, message, expires_at):
                    sql = db.template('activities','create')
                    uuid = db.query_commit(sql,{
                      'handle': handle,
                      'message': message,
                      'expires_at': expires_at
                    })
                    return uuid
                  def query_object_activity(uuid):
                    sql = db.template('activities','object')
                    return db.query_object_json(sql,{
                      'uuid': uuid
                    })
                ```
                
            - additional file was added to handle `DB` actions
                - 
                
                ```python
                from psycopg_pool import ConnectionPool
                import os
                import re
                import sys
                from flask import current_app as app
                import logging
                logger =logging.getLogger("logger")
                
                class Db:
                  def __init__(self):
                    self.init_pool()
                
                  def template(self,*args):
                    pathing = list((app.root_path,'db','sql',) + args)
                    pathing[-1] = pathing[-1] + ".sql"
                
                    template_path = os.path.join(*pathing)
                
                    green = '\033[92m'
                    no_color = '\033[0m'
                    print("\n")
                    print(f'{green} Load SQL Template: {template_path} {no_color}')
                
                    with open(template_path, 'r') as f:
                      template_content = f.read()
                    return template_content
                
                  def init_pool(self):
                    connection_url = os.getenv("CONNECTION_URL")
                    logger.debug("Bool initilised")
                    self.pool = ConnectionPool(connection_url)
                  # we want to commit data such as an insert
                  # be sure to check for RETURNING in all uppercases
                  def print_params(self,params):
                    blue = '\033[94m'
                    no_color = '\033[0m'
                    print(f'{blue} SQL Params:{no_color}')
                    for key, value in params.items():
                      print(key, ":", value)
                
                  def print_sql(self,title,sql):
                    cyan = '\033[96m'
                    no_color = '\033[0m'
                    print(f'{cyan} SQL STATEMENT-[{title}]------{no_color}')
                    print(sql)
                  def query_commit(self,sql,params={}):
                    self.print_sql('commit with returning',sql)
                
                    pattern = r"\bRETURNING\b"
                    is_returning_id = re.search(pattern, sql)
                
                    try:
                      with self.pool.connection() as conn:
                        cur =  conn.cursor()
                        cur.execute(sql,params)
                        if is_returning_id:
                          returning_id = cur.fetchone()[0]
                        conn.commit() 
                        if is_returning_id:
                          return returning_id
                    except Exception as err:
                      self.print_sql_err(err)
                  # when we want to return a json object
                  def query_array_json(self,sql,params={}):
                    self.print_sql('array',sql)
                
                    wrapped_sql = self.query_wrap_array(sql)
                    with self.pool.connection() as conn:
                      with conn.cursor() as cur:
                        cur.execute(wrapped_sql,params)
                        json = cur.fetchone()
                        return json[0]
                  # When we want to return an array of json objects
                  def query_object_json(self,sql,params={}):
                
                    self.print_sql('json',sql)
                    self.print_params(params)
                    wrapped_sql = self.query_wrap_object(sql)
                
                    with self.pool.connection() as conn:
                      with conn.cursor() as cur:
                        cur.execute(wrapped_sql,params)
                        json = cur.fetchone()
                        if json == None:
                          "{}"
                        else:
                          return json[0]
                  def query_wrap_object(self,template):
                    sql = f"""
                    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
                    {template}
                    ) object_row);
                    """
                    return sql
                  def query_wrap_array(self,template):
                    sql = f"""
                    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
                    {template}
                    ) array_row);
                    """
                    return sql
                  def print_sql_err(self,err):
                    # get details about the exception
                    err_type, err_obj, traceback = sys.exc_info()
                
                    # get the line number when exception occured
                    line_num = traceback.tb_lineno
                
                    # print the connect() error
                    print ("\npsycopg ERROR:", err, "on line number:", line_num)
                    print ("psycopg traceback:", traceback, "-- type:", err_type)
                
                    # print the pgcode and pgerror exceptions
                    print ("pgerror:", err.pgerror)
                    print ("pgcode:", err.pgcode, "\n")
                db = Db()
                ```
                
                - Home activities was also updated
                    - 
                    
                    ```python
                    from datetime import datetime, timedelta, timezone
                    from lib.db import db
                    import logging
                    logger = logging.getLogger("LOGGER")
                    
                    # from opentelemetry import trace
                    # tracer = trace.get_tracer("home.activity.tracer")
                    class HomeActivities:
                      def run(cognito_user_id = None):
                          logger.info("HomeActivities")
                          # with tracer.start_as_current_span("home-activites-mock-data"):
                    
                          sql = db.template('activities', 'home')
                          results = db.query_array_json(sql)
                          return results
                    ```
                    
                - additional files for sql activities with following structure is alos added
                    - 
                    
                    ![image](https://user-images.githubusercontent.com/1112540/230210256-dd7f2e94-644c-4c4d-9da1-263f315c9f8f.png)
                    
                    ```python
                    # create.sql
                    INSERT INTO public.activities (
                      user_uuid,
                      message,
                      expires_at
                    )
                    VALUES (
                      (SELECT uuid 
                        FROM public.users 
                        WHERE users.handle = %(handle)s
                        LIMIT 1
                      ),
                      %(message)s,
                      %(expires_at)s
                    ) RETURNING uuid;
                    ```
                    
                    - `home.sql`
                    
                    ```python
                    SELECT
                      activities.uuid,
                      users.display_name,
                      users.handle,
                      activities.message,
                      activities.replies_count,
                      activities.reposts_count,
                      activities.likes_count,
                      activities.reply_to_activity_uuid,
                      activities.expires_at,
                      activities.created_at
                    FROM public.activities
                    LEFT JOIN public.users ON users.uuid = activities.user_uuid
                    ORDER BY activities.created_at DESC
                    ```
                    
                    - `object.sql`
                    
                    ```python
                    SELECT
                      activities.uuid,
                      users.display_name,
                      users.handle,
                      activities.message,
                      activities.created_at,
                      activities.expires_at
                    FROM public.activities
                    INNER JOIN public.users ON users.uuid = activities.user_uuid 
                    WHERE 
                      activities.uuid = %(uuid)s
                    ```
                    
                    activities added shown below
                    
                    ![image](https://user-images.githubusercontent.com/1112540/230210182-74a8f09b-9174-4771-8c2f-75a98e1673f0.png)
