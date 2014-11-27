Burp-Response-Handler
=====================
This is a burp extension that will get the respones of empty requests in Burp's Sitemap. When spidering a host,
it happens that some requests are queued but never get actually requested by the spider. These usually show up
as grey nodes in the sitemap. This extension takes care of those by requesting each of them and adding its
response to the sitemap. No more gray nodes in Burp's sitemap!
