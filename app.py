

from src import app


if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc")
# 
# video(order = '1', type ='video')
# document = (order = '1a', type = 'doc')
# result = Resource.query.filter_by(like(order = 1)).filter_by(type="doc").all()
