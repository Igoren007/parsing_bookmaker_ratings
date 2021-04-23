

def insert_document(collection, data):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    if len(data) > 1:
        return collection.insert_many(data)
    else:
        return collection.insert_one(data)

def find_document(collection, elements, multiple=False):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)