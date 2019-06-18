# A Free Jekyll Builder For You!
    If you have multiple non-technical writers, building Jekyll sites locally is not an option, so you build on the cloud.  You can set up Travis to build your site, you can build on your own server, or you can use **freejekyllbuilder.com**.  (the site is not up at the moment)

    **Build your site:**   
      
    First zip it up at the root and note its location.  
    ```
    zip -r sitesource.zip *;  mv sitesource.zip /tmp
    ```
    Then curl it up to freejekyllbuilder.com  
    ```
    curl -F 'doesntmatter=@/tmp/sitesource.zip' freejekyllbuilder.com/upload/mygeneratedusername1
    ```
    Wait for the response, and you are ready to download!   
      
    **Download your site:** 
    ```
    wget freejekyllbuilder.com/download/mygeneratedusername1
    ```
    **Deploy your site:**  
    You know what to do.  Unzip the _site and deploy the contents in your web root!



You don't need a ruby installation on your laptop to do jekyll builds.  
Just use this!  


# Details: 
the docker-compose will volume mount the directories:
files/  is where the audio message blobs get stored.
boundary/  is where use cases are.  they are all executable.

To use the server, make symlinks to where the files and boundary actually is

The symlinks are not in the repository, you have to create them.
