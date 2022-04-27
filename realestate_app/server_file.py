# NOT Currently Using

import pysftp as sftp
import os

from realestate_bot.settings import FTP_HOST, FTP_PASS, FTP_USER


def sftpExamp():

    print("++++++++++", FTP_HOST, FTP_PASS, FTP_USER)

    try:
        srv = sftp.Connection(
            host=FTP_HOST, username=FTP_USER, password=FTP_PASS)

        remote_path = "test/racestatedata01.json"
        filename = f"{os.getcwd()}/realestate_app/racedata.json"

        # with srv.cd('public/'): #chdir to public
        srv.put(filename, remote_path)

        # Closes the connection
        srv.close()

    except Exception as e:
        print("Error in sftp: ", e)
