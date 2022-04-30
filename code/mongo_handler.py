import pymongo
import pandas as pd


class mongoob:

    def __init__(self, host = '127.0.0.1',port= 27017):
        self.client = pymongo.MongoClient('127.0.0.1', 27017)
        self.db = self.client.academicworld
        
        self.profs = pd.DataFrame(self.db.faculty.aggregate([{"$project":{"name":"$name"}}]))
        self.profs = list(self.profs.iloc[:,1])


def get_prof_info(db,nm):
    query = [{"$match":{"name":nm}},
             {"$lookup":{"from":"publications","localField":"publications","foreignField":"id","as":"pub"}},
             {"$unwind":"$pub"},{"$sort":{"pub.numCitations":-1}},{"$limit":3},
             {"$project":{"name":"$name","email":"$email","phone":"$phone","citations":"$pub.numCitations",
                          "Unv":"$affiliation.name","photo_url":"$photoUrl","position":"$position","title":"$pub.title",
                          "year":"$pub.year"}}]
    
    
    res = db.faculty.aggregate(query)
    res = pd.DataFrame(res)
    return(res)