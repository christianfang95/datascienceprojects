#Import required packages
library(rvest)
library(tidyverse)

#Store copy in case something goes wrong :)
papers <- final_sample

#Extract paper URLs, convert to proper URLs that can be looped over
URLs <- papers$identifier
URLs <- gsub('[\"]', '', URLs) |> gsub('oai:', 'http://', URLs)
URLs <- gsub('oai:', 'http://www.', URLs)

#Set up empty list to store publication information
pubhistory<-list()  

#Loop through all papers and scrape info
t1 <- Sys.time()
for (i in URLs[40001:50000]) {
  Sys.sleep(1.5)
  paper<-read_html(i)
  print(str(i))
  ex_paper<-paper%>%
    html_nodes(".pubhistory")%>%
    html_text2()
  #ex_paper2<-paper%>%      #Uncomment this if you want to have info about special issues
  #  html_nodes(".belongsTo")%>%
  #  html_text2()
  w<-paste(i,"-",ex_paper )#,"-",ex_paper2)
  pubhistory<-append(w,pubhistory)
  
}
t2 <- Sys.time()
t_seq <- t2 - t1

#Store copy in case I mess something up
copy <- pubhistory


#Clean up result and store as a table
pub_table<-do.call(rbind, pubhistory)%>%
  as_tibble()%>%
  separate(V1,sep=" - ",c("link","Publication"))%>%
  separate(Publication,sep="/",c("Received","Revised","Accepted","Published"))%>%
  drop_na()%>%#remove papers accepted straight away
  distinct()%>% #important, when tasks are performed in different days
  mutate(Received= gsub("Received: ","",Received))%>%
  mutate(Received= lubridate::dmy(gsub(" ","/",Received)))%>%
  mutate(Revised=gsub("Revised: ","",Revised))%>%
  mutate(Revised= lubridate::dmy(gsub(" ","/",Revised)))%>%
  mutate(Accepted=gsub("Accepted: ","",Accepted))%>%
  mutate(Accepted= lubridate::dmy(gsub(" ","/",Accepted)))%>%
  mutate(Published=gsub("Published: ","",Published))%>%
  mutate(Published= lubridate::dmy(gsub(" ","/",Published)))%>%
  mutate(days=Published-Received)

#Merge with Journal info
papers_small <- papers |>
                select(identifier, source) 
papers_small$identifier <- gsub('[\"]', '', papers_small$identifier) 
papers_small$identifier <- gsub('oai:', 'http://www.', papers_small$identifier) 
dates <- data.frame(pub_table)
merged <- merge.data.table(papers_small, dates, by.x='identifier', by.y='link') |>
           separate(source, sep=";", c('Journal', "Vol", "Iss", "Pages")) |>
          select(Journal, Received, Revised, Accepted, Published, days)

#Export as csv for use in Python
write.csv(merged, '/Users/christianfang/Desktop/merged_timedata.csv')


