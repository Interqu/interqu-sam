import json

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=3))

    posts = {
        "1": {"id": "1", "title": "First book", "author": "Author1", "url": "https://amazon.com/", "content": "SAMPLE TEXT AUTHOR 1 SAMPLE TEXT AUTHOR 1 SAMPLE TEXT AUTHOR 1 SAMPLE TEXT AUTHOR 1 SAMPLE TEXT AUTHOR 1 SAMPLE TEXT AUTHOR 1", "ups": "100", "downs": "10"},
        "2": {"id": "2", "title": "Second book", "author": "Author2", "url": "https://amazon.com", "content": "SAMPLE TEXT AUTHOR 2 SAMPLE TEXT AUTHOR 2 SAMPLE TEXT", "ups": "100", "downs": "10"},
        "3": {"id": "3", "title": "Third book", "author": "Author3", "url": None, "content": None, "ups": None, "downs": None },
        "4": {"id": "4", "title": "Fourth book", "author": "Author4", "url": "https://www.amazon.com/", "content": "SAMPLE TEXT AUTHOR 4 SAMPLE TEXT AUTHOR 4 SAMPLE TEXT AUTHOR 4 SAMPLE TEXT AUTHOR 4 SAMPLE TEXT AUTHOR 4 SAMPLE TEXT AUTHOR 4 SAMPLE TEXT AUTHOR 4 SAMPLE TEXT AUTHOR 4", "ups": "1000", "downs": "0"},
        "5": {"id": "5", "title": "Fifth book", "author": "Author5", "url": "https://www.amazon.com/", "content": "SAMPLE TEXT AUTHOR 5 SAMPLE TEXT AUTHOR 5 SAMPLE TEXT AUTHOR 5 SAMPLE TEXT AUTHOR 5 SAMPLE TEXT", "ups": "50", "downs": "0"}
    }

    relatedPosts = {
        "1": [posts['4']],
        "2": [posts['3'], posts['5']],
        "3": [posts['2'], posts['1']],
        "4": [posts['2'], posts['1']],
        "5": []
    }

    print("Got an Invoke Request.")

    field = event['field']
    arguments = event.get('arguments', {})

    if field == "getPost":
        post_id = arguments.get('id')
        return posts.get(post_id)
    elif field == "allPosts":
        return list(posts.values())
    elif field == "addPost":
        # Return the arguments back
        return arguments
    elif field == "addPostErrorWithData":
        post_id = arguments.get('id')
        result = posts.get(post_id, {})
        # Attach additional error information to the post
        result['errorMessage'] = 'Error with the mutation, data has changed'
        result['errorType'] = 'MUTATION_ERROR'
        return result
    elif field == "relatedPosts":
        source_id = event.get('source', {}).get('id')
        return relatedPosts.get(source_id)
    else:
        return "Unknown field, unable to resolve" + field