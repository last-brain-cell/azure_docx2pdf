"""
workflow 1 - using only a Temporary .
1. Download a docx file from a blob storage container
2. Upload it Temporary OneDrive/Sharepoint Folder.
3. Download it again in pdf format.
4. Delete it from the Temporary OneDrive/Sharepoint Folder.
"""

"""
workflow 1 - without using Microsoft AZCopy.
1. Download a docx file from a blob storage container
2. Upload it Temporary OneDrive/Sharepoint Folder.
3. Download it again in pdf format.
4. Delete it from the Temporary OneDrive/Sharepoint Folder.
"""

"""
workflow 2 - using Microsoft AZCopy.
1. Use MS AZCopy API to copy a docx file from an Azure Blob Container to a Temporary OneDrive/Sharepoint Folder.
2. Download it in pdf format.
3. Delete it from the Temporary OneDrive/Sharepoint Folder.
"""

import os
import requests

SCOPES = ['Files.Read']
save_location = os.getcwd()

file_ids = ['D4F4CD875F73E298!1428'] # need to get this from api call

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'
access_token = "EwB4A8l6BAAUbDba3x2OMJElkF7gJ4z/VbCPEz0AAVvYUGAtVl6mRt2gOdWJfLws2h529NYi8CbfWXR8SWVZbA9b3Nyh2nBvnVCK0BJ2I60CO3UqPRdIv0kHIsEgCTDN8ATfMNXRF+1Vv5iJTM62SKPizK9FWLPuXY8sej3M9q5K0YUaW7VZQa1XjFDoTEn255PfUHF1tr4rqJn64UI4dn8sB1wOlXqfpGt2HxQbHNFstXzO2q8rzxw4mzyV17ShZDPYSzL43Lp0plDhcNX8yJRKObuyh7fLr/XfzcOV9n/zMugyD6L6xhtbXk+6kErMoC+puOFxKMHy3QRnypcEo0SAz4xM8X1wBE2XfsOf0R5KXd3v/QjaVW7FXUjYjhMQZgAAENc1lcndlEhpQwOXHIG19P9AAtaOdzgg54oJnLBa6a8ZKTjFyWKe/cXQLCGbA5b5J687vZ5TwuUCeATtyavGNFPHw9dgRVrZD+N6wmyd/9mFajxvM7ii/YVd/wDwAaHfqMjVc6Zacnx3HojjUCmHC72lUDbxswyVk1O1HA7vFYMsihG4b5Z3a+l13k/yw0ZmX5aTXL6DiFGqVibYEsG11Nmwp/lpyJ+iyGwa3rpqc0F0q1eQPtCwyepJ94i9dRdLoWLo6nOX/KFpcYtwCUeJDR9Cdl6SUS0HRPwmSDxgK0PzAh9zBzikuifojDKI8+j7uk3wdAH7ZJYHz0OeI589dPL73EzkWso1pDwwVwTape1fgzusbsTapTCGE765Vm4BihHusbmMKou763K75Zn6RIiPEzqbnasju2bmj90OgURbY2eLVExesSXRPfgxW+DZMem5UqVp8ToZx3BF4shfoxM84sWqatBxDOpyH6eo6rzUi39nUARXuQZcR9T36QT0vluX/Sg/88FL2aDlzcrYrAEu5NlOeshRs1bJT9Dlj6I2y+hoMb8XqzMmOhThuGDpqnins8nvdjbJsHHflO1txj/JwiZgcemt4kayBY67ykZK45ZNWHvHEmvEB/XUdTLLnuMkhcK2gIpRyi4zuC9Zfa9L8npnYyH+cLIwneJIe1LX9NiIRQxh3281nHqSgxCZAgK3H6bzSNCdShHt6ep+ce2S5XeuNTX8u9xIb33ftQ0OnEV47GNhGPt2UZnVhvA1pHyNuM6NkyQmmm/LjKxC6EQ9zXcC"
headers = {
    'Authorization': 'Bearer ' + access_token
}


for file_id in file_ids:
    response_file_content = requests.get(GRAPH_API_ENDPOINT + f'/me/drive/items/{file_id}/content?format=pdf', headers=headers)
    with open(os.path.join(save_location, f"temp.pdf"), 'wb') as _f:
        _f.write(response_file_content.content)
