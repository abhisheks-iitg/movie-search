from handler.movie_ingestor import lambda_handler

lambda_handler({
  "detail": {
    "bucket": {
      "name": "ww-movie-database"
    },
    "object": {
     "key": "movie.json",
      "size": 105
    }
  }}, None)