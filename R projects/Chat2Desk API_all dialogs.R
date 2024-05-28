library(httr)
library(plyr)
library(DBI)
library(odbc)
library(dplyr)


Client <- ''   # customer name as in the checklist
Scrypt <- 'Chat2Desk_dialogs'   # script name as in the checklist

setwd("") # set directory for log-files

# parameters for sql-server
sql_server <- '' # addres sql_server
database_name <- ''       # database name
table_name <- 'Chat2Desk_dialogs'

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

#res <- VERB("GET", url = "https://api.chat2desk.com/v1/dialogs/?offset=0&limit=200", add_headers(headers))

dialogs <- data.frame('id' = integer(),
                      'state' = character(),
                      'begin'= character(),
                      'end'= character(),
                      'operator_id' = integer(),
                      'transport' = character(),
                      'client_id' = integer(),
                      'channel_id' = integer(),
                      'text' = character(),
                      'status' = character(),
                      
                       stringsAsFactors=FALSE)



total_res <- VERB("GET", url = paste0("https://api.chat2desk.com/v1/dialogs/"), add_headers(headers))
total_parsed <- content(total_res, as = "parsed", type = "application/json",encoding="UTF-8")


total <- ceiling(total_parsed[["meta"]][["total"]] / 200)


offset <- 0


for(i in 1:total) {
  
  res <- VERB("GET", url = paste0("https://api.chat2desk.com/v1/dialogs/?offset=",offset,"&limit=200"), add_headers(headers))
  parsed <- content(res, as = "parsed", type = "application/json",encoding="UTF-8")
  
  data_list <- parsed[["data"]]

  for (i in 1: length(data_list)){ 
    dialogs[nrow(dialogs) + 1,] = c(
      ifelse(is.null(data_list[[i]][['id']]),'',data_list[[i]][['id']]),
      ifelse(is.null(data_list[[i]][['state']]),'',data_list[[i]][['state']]),
      ifelse(is.null(data_list[[i]][['begin']]),'', data_list[[i]][['begin']]),
      ifelse(is.null(data_list[[i]][['end']]),'',data_list[[i]][['end']]),
      ifelse(is.null(data_list[[i]][['operator_id']]),'',data_list[[i]][['operator_id']]),
      ifelse(is.null(data_list[[i]][['last_message']][['transport']]),'',data_list[[i]][['last_message']][['transport']]),
      ifelse(is.null(data_list[[i]][['last_message']][['client_id']]),'',data_list[[i]][['last_message']][['client_id']]),
      ifelse(is.null(data_list[[i]][['last_message']][['channel_id']]),'',data_list[[i]][['last_message']][['channel_id']]),
      ifelse(is.null(data_list[[i]][['last_message']][['text']]),'',data_list[[i]][['last_message']][['text']]),
      ifelse(is.null(data_list[[i]][['last_message']][['status']]),'',data_list[[i]][['last_message']][['status']])
      
    )
  }
  
  offset <- offset + 200
  
}


colnames(dialogs)  <- c('Id',	'State', 'Begin', 'End', 'Operator_id', 'Transport', 'Client_id', 'Channel_id', 'Text', 'Status')

                      
conn <- connect()
                      

dbWriteTable(conn, table_name, dialogs, overwrite = TRUE)
dbDisconnect(conn)

