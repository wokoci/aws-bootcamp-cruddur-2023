from datetime import datetime, timedelta, timezone
from lib.db import db
import logging
logger = logging.getLogger("LOGGER")

# from opentelemetry import trace
# tracer = trace.get_tracer("home.activity.tracer")
class HomeActivities:
  def run(cognito_user_id = None):
      print("******HOME ACTIVITY? **********")
      logger.info("HomeActivities")
      # with tracer.start_as_current_span("home-activites-mock-data"):

      sql = db.template('activities', 'home')
      results = db.query_array_json(sql)
      return results