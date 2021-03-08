from datetime import datetime, timedelta

import PICPA_La_Robot as Bot

if __name__ == '__main__':
    inbox = Bot.OutlookInboxFolder('PICPA')
    inbox.show_body_links = False

    end_date = datetime.now().date()
    last_week = end_date - timedelta(days=7)

    current_mail_items = inbox.folder_restrict(
        f"[ReceivedTime] >= '{last_week.strftime('%m/%b/%Y %H:%M %p')}'"
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
                '    Learn more' : ''
            }

            body = Bot.chain_replace(body, replace=for_replacement)
            body = body.strip()

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

    contents = [cont + '\n---\n' for cont in contents]

    CHAR_LIMIT = 30000
    char_len_count = 0
    comments = []

    for n, item in enumerate(contents):
        char_len_count += len(item)
        if char_len_count >= CHAR_LIMIT:
            slicer = n
            comments = contents[slicer:]
            contents = contents[0:slicer]
            break

    continue_to_post = input('Done getting data from Outlook. Should we continue?\n')

    if continue_to_post.lower() in ['y', 'yes']:
        try:
            reddit = Bot.RedditInstance('PICPA_La_Robot', user_agent='script/PICPA_La_Robot')

            reddit.post_title = (f"This is PICPA for the week ending {end_date.strftime('%B %d, %Y')}")
            reddit.append_body('# PICPA WEEKLY')
            reddit.append_body('These are summary of new PICPA Events from', end=' ')
            reddit.extend_body_last(f"{last_week.strftime('%b %d')} to {end_date.strftime('%b %d')}.")
            reddit.append_body('You can register for these events at the', end=' ')
            reddit.extend_body_last('[PICPA GlueUp website](https://picpa.glueup.com/).', end='\n\n')

            reddit.append_body(contents)
            
            reddit.append_body('^(I am a bot in alpha. For concerns, contact', end=' ')
            reddit.extend_body_last('[tagapagtuos](https://www.reddit.com/user/tagapagtuos).)')

            reddit.post('AccountingPH')

            for item in comments:
                reddit.comment_on_post(item)
        except Exception as e:
            print(e)
    else:
        print('I will take that as a NO.')