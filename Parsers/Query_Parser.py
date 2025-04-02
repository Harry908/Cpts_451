import json

def cleanStr4SQL(s):
    return s.replace("'", "''").replace("\n", " ").replace("\r", " ")

def getAttributes(attributes):
    L = []
    for (attribute, value) in attributes.items():
        if isinstance(value, dict):
            L += getAttributes(value)
        elif isinstance(value, bool):
            L.append((attribute, value))
    return L

def parseBusinessData():
    print("Parsing businesses...")

    with open('./yelp_business.JSON', 'r') as f, \
         open('yelp_business.txt', 'w') as business_out, \
         open('business_category.txt', 'w') as category_out, \
         open('business_attribute.txt', 'w') as attr_out, \
         open('business_check_in.txt', 'w') as checkin_out:

        count_line = 0
        line = f.readline()

        while line:
            data = json.loads(line)
            business = data['business_id']

            # Write to business.txt
            business_str = (
                "'" + business + "'," +
                "'" + cleanStr4SQL(data['name']) + "'," +
                str(data['stars']) + "," +
                "'" + cleanStr4SQL(data['address']) + "'," +
                "'" + cleanStr4SQL(data['city']) + "'," +
                "'" + data['state'] + "'," +
                "'" + data['postal_code'] + "'," +
                "0," +  # numCheckins
                str(data['is_open']) + "," +
                str(data['stars']) + "," +  # reviewrating
                str(data['review_count'])   # reviewcount
            )
            business_out.write(business_str + '\n')

            # Write to business_category.txt
            if data.get('categories'):
                for category in set([c.strip() for c in data['categories']]):
                    category_str = "'" + business + "','" + cleanStr4SQL(category) + "'"
                    category_out.write(category_str + '\n')

            # Write to business_check_in.txt (from business hours)
            if data.get('hours'):
                for (day, hours) in data['hours'].items():
                    if hours:
                        open_time, _ = hours.split('-')  # only write start time
                        # Force open_time into HH:MM:SS format
                        time_str = open_time.strip()
                        if len(time_str) == 5:
                            time_str += ":00"
                        checkin_str = "'" + business + "','" + day + "','" + time_str + "',1"
                        checkin_out.write(checkin_str + '\n')

            # Write to business_attribute.txt
            if data.get('attributes'):
                for (attr, value) in getAttributes(data['attributes']):
                    attr_str = "'" + business + "','" + str(attr) + "','" + str(value) + "'"
                    attr_out.write(attr_str + '\n')

            line = f.readline()
            count_line += 1

        print(count_line)


def parseCheckinData():
    print("Parsing checkins...")
    #read the JSON file
    with open('./yelp_checkin.JSON','r') as f:
        outfile =  open('./yelp_checkin.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id'] #business id
            for (date, time) in data['time'].items():
                for (hour, count) in time.items():
                    time_str = "'" + business + "','" + \
                                    date + "','" + \
                                    hour + "'," + \
                                    str(count)
                    outfile.write(time_str + '\n')
            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()

def parseReviewData():
    print("Parsing reviews...")
    #reading the JSON file
    with open('./yelp_review.JSON','r') as f:
        outfile =  open('./yelp_review.txt', 'w')
        line = f.readline()
        count_line = 0
        while line:
            data = json.loads(line)
            review_str = "'" + data['review_id'] + "','" +  \
                            data['user_id'] + "','" + \
                            data['business_id'] + "'," + \
                            str(data['stars']) + ",'" + \
                            data['date'] + "','" + \
                            cleanStr4SQL(data['text']) + "'"
            outfile.write(review_str + '\n')
            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()

def parseUserData():
    print("Parsing users...")
    #reading the JSON file
    with open('./yelp_user.JSON','r') as f:
        outfile =  open('./yelp_user.txt', 'w')
        line = f.readline()
        count_line = 0
        while line:
            data = json.loads(line)
            user_str = "'" + data['user_id'] + "','" +  \
                        cleanStr4SQL(data['name']) + "','" + \
                        cleanStr4SQL(data['yelping_since']) + "'," + \
                        str(data['fans']) + "," + \
                        str(data['review_count']) + "," + \
                        str(data['average_stars']) + "," + \
                        str(data['useful']) + "," + \
                        str(data['funny']) + "," + \
                        str(data['cool'])
            outfile.write(user_str + '\n')

            for friend in data['friends']:
                friend_str = "'" + data['user_id'] + "','" + friend + "'"
                outfile.write(friend_str + '\n')
            
            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()


parseBusinessData()
parseCheckinData()
parseReviewData()
parseUserData()

