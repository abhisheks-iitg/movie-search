from handler.movie_ingestor import lambda_handler

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
for i in range(1, 2):
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
    if i % 10 == 0:
        print(f" Consumed {i}")
    i = i+1