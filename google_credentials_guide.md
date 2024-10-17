# Google oauth setup guide

## Get Google credentials
1. Go to [this link](https://console.cloud.google.com)

2. Login with a @ku.th account.

3. Select project name. 
    ![Google cloud console](./google_oauth_guide_pic/Google%20cloud%20page.png)

4. Create new project
    ![Create new project](./google_oauth_guide_pic/Create%20new%20project.png)

5. Fill project name then click create.
    ![Fill project name](./google_oauth_guide_pic/Input%20project%20name.png)

6. Back to main page and select project name on the top of page.
    ![Select Project name](./google_oauth_guide_pic/Google%20cloud%20page.png)

7. Select project name that you've just created.
    ![Choose new project name](./google_oauth_guide_pic/Select%20project%20name.png)

8. Create oauth consent screen. by select hamburger icon > APIs & Services > oAuth consent screen.
    ![Create consent screen](./google_oauth_guide_pic/Select%20oauth%20consent%20screen.png)

9. Select user type to be internal.
    ![Select user type](./google_oauth_guide_pic/Select%20internal.png)

10. Fill App name, User support email, Developer Contact information then click save and continue
    ![Fill app info](./google_oauth_guide_pic/Fill%20app%20information.png)

11. Select scope. Check email and profile checkbox then click update then scroll down to click save and continue.
    ![Select scope](./google_oauth_guide_pic/Select%20scope.png)

12. After see a summary page, click credentials tab on a side bar. Then click create credentials.
    ![Create cred](./google_oauth_guide_pic/create%20credential.png)

13. Select **Web Appplication** as a application type
    ![App type](./google_oauth_guide_pic/Select%20app%20typw.png)

14. Add authorized JavaScript origin.

    First: http://localhost:8080

    (optional): http://127.0.0.1:8080

    (Optional: if you want to login from backend add this too, but it's mostly unnecessary)

    Scroll down and add 2 URI.

    First: http://127.0.0.1:8000

    Second: http://127.0.0.1:8000/accounts/google/login/callback/

    (optional) add 2 more URI by replace `127.0.0.1` with `localhost`

    ![add uri](./google_oauth_guide_pic/Add_uri.png)
    
15. oauth credentials already created. Save client ID and Client secret somewhere.

    ![Complete](./google_oauth_guide_pic/oauth%20created.png)


## Set up social application on Django admin.

1. Create super user.
```python manage.py create superuser```

2. Run server.
```python manage.py runserver```

3. Go to admin page by go to `http://127.0.0.1:8000/admin/`

4. Add new site. by fill

    Domain name: `http://127.0.0.1:8000`

    Display name: `http://127.0.0.1:8000`

    Then click save.

    ![add site](./google_oauth_guide_pic/Add%20site.png)

5. Add social application, by select Google as a Provider, leave Provider ID blank, fill name. Get client ID and Secret key from google credentials that we've just created 

    ![add sociall app](./google_oauth_guide_pic/Add%20social%20app.png)

6. scroll down then add site to social app, then click save.

    ![Add site to social app](./google_oauth_guide_pic/Add%20site%20to%20social%20app.png)

## Test Google login

1. Go to 'http://127.0.0.1:8000/accounts/google/login/' and click continue it's should lead you to google login. You must login with KU account.
2. After login complete, it's should show `{"is_authen": true}` after redirect.

## Test Logout

1. Go to 'http://127.0.0.1:8000/accounts/logout/' and click continue.
2. After login complete, it's should show `{"is_authen": false}` after redirect.







