import re
import win32com.client

class OutlookInboxFolder:
    def __init__(self, folder):
        self.mapi = win32com.client.Dispatch('outlook.application').GetNamespace('MAPI')
        self.folder = self.mapi.GetDefaultFolder(6).Folders[folder]
        self.show_body_links = True

    def folder_restrict(self, str_filter, link_replacement=''):
        folder_items = []
        try:
            if isinstance(str_filter, str):
                for item in self.folder.Items.Restrict(str_filter):
                    msg = dict.fromkeys([item.Subject])
                    body = item.body
                    if not self.show_body_links:
                        body = self.hide_links(body, replacement=link_replacement)
                    msg[item.Subject] = body
                    folder_items.append(msg)
        except Exception as e:
            print(f'Error occured: {e}')
        finally:
            return folder_items

    @staticmethod
    def hide_links(text, replacement = '', pattern = '(<.*?>)'):
        regex = re.findall(pattern, text)
        for match in regex:
            text = text.replace(match, replacement)
        return text
