# PICPA La Robot

This is a Reddit script bot which searches for my Outlook inbox folder for events sent to me by the Philippine Institute of Certified Public Accountants (PICPA). It will then collate the messages and post it on /r/AccountingPH.

The name came from the PICPA Sports Event, PICPALaro.

# Implementation Details

To use the script, run the following command in your command line:

    $ python main.py

The whole script is in the `main.py` file. Details for the bot is abstracted by the `PICPA_La_Robot` module.

```python
    import PICPA_La_Robot as Bot
```