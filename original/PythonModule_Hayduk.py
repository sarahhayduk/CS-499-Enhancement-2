# Edited by: Sarah Hayduk
from pymongo import MongoClient
from bson.objectid import ObjectId

# CRUD class that, when instantiated, provides Create, Read, Update, & Delete functionality.
class CRUD:
    """ CRUD operations for Animal collection in MongoDB """
    
    
    def __init__(self):
        # Initializing the MongoClient. The helps to
        # access the MongoDB databases and collections.
        # This is hard-wired to use the AAC database, the 
        # animals collection, and the aac user.
        #
        # Connection variables (based off my Module Three Milestone)
        #
        USER = 'aacuser'
        PASS = 'Hayduk'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 30432 # my port
        DB = 'AAC' # my DB uses capital letters
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]
        
        
    # Method to implement the C in CRUD.
    def create(self, data):
        """ Inserts a document into the specified Mongo DB database & collection. """
        
        if isinstance(data, dict) and data: # validate input is non-empty dictionary
            try:
                self.collection.insert_one(data) # use self.collection, not hard coded animals
                return True
            except Exception as e:
                print("Insertion error: ", e) # print feedback on false (ex. duplicate insert)
                return False
        else:
            raise ValueError("Input must be a set of key/value pairs.") # raise error for bad input
             
                
    # Method to implement the R in CRUD.
    def read(self, data):
        """ Queries for documents from a specified MongoDB database and collection. """
        
        if isinstance(data, dict): # validate the query is dictionary
            try:
                result = list(self.collection.find(data)) # convert cursor to list using find() method
                return result
            except Exception: 
                return []
        else:
            raise ValueError("Query must be a key/value lookup pair.") # raise error for bad input
            
            
    # Method in implement the U in CRUD.
    def update(self, data, update_data, multiple=False):
        """ Queries for & changes document(s) from a specified MongoDB database & collection. """
        
        if isinstance(data, dict) and isinstance(update_data, dict): # validate both arguemnts are dictionaries
            try:
                if multiple:
                    result = self.collection.update_many(data, {'$set': update_data}) # multiple=True, update many
                    return result.modified_count
                else:
                    result = self.collection.update_one(data, {'$set': update_data}) # multiple=False, update one
                    return result.modified_count
            except Exception as e:
                print("Update error: ", e) # print feedback on fail (ex: update duplicates existing unique Id)
                return 0
        else:
            raise ValueError("Both arguments must be key/value pairs.") # raise error for bad input
            
    
    # Method to implement the D in CRUD.
    def delete(self, data, multiple=False):
        """ Queries for & removes document(s) from specified MongoDB database & collection. """
        
        if isinstance(data, dict): # validate the query is dictionary
            try:
                if multiple:
                    result = self.collection.delete_many(data) # multiple=True, delete many
                    return result.deleted_count
                else:
                    result = self.collection.delete_one(data) #multiple=False, delete one
                    return result.deleted_count
            except Exception as e:
                print("Deletion error: ", e) # print feedback (ex: delete using string instead of ObjectId for _id)
                return 0
        else:
            raise ValueError("Query must be a key/value lookup pair.") # raise error for bad input