library(httr)
library(plyr)
library(DBI)
library(odbc)
library(dplyr)


Client <- ''   # customer name as in the checklist
Scrypt <- 'Chat2Desk_clients'   # script name as in the checklist

setwd("") # set directory for log-files

# parameters for sql-server
sql_server <- '' # addres sql_server
database_name <- ''       # database name.
table_name <- 'Chat2Desk_clients'

sql_login <- ''             # login to sql-server
sql_pass <- ''      # password to sql-server


headers = c(
  'Authorization' = ''
)


#********************************************************************************    
#                         function connect to SQL-server
#********************************************************************************
connect <- function() {
  conn <- DBI::dbConnect(
    odbc::odbc(),
    driver = "SQL Server",
    server = sql_server,
    database = database_name,
    uid = sql_login,
    pwd = sql_pass,
    encoding = "CP1251")
  return(conn)
}


#********************************************************************************    
#                         get data from Chat2Desk
#********************************************************************************

#res <- VERB("GET", url = "https://api.chat2desk.com/v1/clients/?offset=0&limit=200", add_headers(headers))

clients <- data.frame('assigned_name' = character(),
                      'comment' = character(),
                      'username'= character(),
                      'phone'= character(),
                      'client_phone' = character(),
                      'name' = character(),
                      'avatar' = character(),
                      'region_id' =integer(),
                      'country_id' =integer(),
                      'client_external_id' =integer(),
                      'external_id' =integer(),
                      #'external_ids' =integer(),
                      'extra_comment_1' =character(),
                      'extra_comment_2' =character(),
                      'extra_comment_3' =character(),
                      'id' = integer(),
                      stringsAsFactors=FALSE)


total_res <- VERB("GET", url = paste0("https://api.chat2desk.com/v1/clients/"), add_headers(headers))
total_parsed <- content(total_res, as = "parsed", type = "application/json",encoding="UTF-8")


total <- ceiling(total_parsed[["meta"]][["total"]] / 200)

offset <- 0


for(i in 1:total) {
  
  res <- VERB("GET", url = paste0("https://api.chat2desk.com/v1/clients/?offset=",offset,"&limit=200"), add_headers(headers))
  parsed <- content(res, as = "parsed", type = "application/json",encoding="UTF-8")
  
  data_list <- parsed[["data"]]

  for (i in 1: length(data_list)){ 
    clients[nrow(clients) + 1,] = c(
      ifelse(is.null(data_list[[i]][['assigned_name']]),'',data_list[[i]][['assigned_name']]),
      ifelse(is.null(data_list[[i]][['comment']]),'',data_list[[i]][['comment']]),
      ifelse(is.null(data_list[[i]][['username']]),'', data_list[[i]][['username']]),
      ifelse(is.null(data_list[[i]][['phone']]),'',data_list[[i]][['phone']]),
      ifelse(is.null(data_list[[i]][['client_phone']]),'',data_list[[i]][['client_phone']]),
      ifelse(is.null(data_list[[i]][['name']]),'',data_list[[i]][['name']]),
      ifelse(is.null(data_list[[i]][['avatar']]),'', data_list[[i]][['avatar']]),
      ifelse(is.null(data_list[[i]][['region_id']]),0,data_list[[i]][['region_id']]),
      ifelse(is.null(data_list[[i]][['country_id']]),0,data_list[[i]][['country_id']]),
      ifelse(is.null(data_list[[i]][['client_external_id']]),0,data_list[[i]][['client_external_id']]),
      ifelse(is.null(data_list[[i]][['external_id']]),0,data_list[[i]][['external_id']]),
      #ifelse(is.null(data_list[[i]][['external_ids']]),0,data_list[[i]][['external_ids']]),
      ifelse(is.null(data_list[[i]][['extra_comment_1']]),'',data_list[[i]][['extra_comment_1']]),
      ifelse(is.null(data_list[[i]][['extra_comment_2']]),'',data_list[[i]][['extra_comment_2']]),
      ifelse(is.null(data_list[[i]][['extra_comment_3']]),'',data_list[[i]][['extra_comment_3']]),
      ifelse(is.null(data_list[[i]][['id']]),0,data_list[[i]][['id']])
    )
  }
  
  offset <- offset + 200
  
}

clients <- distinct(clients)

colnames(clients)  <- c('Assigned_name',	'Comment',	'Username',	'Phone',	'Client_phone',	'Name',	'Avatar',	'Region_id',	'Country_id',	'Client_external_id',	'External_id',	'Extra_comment_1',	'Extra_comment_2',	'Extra_comment_3',	'id')

                      
                      
conn <- connect()
                      

dbWriteTable(conn, table_name, clients, overwrite = TRUE)
dbDisconnect(conn)

