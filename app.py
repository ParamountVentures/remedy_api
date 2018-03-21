from functools import wraps
from flask import Flask, request, jsonify, Response
from orm.models import *
from orm.orm import create_session
from sqlalchemy import func
from datetime import datetime
import os 

# Session
conn = os.environ['PG_CONN'] if "PG_CONN" in os.environ else 'docker_local'


# App 
app = Flask(__name__)
app.config['DEBUG'] = True

# Auth
def check_auth(username, password):
  return username==os.environ['AUTH_USER'] and password==os.environ['AUTH_PASSWORD']

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# API
@app.route('/', methods=['GET'])
def index():
  return "it works"

@app.route('/api/v1/enquiries', methods=['GET'])
@requires_auth
def enquiries():
  session = create_session(Base, conn)

  ### Call topics
  categories = ["FOI", "FOI Review", "FOI Form Request", "EIR"]

  # Set up query
  q = (
      RemedyCase.query
      .filter(RemedyCase.call_topic_category_1.in_(categories))
      .group_by(RemedyCase.call_topic_category_1, func.date_trunc('day', RemedyCase.call_opened_date_time))
      .with_entities(RemedyCase.call_topic_category_1, func.date_trunc('day', RemedyCase.call_opened_date_time).label('date'), func.count(RemedyCase.call_topic_category_1).label('count'))
      .order_by(func.date_trunc('day', RemedyCase.call_opened_date_time).desc())
      )

  if request.args.get('start'):
    date_string = request.args.get('start')
    date = datetime.strptime(date_string, "%Y-%m-%d")
    q = q.filter(RemedyCase.call_opened_date_time > date)
  if request.args.get('end'):
    date_string = request.args.get('end')
    date = datetime.strptime(date_string, "%Y-%m-%d")
    q = q.filter(RemedyCase.call_opened_date_time < date)

    # Per page
  if request.args.get('per_page'):
    if int(request.args.get('per_page')) > 500:
      per_page = 500
    else:
      per_page = request.args.get('per_page')
  else:
    per_page = 100

  #offset
  if request.args.get('page'):
    page = request.args.get('page')
    q = q.offset(int(per_page) * int(page))
  else:
    page = 1

  # Limit per page
  q = q.limit(per_page)
  print('before results')
  results = q.all()
  print('after results')
  print("queried results")
  data = {'meta':{}, 'data':[]}
  ## Add meta
  data['meta'] = {
  "page": page,
  "returned": len(results)
  }
  schema = ApiSchema()
  for r in results:
    r = schema.dump(r)
    data['data'].append(r.data)
  return jsonify(data)

  ### Close session
  session.close
