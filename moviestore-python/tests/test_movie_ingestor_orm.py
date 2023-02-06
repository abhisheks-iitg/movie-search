from handler.movie_ingestor_orm import lambda_handler

"""
lambda_handler({
      "detail": {
        "bucket": {
          "name": "ww-movie-database"
        },
        "object": {
         "key": "test.json",
          "size": 105
        }
      }}, None)
"""
for i in range(1, 500):
    lambda_handler({
      "detail": {
        "bucket": {
          "name": "ww-movie-database"
        },
        "object": {
         "key": "movies--" + str(i) + ".json",
          "size": 105
        }
      }}, None)