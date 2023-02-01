package com.abhisheks.moviesearch.controller;

import com.abhisheks.moviesearch.model.Movie;
import com.abhisheks.moviesearch.search.MovieRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.util.List;
import java.util.Optional;

@RestController
public class MovieRestController {

        @Autowired
        private MovieRepository repo;

        @GetMapping("/search")
        public ResponseEntity<Object> getMovieByParams(@RequestParam Optional<String> title, @RequestParam Optional<String> year, @RequestParam Optional<String> cast, @RequestParam Optional<String> genres) throws IOException {
            List<Movie> movies = repo.getMovieByParams(title, year, cast, genres);
            return new ResponseEntity<>(movies, HttpStatus.OK);
        }
    }