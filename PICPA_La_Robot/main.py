from datetime import datetime, timedelta

from praw import Reddit
from praw.models import Submission

from helper_outlook import OutlookInboxFolder
from helper_string import chain_replace

if __name__ == '__main__':
    PICPA = OutlookInboxFolder('PICPA')
    PICPA.show_body_links = False
    
    end_date = datetime.now().date()
    last_week = end_date - timedelta(days=7)

    current_mail_items = PICPA.folder_restrict(
        f"[ReceivedTime] >= '{last_week.strftime('%m/%d/%Y %H:%M %p')}'"
    )

    contents = []
    for items in current_mail_items:
        for subject, body in items.items():

            for_replacement = {
                "If you can't see this email click here.": '',
                '\t' : "&emsp;",
                '\r' : '',
                'Marvin' : 'Redditor',
                'Share this event' : '',
                'When' : '',
                '&emsp;\n' : '\n\n',
                '\n  \n' : '',
                '\n  &emsp;' : '\n\n',
                '\nSPEAKER' : ' | **SPEAKER**',
                'Speakers' : '## Speakers',
                '      I Will Attend     \n' : '' ,
                '\n      No     ' : '' ,
                'Register Now': '',
                'Register' : '',
            }

            body = chain_replace(body, replace=for_replacement)

            footer = body.find('Unsubscribe')
            body = body[0:footer]

            speakers = body.find('Speakers')
            body_speakers = body[speakers:]
            body = body[0:speakers]

            body_speakers = body_speakers.split('\n')
            body_speakers = '\n\n'.join(body_speakers)

            body = body + body_speakers

            decor = '¤' * min(48, len(subject)) + '\n'

            contents.append(
                f"{decor}\n## {subject}\n\n{decor}\n{body}"
            )

    # Reddit
    continue_to_post = input('Done getting data from Outlook. Should we continue?\n')

    if continue_to_post.lower() in ['y', 'yes']:
        POST_TITLE = f"This is PICPA for the week ending {end_date.strftime('%B %d, %Y')}"
        POST_BODY = '# PICPA WEEKLY \nThese are summary of new PICPA Events from ' \
            f"{last_week.strftime('%b %d')} to {end_date.strftime('%b %d')}.\n" \
            'You can register for these events at the ' \
            '[PICPA GlueUp website](https://picpa.glueup.com/).\n\n'

        POST_BODY = POST_BODY + '\n---\n'.join(contents)

        POST_BODY = POST_BODY \
            + '\n---\n^(I am a bot in alpha. For concerns, contact ' \
            + '[tagapagtuos](https://www.reddit.com/user/tagapagtuos).)'
        
        try:
            reddit = Reddit('PICPA_La_Robot', user_agent='script/PICPA_La_Robot')
            submit_body = reddit.subreddit('AccountingPH').submit(POST_TITLE, POST_BODY)
        except Exception as e:
            print(e)
    else:
        print('I will take that as a NO.')
