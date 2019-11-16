Projec goal: Creating a Streaming Platform utilizing Python (Django). The mind map is shown at the bottom of the page.

# Features:

### Search Bar
You could search for movies in the entier system. 
For instance, if you search "Spider man", 
it'll give you all results related to spider man

You could also search for iMDb links - for instance, you could search "tt23333333", it'll return all movies with iMDb links "tt23333333" (which is nothing)

### Fluffy Search
For instance, if you search for "tt66", it will return all movies with iMDb links containing "tt66".

### Word Cloud Implementation
For each movies, we have accessed all comments on iMDb and created a word map based on these comments.
Here is one demo word map for LotR:

![picture](https://github.com/Elnifio/RedVenture/blob/master/RedVenture/redventure/crawler/static/crawler/resources/WordCloud/13.jpg)(https://github.com/Elnifio/RedVenture/blob/master/RedVenture/redventure/crawler/static/crawler/resources/WordCloud/5.jpg)(https://github.com/Elnifio/RedVenture/blob/master/RedVenture/redventure/crawler/static/crawler/resources/WordCloud/1.jpg)

As displayed above, we have mapped out the contours of the poster, and then added popular keywords from all comments.

### Stat Page
All Stat Pages can be found at the bottom of the homepage, 
which traces the number of clicks user make for any particular pages.

You could explore other features by yourself. See Usage below.

* * *

## Usage

1. Pull all contents to your local computer
2. In your local computer, open your terminal, and `cd` to the project folder, and then perform `cd RedVenture/redventure`
3. Before running Django, you should check if current directory contains `manage.py` - simply use `ls` will do the trick.
4. In your terminal, run `python3 manage.py runserver`
5. Open your browser, and visit `127.0.0.1:8000`, the homepage should be available.

### Dependencies
- Django (Obviously)
- json
- re
- requests
- The following modules are not necessary to run `crawler.py`, but is necessary if you wish to mess with this file:
  - BeautifulSoup (For HTML Analysis)
  - wordcloud (for creating WordCloud Pictures)
  - cv2 - OpenCV (for mapping out the contours of the poster, PLEASE USE 3.x.x.xx VERSIONS; If you have 4.x.x.xx installed, then try modifying the codes in `crawler.py` as stated in the comment)
  - numpy
  - io
  - pandas (to calculate the "Better Percentage" index)
  - MatPlotLib (to create WordCloud)

(
If you wish to play around in `crawler.py`, 
be sure to understand how to use Django! 
It's not necessary to understand other modules, 
but it'll be beneficial for you to understand the code.
)

* * *
## Further Extensions
If you wish to add more features to this site, 
please read [django documentation](https://www.djangoproject.com/) 
before making any changes to this project. 

:)


# Credit
Frontend & Backend: @Elnifio

Crawler & WordCloud & "Better Percentage": @Vol0324

Marketing & Product Manager: @wangyf99
