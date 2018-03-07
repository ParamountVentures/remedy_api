from flask import Flask, request, jsonify
from orm.models import *
from orm.orm import create_session
from sqlalchemy import func

# Session
session = create_session(Base, 'local')

# App 
app = Flask(__name__)
app.config['DEBUG'] = True

# API
@app.route('/api/v1/enquiries', methods=['GET'])
def enquiries():
  categories = ["FOI", "FOI Review", "FOI Form Request", "EIR"]

  # Set up query
  q = (
      RemedyCase.query
      .filter(RemedyCase.call_topic_category_1.in_(categories))
      .group_by(RemedyCase.call_topic_category_1, func.date_trunc('day', RemedyCase.call_opened_date_time))
      .with_entities(RemedyCase.call_topic_category_1, func.date_trunc('day', RemedyCase.call_opened_date_time).label('date'), func.count(RemedyCase.call_topic_category_1).label('count'))
      .order_by(func.date_trunc('day', RemedyCase.call_opened_date_time).desc())
      )

  # Per page
  if request.args.get('per_page'):
    if int(request.args.get('per_page')) > 500:
      per_page = 500
    else:
      per_page = request.args.get('per_page')
  else:
    per_page = 100

  # Limit per page
  q = q.limit(per_page)

  if request.args.get('page'):
    q = q.offset(int(per_page) * int(request.args.get('page')))
  if request.args.get('start'):
    q = q.filter(RemedyCase.call_opened_date_time > request.args.get('start'))
  if request.args.get('end'):
    q = q.filter(RemedyCase.call_opened_date_time < request.args.get('end'))

  results = q.all()
  data = {'data':[]}
  schema = ApiSchema()
  for r in results:
    r = schema.dump(r)
    data['data'].append(r.data)
  return jsonify(data)