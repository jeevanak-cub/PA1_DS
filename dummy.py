





====================
file: README.md
====================
This project implements PA1 using pure TCP sockets. Buyer and Seller clients are CLI-based. Buyer and Seller servers are stateless and forward requests to backend Product and Customer databases. All persistent state (sessions, carts, products) is stored in backend databases. Sessions are maintained via session IDs with 5-minute inactivity timeout. All components run as independent processes on different ports.

====================
file: performance_notes.txt
====================
Run multiple buyer and seller clients concurrently using shell scripts. Measure response time using time.time() around client calls. Throughput measured as total operations / total time for 1000 API calls per client. Three scenarios tested: 1, 10, and 100 concurrent buyers/sellers. Increased contention and socket overhead explains reduced throughput at scale.
