################################################################################## 
# This R file downloads all MDPI paper metadata from 2012 (earliest year in      #
# data base) until 29 September 2022. Feel free to adapt the code if you execute #
# the analysis at a later point in time!                                         #
#                                                                                #
# Author: Christian Fang                                                         #
##################################################################################

#Install and load required package
install.packages("oai")
library(oai)



#Count number of papers
count_identifiers("http://oai.mdpi.com/oai/oai2.php")
  #Result: There are 930,000(!) papers stored -> This is the majority of MDPI papers

#Load papers. I do this separately because it takes forever if you try to do it in one go.


#2022 papers
papers_2022a <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2022-01-01', until = '2022-02-01')
papers_2022b <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2022-02-02', until = '2022-03-01')
papers_2022c <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2022-03-02', until = '2022-04-01')
papers_2022d <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2022-04-02', until = '2022-05-01')
papers_2022e <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2022-05-02', until = '2022-06-01')
papers_2022f <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2022-06-02', until = '2022-07-01')
papers_2022g <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2022-07-02', until = '2022-08-01')
papers_2022h <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2022-08-02', until = '2022-09-01')
papers_2022i <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2022-09-02', until = '2022-09-30')


#2021 papers
papers_2021a <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-01-01', until = '2021-02-01')
papers_2021b <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-02-02', until = '2021-03-01')
papers_2021c <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-03-02', until = '2021-04-01')
papers_2021d <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-04-02', until = '2021-05-01')
papers_2021e <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-05-02', until = '2021-06-01')
papers_2021f <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-06-02', until = '2021-07-01')
papers_2021g <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-07-02', until = '2021-08-01')
papers_2021h <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-08-02', until = '2021-09-01')
papers_2021i <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-09-02', until = '2021-10-01')
papers_2021j <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-10-02', until = '2021-11-01')
papers_2021k <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-02', until = '2021-11-05')
papers_2021l <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-06', until = '2021-11-10')
papers_2021m <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-11', until = '2021-11-20')
papers_2021n <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-21', until = '2021-11-22')
papers_2021o <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-22', until = '2021-11-23')
papers_2021p <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-23', until = '2021-11-24')
papers_2021q <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-24', until = '2021-11-25')
papers_2021r <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-25', until = '2021-11-26')
papers_2021s <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-26', until = '2021-11-27')
papers_2021v <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-11-29', until = '2021-11-30')
papers_2021w <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-12-01', until = '2021-12-07')
papers_2021x <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-12-08', until = '2021-12-20')
papers_2021y <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2021-12-21', until = '2021-12-31')


#2020 papers
papers_2020a <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-01-01', until = '2020-02-01')
papers_2020b <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-02-02', until = '2020-03-01')
papers_2020c <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-03-02', until = '2020-04-01')
papers_2020d <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-04-02', until = '2020-05-01')
papers_2020e <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-05-02', until = '2020-06-01')
papers_2020f <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-06-02', until = '2020-07-01')
papers_2020g <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-07-02', until = '2020-08-01')
papers_2020h <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-08-02', until = '2020-09-01')
papers_2020i <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-09-02', until = '2020-10-01')
papers_2020j <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-10-02', until = '2020-11-01')
papers_2020k <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-11-02', until = '2020-12-01')
papers_2020l <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2020-12-02', until = '2020-12-31')


#2019 papers
papers_2019a <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-01-01', until = '2019-02-01')
papers_2019b <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-02-02', until = '2019-03-01')
papers_2019c <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-03-02', until = '2019-04-01')
papers_2019d <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-04-02', until = '2019-05-01')
papers_2019e <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-05-02', until = '2019-06-01')
papers_2019f <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-06-02', until = '2019-07-01')
papers_2019g <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-07-02', until = '2019-08-01')
papers_2019h <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-08-02', until = '2019-09-01')
papers_2019i <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-09-02', until = '2019-10-01')
papers_2019j <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-10-02', until = '2019-11-01')
papers_2019k <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-11-02', until = '2019-12-01')
papers_2019l <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2019-12-02', until = '2019-12-31')


#2018 papers
papers_2018 <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2018-01-01', until = '2018-06-01')
papers_2018b <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2018-06-02', until = '2018-07-01')
papers_2018c <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2018-07-02', until = '2018-08-01')
papers_2018d <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2018-08-02', until = '2018-09-01')
papers_2018e <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2018-09-02', until = '2018-10-01')
papers_2018f <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2018-10-02', until = '2018-11-01')
papers_2018g <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2018-11-02', until = '2018-12-01')
papers_2018h <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2018-12-02', until = '2018-12-31')


#These run very quickly, not too many rows, so I did not split them up:
papers_2017 <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2017-01-01', until = '2017-12-31')
papers_2016 <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2016-01-01', until = '2016-12-31')
papers_2015 <- list_records("http://oai.mdpi.com/oai/oai2.php", from = '2015-01-01', until = '2015-12-31')
papers_2014 <- list_records("http://oai.mdpi.com/oai/oai2.php",  until = '2014-12-31')

#Concatenate papers into one data frame
library(data.table)
all_papers <- rbindlist(list(papers_2022a, papers_2022b, papers_2022c, papers_2022d, papers_2022e,
                             papers_2022f, papers_2022g, papers_2022h, papers_2022i, papers_2021a,
                             papers_2021b, papers_2021c, papers_2021d, papers_2021e, papers_2021f,
                             papers_2021g, papers_2021h, papers_2021i, papers_2021j, papers_2021k,
                             papers_2021l, papers_2021m, papers_2021n, papers_2021o, papers_2021p,
                             papers_2021q, papers_2021r, papers_2021s, papers_2021v, papers_2021w, 
                             papers_2021x, papers_2021y, papers_2020a, papers_2020b, papers_2020c,
                             papers_2020d, papers_2020e, papers_2020f, papers_2020g, papers_2020h,
                             papers_2020i, papers_2020j, papers_2020k, papers_2020l, papers_2019a,
                             papers_2019b, papers_2019c, papers_2019d, papers_2019e, papers_2019f,
                             papers_2019g, papers_2019h, papers_2019i, papers_2019j, papers_2019k,
                             papers_2019l, papers_2018, papers_2018b, papers_2018c, papers_2018d,
                             papers_2018e, papers_2018f, papers_2018g, papers_2018h, papers_2017,
                             papers_2016, papers_2015, papers_2014), fill = TRUE)
#Export data frame as .csv
write.csv(all_papers, "all_papers.csv")


