$TTL    604800
@       IN      SOA     yep.example.com. admin.nyc3.example.com. (
                  3     ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL

                        IN       NS     ns1.yep.example.com.

ns1.yep.example.com.    IN      A       10.40.0.4

www.yep.example.com.    IN      A       10.40.0.12
