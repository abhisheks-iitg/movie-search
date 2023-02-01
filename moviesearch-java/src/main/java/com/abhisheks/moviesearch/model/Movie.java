package com.abhisheks.moviesearch.model;

import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;

import java.util.List;

@Document(indexName="#{@applicationConfig.getIndexName()}")
public class Movie {

    @Field(type = FieldType.Text, name = "title")
    private String title;

    @Field(type = FieldType.Integer, name = "year")
    private Integer year;

    @Field(type = FieldType.Text, name = "cast")
    private List<String> cast;

    @Field(type = FieldType.Text, name = "genres")
    private List<String> genres;

    /*public String getId() {
        return _id;
    }

    public void setId(String _id) {
        this._id = _id;
    }*/

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public Integer getYear() {
        return year;
    }

    public void setYear(Integer year) {
        this.year = year;
    }

    public List<String> getCast() {
        return cast;
    }

    public void setCast(List<String> cast) {
        this.cast = cast;
    }

    public List<String> getGenres() {
        return genres;
    }

    public void setGenres(List<String> genres) {
        this.genres = genres;
    }
}
