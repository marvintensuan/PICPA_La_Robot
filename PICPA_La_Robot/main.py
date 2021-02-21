from datetime import datetime, timedelta

from praw import Reddit
from praw.models import Submission

from helper_outlook import OutlookInboxFolder

if __name__ == '__main__':
    PICPA = OutlookInboxFolder('PICPA')
    PICPA.show_body_links = False

    
    end_date = datetime.now().date()
    last_week = end_date - timedelta(days=7)

    current_mail_items = PICPA.folder_restrict(
        f"[ReceivedTime] >= '{last_week.strftime('%m/%d/%Y %H:%M %p')}'"
    )

    for items in current_mail_items:
        for subject, body in items.items():
            body = body.replace("If you can't see this email click here.", '')
            body = body.replace('\t', "&#9;")
            body = body.replace('\r', '')
        break

    # Reddit

    continue_to_post = input('Done getting data from Outlook. Should we continue?\n')

    if continue_to_post.lower() in ['y', 'yes']:
        POST_TITLE = f'This is PICPA for the week ending {end_date.strftime()}'
        POST_BODY = '# PICPA WEEKLY \nThese are summary of new PICPA Events from' \
            f"{last_week.strftime('%b %d')} to {end_date.strftime('%b %d')}.\n" \
            'You can register in these events at the' \
            '[PICPA GlueUp page](https://picpa.glueup.com/my/home/)'

        reddit = Reddit('PICPA_La_Robot', user_agent='script/PICPA_La_Robot')
        submit_body = reddit.subreddit('testingground4bots').submit(POST_TITLE, POST_BODY)
    else:
        print('I will take that as a NO.')
