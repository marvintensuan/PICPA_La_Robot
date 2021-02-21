from helper_outlook import OutlookInboxFolder

if __name__ == '__main__':
    PICPA = OutlookInboxFolder('PICPA')
    PICPA.show_body_links = False

    # start_date = str(input('Enter start date. Format: MM/DD/YYYY.\n'))
    # start_date = start_date + ' 12:00 AM'
    start_date = '02/17/2021 12:00 AM'

    current_mail_items = PICPA.folder_restrict(f"[ReceivedTime] >= '{start_date}'")

    for items in current_mail_items:
        for subject, body in items.items():
            body = body.replace("If you can't see this email click here.", '')
            body = body.replace('\t', "&#9;")
            body = body.replace('\r', '')
            body = body.replace('\n', '#')
            print([body])
            #print('----' * 100)
        break
