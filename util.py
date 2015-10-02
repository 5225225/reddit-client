def humanify_td(z):
    if z.days > 365:
        years = z.days // 365
        if years == 1:
            return "1 year"
        else:
            return "{} years".format(years)

    elif z.days > 30:
        months = z.days // 30
        if months == 1:
            return "1 month"
        else:
            return "{} months".format(months)

    elif z.days > 7:
        weeks = z.days // 7
        if weeks == 1:
            return "1 week"
        else:
            return "{} weeks".format(weeks)

    elif z.days >= 1:
        days = z.days
        if days == 1:
            return "1 day"
        else:
            return "{} days".format(days)

    elif z.seconds > 3600:
        hours = z.seconds // 3600
        if hours == 1:
            return "1 hour"
        else:
            return "{} hours".format(hours)

    elif z.seconds > 60:
        minutes = z.seconds // 60
        if minutes == 1:
            return "1 minute"
        else:
            return "{} minutes".format(minutes)

    elif z.seconds > 5:
        seconds = z.seconds
        return "{} seconds".format(seconds)

    return "just now"

def refresh_subreddit(subreddit, sort, filter_time):
    posts = []

    if sort == "hot":
        posts = list(subreddit.get_hot())
    elif sort == "new":
        posts = list(subreddit.get_new())
    elif sort == "rising":
        posts = list(subreddit.get_rising())
    elif sort == "controversial":
        if filter_time == "hour":
            posts = list(subreddit.get_controversial_from_hour())
        elif filter_time == "day":
            posts = list(subreddit.get_controversial_from_day())
        elif filter_time == "week":
            posts = list(subreddit.get_controversial_from_week())
        elif filter_time == "month":
            posts = list(subreddit.get_controversial_from_month())
        elif filter_time == "year":
            posts = list(subreddit.get_controversial_from_year())
        elif filter_time == "all":
            posts = list(subreddit.get_controversial_from_all())
    elif sort == "top":
        if filter_time == "hour":
            posts = list(subreddit.get_top_from_hour())
        elif filter_time == "day":
            posts = list(subreddit.get_top_from_day())
        elif filter_time == "week":
            posts = list(subreddit.get_top_from_week())
        elif filter_time == "month":
            posts = list(subreddit.get_top_from_month())
        elif filter_time == "year":
            posts = list(subreddit.get_top_from_year())
        elif filter_time == "all":
            posts = list(subreddit.get_top_from_all())

    return posts
