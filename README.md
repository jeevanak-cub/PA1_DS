# Ecomm (TCP-Based)

This project implements a distributed online marketplace using a socket-based TCP client–server architecture. The system consists of independent services that communicate via JSON messages over TCP. The design follows a stateless frontend and stateful backend model, where all persistent application state is maintained in backend database services.

---

## Project Goal

The goal of this assignment is to design and implement a distributed system using TCP sockets that supports buyer–seller interactions in an online marketplace

---

##  System Architecture

The system consists of six logical components:

| Component | Port | Description |
|-----------|------|-------------|
| **Customer Database Service** | 9002 | Stores users, sessions, carts, purchase history, and seller feedback |
| **Product Database Service** | 9001 | Stores item metadata, prices, quantities, and feedback |
| **Seller Frontend Server** | 8001 | Stateless server handling seller APIs |
| **Buyer Frontend Server** | 8002 | Stateless server handling buyer APIs |
| **Seller CLI Client** | — | Command-line interface for sellers |
| **Buyer CLI Client** | — | Command-line interface for buyers |

All communication occurs strictly over TCP sockets.

---

## System Design Overview

- Frontend servers are stateless and do not store session or cart data  
- All persistent data resides in backend database services  
- Session IDs are issued at login and validated for every request  
- A background thread in the Customer Database enforces a 5-minute inactivity timeout
- Servers are multithreaded, supporting concurrent client connections  
- Communication uses a custom JSON protocol over TCP sockets  
- The architecture separates request handling (frontend) from state management (backend)

---

## Deployment Instructions

### Start All Services
```bash
./run_all.sh
```

### Stop All Services
```bash
./stop_all.sh
```

### Manual Startup (Alternative)
```bash
python3 product_db.py
python3 customer_db.py
python3 seller_server.py
python3 buyer_server.py
```

---

## Running Clients

```bash
python3 seller_client.py
python3 buyer_client.py
```

---

##  Running Performance Experiments

The benchmarking script simulates concurrent buyers and sellers.

```bash
python3 performance.py
```

### Scenarios Executed

| Scenario | Buyers | Sellers |
|----------|--------|---------|
| 1 | 1 | 1 |
| 2 | 10 | 10 |
| 3 | 100 | 100 |

Each client performs 1000 API operations per run, averaged across 10 runs.

---

##  Assumptions

- All data is stored in memory (no disk persistence)  
- TCP ensures reliable communication  
- Item search uses category matching and keyword overlap  
- Buyers and sellers may connect from multiple hosts simultaneously  
- Security features (encryption, hashing) are out of scope  
- The MakePurchase API is intentionally not implemented  

---

## Current System State

The system supports all required APIs except MakePurchase. Implemented functionality includes:

- Account creation and login  
- Session validation and timeout  
- Item registration and updates  
- Item search and retrieval  
- Shopping cart management  
- Seller feedback tracking  
- Purchase history tracking  
- Concurrent client handling  
- Performance benchmarking  



---

## 📁 Project Structure


```
PA1/
│
├── buyer_client.py
├── seller_client.py
├── buyer_server.py
├── seller_server.py
├── product_db.py
├── customer_db.py
├── protocol.py
├── performance.py
│
├── run_all.sh
├── stop_all.sh
├── README.md
└── DS_PA1_performance_report.pdf
```

---
