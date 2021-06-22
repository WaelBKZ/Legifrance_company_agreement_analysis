# Project Summary

Gather and exploit company agreements from **Legifrance** on the effect of the pandemic on telecommuting and on the effect of a French reform on the professional inequalities between women and men.


# Scrapping

Here are all the steps you need to follow in order to scrap the agreements from **Legifrance** using this repository. To begin with, you will need a token to be authorized to access the API. We describe the process on how to get it below.

## Create an account on Legifrance API

Go on French government Open Data website https://developer.aife.economie.gouv.fr/  and create an account .![Click there to create an account ](https://i.imgur.com/vfQudXP.jpg)

## Accept ToS on your Sandbox application

Connect on your account, click on the *"Applications"* tab on the top-right corner of the screen. On this page, you should see that a Sandbox application has already been created : ![Create an application](https://i.imgur.com/tJmzhhM.png)  
Note : It is possible that this application doesn't appear. If that's the case, log-out and log-in again and it should appear.
  
Now, click on the application, then click on "Edit application".![enter image description here](https://i.imgur.com/Yel8FhB.png)
Now, scroll down and check the two boxes in front of **'DILA - Légifrance Beta'** on the multiple choice table (see the screenshot below). ![tos checkboxes](https://i.imgur.com/vxIGJPJ.png)
You don't have to check the other boxes.
Now, click on *"Validate my ToS choices"* and then click on *"Save Application"*.


## Fetch a token

Go on the **Sandbox** tab (top-right corner on the purple upper bar, next to your profile picture). Scroll down to **DILA - Légifrance Beta** and click on the "Test the API" button. ![test the api](https://i.imgur.com/XlrUMVh.png) 

Now, wait for the page to fully load. Scroll down a bit to this Test interface :  ![enter image description here](https://i.imgur.com/YpVdBcU.png) 
Click on the *Oauth Credentials* menu and select the application you created just a moment ago. Then, click on the *Oauth Flow* menu and select "Client Credentials". It should look like this :
![token fetch](https://i.imgur.com/31V55tV.jpg)Click on *Request token*, a page will open. ![token fetch 2](https://i.imgur.com/08BgxTq.png)Make sure "openid" is checked, and click on *Authorize*. 

![token screen](https://i.imgur.com/kVVVtN8.jpg)
And there you have it, your Legifrance token! Now copy it in your clipboard, it will be needed to launch the scrapping procedure on Python.

## Launch the scrapping

- If you wish to do the scrapping on Google Colab: open  ***scrapping_notebook.ipynb*** in Google Colab and follow the instructions.
- If you wish to do the scrapping on a local machine: open ***scrap.py*** in your IDE, enter your parameters (such as legifrance_token,...) under the `if __name__ == '__main__' :` at the bottom, then launch the file. (p.s : I advise you to launch the file in a Python Console (and not just Run it); if your session crashes let's say at the saving part because of an invalid `save_path`, you still could relaunch just a small part of the procedure (explained in the files) and not wait an extra 2hours for a small mistake). 
