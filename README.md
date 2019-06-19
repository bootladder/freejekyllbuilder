# A Free Jekyll Builder For You!

You don't need a ruby installation on your laptop to do jekyll builds.  Just put this on a server!  

If you have multiple non-technical writers, building Jekyll sites locally is not an option, so you build on the cloud.  You can set up Travis to build your site, you can build on your own server, or you can use **freejekyllbuilder.com**.  (the site is not up at the moment)

# Usage
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
  
**Here's a description of the pipeline I used:**

* Git push --> Webhook to Travis
* Travis zips the site source and uploads to freejekyllbuilder
* Travis then hits a webhook on the static site server
* Static site server downloads from freejekyllbuilder and deploys


# Installation
`docker-compose up` should work. 
