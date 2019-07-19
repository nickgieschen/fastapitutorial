## Setting up the database
We're now going to set up our database. The code for this section will be in `main-6.py`. Since we're using a GUI tool to do this, I've created a video walking you through the steps. What I'll show you in the video is:
- Starting Postgres
- Creating a database user
- Creating a database
- Creating a table
- Creating columns
- Populating the table with initial data
- Connecting to the database from our app

<video controls style="width: 100%">
  <source src="../images/database.mp4" type="video/mp4">
</video> 

Much of the time while doing development, you won't modify your database structure this way. Rather, you'll create migration files in which the database structure is modified (tables added, columns added, etc) via a script. The benefit of this is that other people who are working on your app just have to run the scripts to set the database up or make modifications to it. For example, let's say you add a new property to your `User` object called `email`. In this case, we'd want a new column in our `users` table to store the `email`. We would create a migration script (or more likely have a tool like [Alembic](https://www.pythoncentral.io/migrate-sqlalchemy-databases-alembic/) create it.) This would get added to source control. Then when a user pulled down your changes, they would run the migration script which would add the column in their local version of the database. 
