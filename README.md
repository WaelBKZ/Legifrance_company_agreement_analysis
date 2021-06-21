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

## Export a file

You can export the current file by clicking **Export to disk** in the menu. You can choose to export the file as plain Markdown, as HTML using a Handlebars template or as a PDF.


# Synchronization

Synchronization is one of the biggest features of StackEdit. It enables you to synchronize any file in your workspace with other files stored in your **Google Drive**, your **Dropbox** and your **GitHub** accounts. This allows you to keep writing on other devices, collaborate with people you share the file with, integrate easily into your workflow... The synchronization mechanism takes place every minute in the background, downloading, merging, and uploading file modifications.

There are two types of synchronization and they can complement each other:

- The workspace synchronization will sync all your files, folders and settings automatically. This will allow you to fetch your workspace on any other device.
	> To start syncing your workspace, just sign in with Google in the menu.

- The file synchronization will keep one file of the workspace synced with one or multiple files in **Google Drive**, **Dropbox** or **GitHub**.
	> Before starting to sync files, you must link an account in the **Synchronize** sub-menu.

## Open a file

You can open a file from **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Open from**. Once opened in the workspace, any modification in the file will be automatically synced.

## Save a file

You can save any file of the workspace to **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Save on**. Even if a file in the workspace is already synced, you can save it to another location. StackEdit can sync one file with multiple locations and accounts.

## Synchronize a file

Once your file is linked to a synchronized location, StackEdit will periodically synchronize it by downloading/uploading any modification. A merge will be performed if necessary and conflicts will be resolved.

If you just have modified your file and you want to force syncing, click the **Synchronize now** button in the navigation bar.

> **Note:** The **Synchronize now** button is disabled if you have no file to synchronize.

## Manage file synchronization

Since one file can be synced with multiple locations, you can list and manage synchronized locations by clicking **File synchronization** in the **Synchronize** sub-menu. This allows you to list and remove synchronized locations that are linked to your file.


# Publication

Publishing in StackEdit makes it simple for you to publish online your files. Once you're happy with a file, you can publish it to different hosting platforms like **Blogger**, **Dropbox**, **Gist**, **GitHub**, **Google Drive**, **WordPress** and **Zendesk**. With [Handlebars templates](http://handlebarsjs.com/), you have full control over what you export.

> Before starting to publish, you must link an account in the **Publish** sub-menu.

## Publish a File

You can publish your file by opening the **Publish** sub-menu and by clicking **Publish to**. For some locations, you can choose between the following formats:

- Markdown: publish the Markdown text on a website that can interpret it (**GitHub** for instance),
- HTML: publish the file converted to HTML via a Handlebars template (on a blog for example).

## Update a publication

After publishing, StackEdit keeps your file linked to that publication which makes it easy for you to re-publish it. Once you have modified your file and you want to update your publication, click on the **Publish now** button in the navigation bar.

> **Note:** The **Publish now** button is disabled if your file has not been published yet.

## Manage file publication

Since one file can be published to multiple locations, you can list and manage publish locations by clicking **File publication** in the **Publish** sub-menu. This allows you to list and remove publication locations that are linked to your file.


# Markdown extensions

StackEdit extends the standard Markdown syntax by adding extra **Markdown extensions**, providing you with some nice features.

> **ProTip:** You can disable any **Markdown extension** in the **File properties** dialog.


## SmartyPants

SmartyPants converts ASCII punctuation characters into "smart" typographic punctuation HTML entities. For example:

|                |ASCII                          |HTML                         |
|----------------|-------------------------------|-----------------------------|
|Single backticks|`'Isn't this fun?'`            |'Isn't this fun?'            |
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|


## KaTeX

You can render LaTeX mathematical expressions using [KaTeX](https://khan.github.io/KaTeX/):

The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is via the Euler integral

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$

> You can find more information about **LaTeX** mathematical expressions [here](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference).


## UML diagrams

You can render UML diagrams using [Mermaid](https://mermaidjs.github.io/). For example, this will produce a sequence diagram:

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

And this will produce a flow chart:

```mermaid
graph LR
A[Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D
```
