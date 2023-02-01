package com.abhisheks.moviesearch.search;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.query_dsl.BoolQuery;
import co.elastic.clients.elasticsearch._types.query_dsl.MatchQuery;
import co.elastic.clients.elasticsearch._types.query_dsl.Query;
import co.elastic.clients.elasticsearch.core.GetResponse;
import co.elastic.clients.elasticsearch.core.SearchRequest;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import com.abhisheks.moviesearch.model.Movie;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.io.IOException;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Class to support lookup of Movie entries from the Repository
 */

@Repository
public class MovieRepository {

    @Autowired
    private ElasticsearchClient elasticsearchClient;

    @Autowired
    private String indexName;


    public Movie getMovieById(String id) throws IOException {
        Movie movie = null;
        GetResponse<Movie> response = elasticsearchClient.get(
                g -> g.index(indexName)
                        .id(id),
                Movie.class
        );

        if (response.found()) {
            movie = response.source();
        } else {
        }
        return movie;
    }

    public List<Movie> getMovieByParams(Optional<String> title, Optional<String> year, Optional<String> cast, Optional<String> genres) throws IOException {
        List<Movie> movies = List.of();

        Query byTitle = getQuery("title", title);
        Query byYear = getQuery("year", year);
        Query byCast = getQuery("cast", cast);
        Query byGenres = getQuery("genres", genres);

        SearchRequest searchRequest = new SearchRequest.Builder().index(indexName)
                .query(q -> q
                        .bool(b -> {
                            BoolQuery.Builder builder = b;
                            builder = checkAndBuildQuery(builder, byTitle);
                            builder = checkAndBuildQuery(builder, byYear);
                            builder = checkAndBuildQuery(builder, byCast);
                            builder = checkAndBuildQuery(builder, byGenres);

                            return builder;
                        })).build();
        SearchResponse<Movie> response = elasticsearchClient.search(searchRequest, Movie.class);

        if (response.hits().hits().size() > 0) {
            List<Hit<Movie>> res = response.hits().hits();
            movies = res.stream().map(entry -> entry.source()).collect(Collectors.toList());
            //System.out.println("Movie Title is: " + movie.getTitle());
        } else {
            //System.out.println ("Movie not found");
        }
        return movies;
    }

    private BoolQuery.Builder checkAndBuildQuery(BoolQuery.Builder builder, Query byTitle) {
        if (byTitle != null) {
            builder = builder.should(byTitle);
        }
        return builder;
    }

    private Query getQuery(String fieldName, Optional<String> fieldValue) {
        Query byField = null;
        if (fieldValue.isPresent()) {
            byField = MatchQuery.of(m -> m
                    .field(fieldName)
                    .query(fieldValue.get())
            )._toQuery();
        }
        return byField;
    }
}