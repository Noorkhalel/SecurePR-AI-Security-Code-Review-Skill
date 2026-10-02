# Application contract

MongoDB driver semantics apply. slug must be a literal public catalog identifier and the query must match only that identifier. JSON body accepts objects as well as strings. MongoDB operators supplied as the slug object alter this query. No schema check exists. Scope is catalog query manipulation, not account takeover.
