def is_job_search(query):

    query = query.lower().strip()

    # ------------------ Actual Job Search Words ------------------

    search_words = [
        "find jobs",
        "find job",
        "search jobs",
        "search job",
        "show jobs",
        "show job",
        "job openings",
        "job opening",
        "job vacancies",
        "job vacancy",
        "vacancies",
        "vacancy",
        "hiring",
        "job listings",
        "job listing",
        "apply for jobs",
        "apply for job",
        "jobs near me",
        "jobs in",
        "job in",
        "openings in",
        "opening in"
    ]

    # ------------------ Job Search Intent ------------------

    for word in search_words:

        if word in query:
            return True

    # ------------------ Explicit Job + Action ------------------

    action_words = [
        "find",
        "search",
        "show",
        "list",
        "look for",
        "get me"
    ]

    job_words = [
        "jobs",
        "job",
        "vacancy",
        "vacancies",
        "opening",
        "openings"
    ]

    has_action = any(
        word in query
        for word in action_words
    )

    has_job_word = any(
        word in query
        for word in job_words
    )

    if has_action and has_job_word:
        return True

    # ------------------ Otherwise AI Chat ------------------

    return False