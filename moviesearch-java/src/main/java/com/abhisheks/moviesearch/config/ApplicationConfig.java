package com.abhisheks.moviesearch.config;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.ElasticsearchTransport;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import org.apache.http.HttpHost;
import org.apache.http.HttpResponseInterceptor;
import org.apache.http.entity.ContentType;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.nio.client.HttpAsyncClientBuilder;
import org.apache.http.message.BasicHeader;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestClientBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;

import java.util.List;

/**
 *  Application Configuration class
 */

@Configuration
public class ApplicationConfig {
    @Bean
    public RestClient getRestClient() {

        RestClientBuilder.HttpClientConfigCallback httpClientConfigCallback = (HttpAsyncClientBuilder httpClientBuilder) ->
                httpClientBuilder.setDefaultCredentialsProvider(new BasicCredentialsProvider())

                        .setDefaultHeaders(
                                List.of(
                                        new BasicHeader(
                                                HttpHeaders.CONTENT_TYPE, ContentType.APPLICATION_JSON.toString())))
                        .addInterceptorLast(
                                (HttpResponseInterceptor)
                                        (response, context) ->
                                                response.addHeader("X-Elastic-Product", "Elasticsearch"));
        var restClient =
                RestClient.builder(new HttpHost("elasticsearch", 9200, "http"))
                        .setHttpClientConfigCallback(httpClientConfigCallback)
                        .build();

        return restClient;
    }
    

    @Bean
    public ElasticsearchTransport getElasticsearchTransport() {
        return new RestClientTransport(getRestClient(), new JacksonJsonpMapper());
    }

    @Bean
    public ElasticsearchClient getElasticsearchClient(){
        ElasticsearchClient client = new ElasticsearchClient(getElasticsearchTransport());
        return client;
    }

    @Bean
    public String getIndexName() {
        return "abhisheks";
    }
}
