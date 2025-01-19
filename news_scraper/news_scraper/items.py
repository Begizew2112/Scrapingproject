import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    publication_date = scrapy.Field()
    body = scrapy.Field()

# //*[@id="lists"]/li[7] 
# //*[@id="lists"]/li[8]
# ...
# //*[@id="lists"]/li[50]

#/html/body/div[2]/div/div[1]/div/h1
# path of u 
# /html/body/div[2]/div/div[1]/div/h1...title
# /html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[1].. view
# /html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[2]..date
# /html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[3]..source
# /html/body/div[2]/div/div[1]/div/div[2]/article .. article

# //*[@id="lists"]/li[8] <l>
# /html/body/div[2]/div/div[1]/div/h1 ...title
# /html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[1]...view
# /html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[2]...date
# /html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[3]...source
# /html/body/div[2]/div/div[1]/div/div[2]/article ...article 


# //*[@id="lists"]/li[9]
# //*[@id="lists"]/li[50]

# //*[@id="lists"]/li[7]/div[1]/h4
# //*[@id="lists"]/li[8]/div[1]/h4

# //*[@id="lists"]/li[7]/div[1]/h4/a
# //*[@id="lists"]/li[8]/div[1]/h4/a
# //*[@id="lists"]/li[7]/div[1]/h4/a