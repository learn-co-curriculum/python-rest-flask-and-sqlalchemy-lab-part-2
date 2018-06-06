
# Flask and Flask-SQLAlchemy Lab Part 2

## Introduction
In this lab we are going to practice working with creating a RESTful web app that returns HTML about Tweets and Users. In this domain Users will have many Tweets and Tweets will, therefore, belong to a User. We already have our app's database set up. We will create HTML templates to render views for all of our user and tweet information stored in the database. We will query the database for the proper information, depending upon the URL, to pass onto the templates for HTML rendering. Let's get started!

## Objectives
* Create templates that display data for individual and collections of users and tweets
* Define RESTful Routes that return HTML for Users
* Define RESTful Routes that return HTML for Tweets
* **Bonus:** Define RESTful Rotues that return HTML for related resources

The configuration for our app will be exactly the same as that from the previous lab when we created the API. All of this configuration code has been provided for us in the app.py file. Note that our models and seed data are also exactly the same.

> **Note:** remember to seed your database by running `python seed.py` from your terminal so that your database will be populated with the necessary tables and some pre-populated data.

## Defining RESTful Routes for User Data

 Our routes for our User resource should follow REST convention and return HTML for:
 * A list of all user objects
 * A single user object whose `id` matches the id in the URL
 * A list of users with a whose `username` contains the string in the URL

## Defining RESTful Routes for Tweet Data

Our routes for our Tweet resource should follow REST convention and return HTML for:
* A list of all tweet objects
* A single tweet object that has the same `id` as the id in the URL

## Create Templates

Given the above routes, we will need to create four (4) HTML templates. In our templates directory, we have four files named, tweets.py, tweet_show.py, users.py, and user_show.py. The files with the pluralized resource name will be our templates for a collection of the given resource and the files named `[resource]_show` will be for a single object of the given resource. 

### Multiple Users:
When multiple users are requested, the format should be an ordered list with each list item containing an `h3` tag showing the user's `username`, an `h4` tag showing the user's `id`, and another `h4` tag showing the number of `tweets` that user has tweeted.

**example:**

<ol>
    <li>
        <h3>Username: "USERNAME"</h3>
        <h4>ID: "ID"</h4>
        <h4>Tweet Count: "NUMBER OF TWEETS FROM USER"</h4>
    </li>
    <li>
        <h3>Username: "USERNAME"</h3>
        <h4>ID: "ID"</h4>
        <h4>Tweet Count: "NUMBER OF TWEETS FROM USER"</h4>
    </li>
</ol>


### Single User:
A single user's page should have an `h3` tag for their `username`, a `p` tag for their `id`, an `h4` tag that has the text "Tweets:" followed by an unordered list containing all of the user's tweets each list item showing the tweet's `user_id` and content, which is a tweet's `text`.

**example:**

<h3>Username: "USERNAME"</h3>
<p>ID: "ID"</p>
<h4>Tweets:</h4>
<ul>
    <li>
        <p>User ID: "TWEET USER_ID"</p> 
        <p>Content: "TWEET CONTENT"</p>
    </li>
</ul>

### Multiple Tweets:
When multiple tweet's are requested the page should have an undordered list showing each tweet. Each list item should have an `h4` tag for the tweet's author (or the username of the user who wrote the tweet), and a `p` tag for its content or `text`.

**example:**

<ul>
    <li>
        <h4>Author: "TWEET'S AUTHOR'S USERNAME"</h4> 
        <p>Content: "TWEET CONTENT"</p>
    </li>
    <li>
        <h4>Author: "TWEET'S AUTHOR'S USERNAME"</h4> 
        <p>Content: "TWEET CONTENT"</p>
    </li>
</ul>

### Single Tweet:
A single tweet's page should have an `h4` tag for its author (or the username of the user who wrote the tweet), and a `p` tag for its content or `text`, and another `p` tag showing the tweet's `user_id`.

**example:**

<h4>Author: "TWEET'S AUTHOR'S USERNAME</h4>
<p>Content: "TWEET CONTENT"</p>
<p>User ID: "TWEET USER_ID"</p>

## BONUS:

## Defining Nested RESTful Routes that Display Related Resources

Since we are dealing with a has many / belongs to relationship we will want to define routes that return an HTML template that displays the data for the requested related resource(s). We will want routes that, again follow the REST convention and return an HTML template for:
* Tweets that belong to a user by `user_id`
* Tweets that belong to a user by a user's `name`   
* A single User that is associated to a tweet by its `id` 

## Summary

In this lab, we practiced creating HTML templates for our different views. We queried our database to extract the necessary resources to pass along to our templates, which then rendered our web pages in the correct HTML format. We used the REST convention to create common sense routes that describe the application and what information the page ought to display based upon what the client requested in the URL. Finally, as a bonus, we used nested RESTful routes to display a resource's related resources (i.e. a particular user's tweets).
