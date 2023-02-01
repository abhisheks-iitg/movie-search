package com.abhisheks.moviesearch.helper.ssl;

import javax.net.ssl.X509TrustManager;
import java.security.cert.X509Certificate;

//Trust All Certificate. For Testing only and not meant for Production

public class TrustAllManager implements X509TrustManager {
    public X509Certificate[] getAcceptedIssuers() {
        return null;
    }

    public void checkClientTrusted(X509Certificate[] certs,
                                   String authType) {
    }

    public void checkServerTrusted(X509Certificate[] certs,
                                   String authType) {
    }
}
