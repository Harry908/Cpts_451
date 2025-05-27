# CPTS_451 Business Browser

## 📌 Overview

**CPTS_451 Business Browser** is a standalone Python-based desktop application developed as part of the CptS 451: Introduction to Database Systems course. The application allows users to search and analyze local business data extracted from a simplified **Yelp dataset** and enriched with **U.S. Census ZIP code** data. Its primary focus is on effective **database design, optimization, and query performance**.

---

## 🎯 Features

- 🔍 **Search Businesses** by state, city, ZIP code, and/or category
- 📊 **Analyze Business Metrics**
  - View number of reviews, average review ratings, and check-ins
  - Identify **popular** and **successful** businesses using custom SQL-based metrics
- 🗃️ **Integrated ZIP Code Data**
  - Population and average income data per ZIP code
- 💡 **Top Business Categories**
  - Discover the most frequent categories in a region
- ✅ **Fully Database-Driven**
  - All data retrieval is performed using SQL queries via PostgreSQL
  - No in-memory storage allowed — all logic flows through the DB layer

---

## 🗂️ Datasets Used

- **Yelp Academic Dataset (Simplified)**
- **U.S. Census ZIP Code Data (Simplified)**

---

## 🧱 Tech Stack

- **Python 3.11.9**
- **PyQt5**
- **PostgreSQL**
- **psycopg2** (Python PostgreSQL adapter)
- **SQL (DDL, DML)**

---

## 📌 Key Functionalities

### 1. Business Search
- Filter businesses by **state, city, ZIP code**, and **category**
- Display key info:
  - Business name
  - Address
  - Rating and review stats
  - Check-in count

### 2. ZIP Code Analysis
- Total businesses
- Population
- Average income

### 3. Business Classification
- Businesses are classified into:
  - **Popular**: High customer engagement
  - **Successful**: Longevity and customer loyalty
- Metrics are defined and implemented by the team using SQL logic

---

## 📁 Milestones

### ✅ Milestone 1
- JSON Parsing (business, user, review, check-in)
- ER Diagram v1 and DDL Statements
- Basic DB Application with CSV import

### ✅ Milestone 2
- Revised ER Diagram and SQL Schema
- Full Data Insertion & Integrity Constraints
- Popularity & Success Metrics Paper
- Alpha Application Prototype

### 🔜 Milestone 3
- Final Application
- Advanced Queries & GUI Polish

---

## 📚 References

- [Yelp Dataset Challenge](https://www.yelp.com/dataset)
- [Yelp Dataset Documentation](https://www.yelp.com/dataset/documentation/json)
- Sample parser and dataset provided by course instructors

---

## 👥 Authors

- Huy (Harry) Ky: [GitHub: Harry908](https://github.com/Harry908)
- Nhan Nguyen: [GitHub: nhannguyen111](https://github.com/nhannguyen111)

