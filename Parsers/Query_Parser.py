import json


def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ")

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute,value))
    return L

def parseBusinessData():
    print("Parsing businesses...")
    #read the JSON file
    with open('./yelp_business.JSON','r') as f:
        outfile =  open('./yelp_business.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id'] #business id
            business_str =  "'" + cleanStr4SQL(data['name']) + "'," + \
                            "'" + cleanStr4SQL(data['address']) + "'," + \
                            "'" + cleanStr4SQL(data['city']) + "'," +  \
                            "'" + data['state'] + "'," + \
                            "'" + data['postal_code'] + "'," +  \
                            str(data['latitude']) + "," +  \
                            str(data['longitude']) + "," + \
                            str(data['stars']) + "," + \
                            str(data['review_count']) + "," + \
                            str(data['is_open'])
            outfile.write(business_str + '\n')

            # process business categories
            for category in data['categories']:
                category_str = "'" + business + "','" + category + "'"
                outfile.write(category_str + '\n')

            # process business hours
            for (day,hours) in data['hours'].items():
                hours_str = "'" + business + "','" + str(day) + "','" + str(hours.split('-')[0]) + "','" + str(hours.split('-')[1]) + "'"
                outfile.write( hours_str +'\n')

            #process business attributes
            for (attr,value) in getAttributes(data['attributes']):
                attr_str = "'" + business + "','" + str(attr) + "','" + str(value)  + "'"
                outfile.write(attr_str +'\n')

            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()


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