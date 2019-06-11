docker run --rm -d --network pruebas  --name nginx -p 80:80 -p 81:81 \
-v $(pwd)/html:/usr/share/nginx/html \
 -v $(pwd)/sitios_nginx:/etc/nginx/conf.d \
 -v $(pwd)/html2:/usr/share/nginx/html2 nginx

