# Hi. Welcome to the Ruby editor window on ScraperWiki.

# To see if everything is working okay, click the RUN button on the bottom left
# to make the following four lines of code do its stuff

(1..10).each do |i|
    puts "Hello, #{i}\n" 
end

# Did it work? 10 lines should have been printed in the console window below
# If not, try using Google Chrome or the latest version of FireFox.

# The first job of any scraper is to download the text of a web-page.  
# Uncomment the next two lines of code (remove the # from the beginning of the line)
# and click RUN again to see how it works.

html = ScraperWiki.scrape('http://scraperwiki.com/hello_world.html')
puts html

# The text will appear in the console, and the URL that it downloaded from
# should appear under "Sources".