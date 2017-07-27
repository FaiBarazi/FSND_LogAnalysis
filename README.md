# News Data Analysis
In this project, a news data base is analyzed to answer 3 questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Running the analysis 
### Requirements:

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
- [Vagrant](https://www.vagrantup.com/downloads.html)
- python 3

###  Setup:
- Install VirtualBox to create a virtual database server on your machine.
- Install Vagrant which configures the VM and lets you share files between your host computer and the VM's filesystem.
- Download the [VM Setup](https://github.com/udacity/fullstack-nanodegree-vm) file from udacity for fast setup. 
- download the [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- Save the newsdata.sql file in the VM setup folder downloaded.
- On the terminal go the directory of the VM Setup and run: 

```
$ vagrant up
```
```
$ vagrant ssh
```
### Loading the data
To load the data run

```
/vagrant$ psql -d news -f newsdata.sql
```
Connect to the data base by running `psql -d news`
This will create a database called news. The data base has 3 tables: `authors,articles and log.` 
These can be explored by typing \d and the name of the table:
```
news=> \d log
```
### Creating required views:
The python code requires  views that are set in the code these are: 

- popular_articles
- total_log
- failed_log

To set these run: 

```
news=>create view  popular_articles as
select slug,count(*) as views from 
(select slug,path from articles, log where log.path like '%'||articles.slug||'%')
as new_log group by new_log.slug order by views desc;
```
```
news=>create view total_log as select date(time) as date,count(log.status) 
as total_views from log where status = '404 NOT FOUND' or status = '200 OK' 
group by date;
```
```
news=>create view  failed_log  as select date(time) as date,count(status) as failed_views 
from log where status = '404 NOT FOUND' group by date;
```
### Running the code:
Make sure to save LogAnalysis.py in the vagrant folder. 
run:
```
/vagrant$python3 LogAnalysis.py
```






