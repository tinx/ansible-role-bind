$TTL    604800
@       IN      SOA     nope.example.com. admin.nyc3.example.com. (
                  3     ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL

                        IN       NS     ns1.nope.example.com.

ns1.nope.example.com.   IN      A       10.40.0.4

www.nope.example.com.   IN      A       10.40.0.12
