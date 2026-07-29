def normalize_search_query(query_param):

    search_query = query_param.strip() if query_param else ''
    return ' '.join(search_query.split())

