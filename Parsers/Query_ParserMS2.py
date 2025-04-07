import json
import psycopg2
import traceback

def cleanStr4SQL(s):
    return s.replace("'", "''").replace("\n", " ").replace("\r", " ") if isinstance(s, str) else str(s)

def getAttributes(attributes, parent=''):
    """Recursively extract all key-value pairs from nested attributes."""
    L = []
    for key, value in attributes.items():
        full_key = f"{parent}.{key}" if parent else key
        if isinstance(value, dict):
            L += getAttributes(value, full_key)
        elif isinstance(value, (bool, str, int, float)):
            L.append((full_key, value))
    return L

# PostgreSQL connection config
db_params = {
    'dbname': 'milestone1db',
    'user': 'postgres',
    'password': '0',  # <-- replace with your actual password
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

def parseBusinessData():
    print("Parsing businesses and inserting into DB...")
    with open('./yelp_business.JSON', 'r', encoding='utf-8') as f:
        count_line = 0
        for line in f:
            data = json.loads(line)
            try:
                business_id = cleanStr4SQL(data['business_id'])
                name = cleanStr4SQL(data['name'])
                address = cleanStr4SQL(data['address'])
                city = cleanStr4SQL(data['city'])
                state = cleanStr4SQL(data['state'])
                zipcode = cleanStr4SQL(data['postal_code'])
                stars = data['stars']
                review_count = data['review_count']
                is_open = data['is_open'] == 1

                cursor.execute("""
                    INSERT INTO business (
                        business_id, name, stars, address, city, state, zipcode,
                        numcheckins, is_open, reviewrating, reviewcount
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, 0, %s, 0.0, %s)
                """, (business_id, name, stars, address, city, state, zipcode, is_open, review_count))
                count_line += 1
                if count_line % 1000 == 0:
                    conn.commit()
            except Exception as e:
                print(f"Error inserting business {data.get('business_id')}: {e}")
                traceback.print_exc()
                conn.rollback()
    conn.commit()
    print(f"Inserted {count_line} businesses.")

def parseBusinessCategories():
    print("Parsing business categories and inserting into DB...")
    with open('./yelp_business.JSON', 'r', encoding='utf-8') as f:
        count_line = 0
        for line in f:
            data = json.loads(line)
            business_id = cleanStr4SQL(data['business_id'])
            categories_raw = data.get('categories', [])
            if categories_raw:
                if isinstance(categories_raw, list):
                    categories = categories_raw
                else:
                    categories = [c.strip() for c in categories_raw.split(',')]
                for category in categories:
                    try:
                        cname = cleanStr4SQL(category)
                        cursor.execute("""
                            INSERT INTO business_category (business_id, cname)
                            VALUES (%s, %s)
                        """, (business_id, cname))
                        count_line += 1
                    except Exception as e:
                        print(f"Error inserting category for {business_id}: {e}")
                        traceback.print_exc()
                        conn.rollback()
            if count_line % 1000 == 0:
                conn.commit()
    conn.commit()
    print(f"Inserted {count_line} business_category rows.")

def parseBusinessAttributes():
    print("Parsing business attributes and inserting into DB...")
    with open('./yelp_business.JSON', 'r', encoding='utf-8') as f:
        count_line = 0
        for line in f:
            data = json.loads(line)
            business_id = cleanStr4SQL(data['business_id'])
            attributes = getAttributes(data.get('attributes', {}))
            for (attr, value) in attributes:
                try:
                    attr = cleanStr4SQL(attr)
                    val_str = cleanStr4SQL(value)
                    cursor.execute("""
                        INSERT INTO business_attribute (business_id, aname, value)
                        VALUES (%s, %s, %s)
                    """, (business_id, attr, val_str))
                    count_line += 1
                except Exception as e:
                    print(f"Error inserting attribute for {business_id}: {e}")
                    traceback.print_exc()
                    conn.rollback()
            if count_line % 1000 == 0:
                conn.commit()
    conn.commit()
    print(f"Inserted {count_line} business_attribute rows.")

def parseBusinessCheckins():
    print("Parsing check-ins and inserting into DB...")
    with open('./yelp_checkin.JSON', 'r', encoding='utf-8') as f:
        count_line = 0
        for line in f:
            data = json.loads(line)
            business_id = cleanStr4SQL(data['business_id'])
            for day, times in data['time'].items():
                for hour, count in times.items():
                    try:
                        hour_formatted = f"{hour}:00" if ':' not in hour else hour
                        cursor.execute("""
                            INSERT INTO business_check_in (business_id, day, hour, count)
                            VALUES (%s, %s, %s, %s)
                        """, (business_id, day, hour_formatted, count))
                        count_line += 1
                        if count_line % 1000 == 0:
                            conn.commit()
                    except Exception as e:
                        print(f"Error parsing checkin for {business_id} on {day} at {hour}: {e}")
                        traceback.print_exc()
                        conn.rollback()
    conn.commit()
    print(f"Inserted {count_line} business_check_in rows.")

def parseReviewData():
    print("Parsing reviews and inserting into DB...")
    with open('./yelp_review.JSON', 'r', encoding='utf-8') as f:
        count_line = 0
        for line in f:
            data = json.loads(line)
            try:
                review_id = cleanStr4SQL(data['review_id'])
                business_id = cleanStr4SQL(data['business_id'])
                stars = int(data['stars'])
                date = cleanStr4SQL(data['date'])
                text = cleanStr4SQL(data['text'])

                cursor.execute("""
                    INSERT INTO review (
                        review_id, business_id, stars, date, text
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (review_id, business_id, stars, date, text))
                count_line += 1
                if count_line % 1000 == 0:
                    conn.commit()
            except Exception as e:
                print(f"Error inserting review {data.get('review_id')}: {e}")
                traceback.print_exc()
                conn.rollback()
    conn.commit()
    print(f"Inserted {count_line} reviews.")



# Run all parsers
parseBusinessData()
parseBusinessCategories()
parseBusinessAttributes()
parseBusinessCheckins()
parseReviewData()


# Clean up
cursor.close()
conn.close()
