import sqlite3
from pathlib import Path

db_path = Path(__file__).with_name("sql_assessment.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

print("Creating tables and inserting sample data...")
cursor.executescript("""
DROP TABLE IF EXISTS Deliveries;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Restaurants;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    UserName VARCHAR(50),
    City VARCHAR(50),
    AccountType VARCHAR(20)
);

CREATE TABLE Restaurants (
    RestaurantID INT PRIMARY KEY,
    RestaurantName VARCHAR(100),
    Cuisine VARCHAR(50),
    Rating DECIMAL(2,1)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    UserID INT,
    RestaurantID INT,
    BillAmount DECIMAL(10,2),
    OrderDate DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID)
);

CREATE TABLE Deliveries (
    DeliveryID INT PRIMARY KEY,
    OrderID INT,
    DeliveryStatus VARCHAR(20),
    DeliveryTimeMinutes INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);
""")

cursor.executescript("""
INSERT INTO Users VALUES (1, 'Aman Verma', 'Delhi', 'Premium');
INSERT INTO Users VALUES (2, 'Riya Sen', 'Mumbai', 'Regular');
INSERT INTO Users VALUES (3, 'Karan Patel', 'Delhi', 'Regular');

INSERT INTO Restaurants VALUES (101, 'Spice Symphony', 'North Indian', 4.5);
INSERT INTO Restaurants VALUES (102, 'Pizza Express', 'Italian', 3.9);
INSERT INTO Restaurants VALUES (103, 'Tandoori Nights', 'North Indian', 4.2);

INSERT INTO Orders VALUES (501, 1, 101, 1200.00, '2026-07-15');
INSERT INTO Orders VALUES (502, 2, 102, 450.00, '2026-07-16');
INSERT INTO Orders VALUES (503, 1, 101, 5500.00, '2026-07-17');

INSERT INTO Deliveries VALUES (901, 501, 'Delivered', 25);
INSERT INTO Deliveries VALUES (902, 502, 'Delivered', 42);
INSERT INTO Deliveries VALUES (903, 503, 'Cancelled', 15);
""")

queries = {
    "Q1": """
SELECT
    u.UserName,
    r.RestaurantName,
    o.BillAmount
FROM Orders o
JOIN Users u ON o.UserID = u.UserID
JOIN Restaurants r ON o.RestaurantID = r.RestaurantID;
""",
    "Q2": """
SELECT DISTINCT
    r.RestaurantName
FROM Restaurants r
JOIN Orders o ON r.RestaurantID = o.RestaurantID
JOIN Deliveries d ON o.OrderID = d.OrderID;
""",
    "Q3": """
SELECT
    o.OrderID,
    u.UserName
FROM Orders o
JOIN Users u ON o.UserID = u.UserID
JOIN Deliveries d ON o.OrderID = d.OrderID
WHERE d.DeliveryTimeMinutes > 35;
""",
    "Q4": """
SELECT
    u.UserID,
    u.UserName,
    COALESCE(SUM(o.BillAmount), 0) AS TotalSpend
FROM Users u
LEFT JOIN Orders o ON u.UserID = o.UserID
GROUP BY u.UserID, u.UserName
ORDER BY u.UserID;
""",
    "Q5": """
SELECT
    u.UserID,
    u.UserName,
    COUNT(o.OrderID) AS TotalOrders
FROM Users u
LEFT JOIN Orders o ON u.UserID = o.UserID
GROUP BY u.UserID, u.UserName
ORDER BY u.UserID;
""",
    "Q6": """
SELECT
    r.RestaurantName
FROM Restaurants r
JOIN Orders o ON r.RestaurantID = o.RestaurantID
JOIN Users u ON o.UserID = u.UserID
WHERE u.City = 'Delhi'
GROUP BY r.RestaurantID, r.RestaurantName
HAVING SUM(o.BillAmount) > 5000;
""",
    "Q7": """
SELECT
    r.RestaurantName,
    COUNT(d.DeliveryID) AS CancelledOrderCount
FROM Restaurants r
JOIN Orders o ON r.RestaurantID = o.RestaurantID
JOIN Deliveries d ON o.OrderID = d.OrderID
WHERE d.DeliveryStatus = 'Cancelled'
GROUP BY r.RestaurantID, r.RestaurantName;
""",
    "Q8": """
SELECT DISTINCT
    u.UserName,
    u.City
FROM Users u
JOIN Orders o ON u.UserID = o.UserID
WHERE o.BillAmount > (
    SELECT AVG(BillAmount)
    FROM Orders
);
""",
    "Q9": """
SELECT
    r.Cuisine,
    AVG(d.DeliveryTimeMinutes) AS AvgDeliveryTime
FROM Restaurants r
JOIN Orders o ON r.RestaurantID = o.RestaurantID
JOIN Deliveries d ON o.OrderID = d.OrderID
GROUP BY r.Cuisine
HAVING AVG(r.Rating) > 4.0;
""",
}

print("Running SQL queries...\n")

for title, query in queries.items():
    print(f"=== {title} ===")
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    print("Columns:", columns)
    if rows:
        for row in rows:
            print(row)
    else:
        print("(No rows)")
    print()

# Q10 is handled separately because SQLite may or may not support window functions
print("=== Q10 ===")
q10_sql = """
SELECT
    r.Cuisine,
    r.RestaurantName,
    COUNT(o.OrderID) AS OrderCount
FROM Restaurants r
LEFT JOIN Orders o ON r.RestaurantID = o.RestaurantID
GROUP BY r.Cuisine, r.RestaurantID, r.RestaurantName
ORDER BY r.Cuisine, OrderCount DESC, r.RestaurantName;
"""
cursor.execute(q10_sql)
rows = cursor.fetchall()

if sqlite3.sqlite_version >= "3.25.0":
    # Try window function version if supported
    q10_window = """
    SELECT
        Cuisine,
        RestaurantName,
        OrderCount,
        DENSE_RANK() OVER (
            PARTITION BY Cuisine
            ORDER BY OrderCount DESC
        ) AS RestaurantRank
    FROM (
        SELECT
            r.Cuisine AS Cuisine,
            r.RestaurantName AS RestaurantName,
            COUNT(o.OrderID) AS OrderCount
        FROM Restaurants r
        LEFT JOIN Orders o ON r.RestaurantID = o.RestaurantID
        GROUP BY r.Cuisine, r.RestaurantID, r.RestaurantName
    ) AS t
    ORDER BY Cuisine, RestaurantRank, RestaurantName;
    """
    cursor.execute(q10_window)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    print("Columns:", columns)
    for row in rows:
        print(row)
else:
    # Fallback ranking in Python
    columns = ["Cuisine", "RestaurantName", "OrderCount", "RestaurantRank"]
    print("Columns:", columns)
    grouped = {}
    for cuisine, restaurant_name, order_count in rows:
        grouped.setdefault(cuisine, []).append((restaurant_name, order_count))

    for cuisine, items in grouped.items():
        items.sort(key=lambda x: (-x[1], x[0]))
        for rank, (restaurant_name, order_count) in enumerate(items, start=1):
            print((cuisine, restaurant_name, order_count, rank))

conn.commit()
conn.close()

print(f"\nDatabase file created at: {db_path}")