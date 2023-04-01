from datetime import datetime, timedelta, timezone
from lib.db import pool

# from opentelemetry import trace
# tracer = trace.get_tracer("home.activity.tracer")

class HomeActivities:
  def run(cognito_user_id = None):
      print("---INSIDE HOME ACTIVITY-------")
    # with tracer.start_as_current_span("home-activity") as outer_span:
    #   with tracer.start_as_current_span("inner-home-activity") as inner_span:
    #       outer_span.set_attribute("entering call", True)
    #       inner_span.set_attribute("in call", True)
    #       now = datetime.now(timezone.utc).astimezone()

      sql = """ 
      SELECT * FROM activities;  
      """
          
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          rows = cur.fetchall()
          for row in rows:
            print("------11--22-----")
            json = cur.fetchall()
            return json[0]

      # handle = results[0]['handle']
      # span = trace.get_current_span()
      # span.set_attribute("app.result_length", len(results))      
      # return results  

      