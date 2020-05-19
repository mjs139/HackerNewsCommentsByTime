#!/usr/bin/env python
# coding: utf-8

# # Analyzing Hacker News Comment Data in Python
# 
# In this Python project, I will work through Hacker News data found [here](https://www.kaggle.com/hacker-news/hacker-news-posts) to determine how time affects the number of comments a post receives. I will focus on Ask HN and Show HN posts. I will also look to see if one type of posts receives more comments than another. 

# In[1]:


from csv import reader
opened_file = open('hacker_news.csv')
read_file = reader(opened_file)
hn = list(read_file)
print(hn[0:4])


# I will now separate the header from the rest of the data. 

# In[2]:


headers = hn[0]
hn = hn[1:]
print(headers)
print(hn[0:4])


# I will now filter my data. In this analysis, I am only concerns with post titles beginning with "Ask HN" and "Show HN". I will create two lists of lists containing the data for those titles.  

# In[11]:


ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1].lower()
    if title.startswith('ask hn'):
        ask_posts.append(row)
    elif title.startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)
        
print("The number of Ask HN posts is ", len(ask_posts))
print("The number of Show HN posts is ", len(show_posts))
print("The number of Other HN posts is ", len(other_posts))


# I have 1744 Ask HN posts and 1162 Show HN posts to analyze. I will print out the first five rows of my Ask HN list to make sure that my code was working. 

# In[13]:


print(ask_posts[0:4])


# I will now determine if ask posts or show posts receive more comments on average. I will accomplish this by finding the number of comments in each post, and then averaging that out. 

# In[33]:


total_ask_comments = 0

for row in ask_posts:
    num_comments = int(row[4])
    total_ask_comments += num_comments
    
avg_ask_comments = total_ask_comments / len(ask_posts)

print("The average number of comments for a Ask HN post is ", round(avg_ask_comments, 1))


total_show_comments = 0

for row in show_posts:
    num_comments = int(row[4])
    total_show_comments += num_comments
    
avg_show_comments = total_show_comments / len(show_posts)

print("The average number of comments for a Show HN post is ", round(avg_show_comments, 1))
    


# We can see that Ask HN posts receive roughly 4 more comments on average than Show HN posts. Since ask posts are more likely to receive comments, the rest of this analysis will focus on just these posts. 
# 
# ### Affect of Time on Ask HN Posts
# 
# Next, I will try to determine how time affects the number of comments for Ask HN posts. I will find how many comments are made during different hours in the day

# In[35]:


import datetime as dt


# In[45]:


result_list = []

for row in ask_posts:
    created_at = row[6]
    num_comments = int(row[4])
    info = [created_at, num_comments]
    result_list.append(info)
    
counts_by_hour = {}
comments_by_hour = {}
date_format = "%m/%d/%Y %H:%M"

for row in result_list:
    date = row[0]
    comments = row[1]
    time = dt.datetime.strptime(date, date_format).strftime("%H")
    
    if time not in counts_by_hour:
        counts_by_hour[time] = 1
        comments_by_hour[time] = comments
    else:
        counts_by_hour[time] += 1
        comments_by_hour[time] += comments
    
print(counts_by_hour)
print(comments_by_hour)


# I will now use the previous dictionaries to calculate the average number of comments for posts created during each hour of the day. 

# In[57]:


avg_by_hour = []

for row in counts_by_hour:
    time = int(row)
    counts = int(counts_by_hour[row])
    num_comments = comments_by_hour[row] 
    avg = num_comments / counts
    avg_counts_per_hour = [time, avg]
    avg_by_hour.append(avg_counts_per_hour)
    
print(avg_by_hour)
print('\n')
print("The hour with the most comments is ", max(avg_by_hour, key=lambda x: x[1]))
print("The hour with the fewest comments is ", min(avg_by_hour, key=lambda x: x[1]))


# On average, the post time for an Ask HN post with the most comments is 3PM, whereas the post time with the fewest comments is 9AM. Let's now sort our data to find the top 5 hours for Ask HN post comments

# In[72]:


swap_avg_by_hour = []

for row in avg_by_hour:
    hour = row[0]
    comments = row[1]
    switch = [comments, hour]
    swap_avg_by_hour.append(switch)
    
print(swap_avg_by_hour)
print('\n')

sorted_swap = sorted(swap_avg_by_hour, reverse = True)
print(sorted_swap)
print('\n')

print("Top 5 Hours for Ask HN Posts Comments")

count = 0
for row in sorted_swap:
    time = str(row[1])
    hour = dt.datetime.strptime(time, "%H").strftime("%H:%M")
    avg = round(row[0], 2)
    count += 1
    if count < 6:
        print(hour,": ", avg, " average comments per post")
    else:
        break
    



# ### Conclusion
# 
# These results are interesting. If you wish to receive the most comments for a Ask HN post, you should post it at 3PM, 2AM, 8PM, 4PM, or 9PM. I see two main time-intervals: between 3-5PM and 8-10PM. 
