"""
TODO
- Create a ApiView class to handle activity detail request and edit activity request.
- Wire this class view to URL /activities/<activity_id> where
    - If request is GET return activity detail that has id equal to activity_id.
    - If request is PUT update activity according to request content where it's id equal to activity_id.
    - Edit activity is limit to host of an activity therefore, we need permission class to enforce it.
    - Fix _test_detail.py and test_edit_activity.py after create a ApiView class 
- Refer to this docs
    Class base API view https://www.django-rest-framework.org/tutorial/3-class-based-views/
    Permission class https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
"""