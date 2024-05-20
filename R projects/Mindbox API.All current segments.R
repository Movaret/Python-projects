# package on
library(dplyr)
library(httr)
library(DBI)
library(odbc)
library(googlesheets4)
library(data.table)
#*******************************************************************************
#                              data of query - edit!
#*******************************************************************************


Client <- ''   # customer name as in the checklist
Scrypt <- 'Segments'   # script name as in the checklist

setwd("") # set directory for log-files

# parameters for sql-server
sql_server <- '' # addres sql_server
database_name <- ''       # database name. Important!!! The database must be on the server.
table_name <- 'Segments'

sql_login <- ''             # login to sql-server
sql_pass <- ''      # password to sql-server

# parameters for mindbox
endpoint_Id <- ''
ApiKey <- 'Mindbox secretKey=""'
operation <- 'SegmentsExportForPowerBI'


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
#                         get data from mindbox
#********************************************************************************

url <-
  paste0(
    "https://api.mindbox.ru/v3/operations/sync?endpointId=",
    endpoint_Id,
    "&operation=",
    operation
  )

        get_answer  <-  POST(url,
                             body = "",
                             content_type("application/json"),
                             add_headers(.headers = c(Accept = "application/json", Authorization = ApiKey)
                             ))
        parsed <- content(get_answer, as = "parsed", type = "application/json")
        exportID <- parsed[["exportId"]]
       
        print(exportID)

        body <- paste("{'exportID': '", exportID, "'}", sep = '')
        repeat {
          get_answer  <-  POST(url,
                               body = body,
                               content_type("application/json"),
                               add_headers(
                                 .headers = c(Accept = "application/json", Authorization = ApiKey)
                               ))
          parsed <- content(get_answer, as = "parsed", type = "application/json")
          if (!is.null(parsed[["exportResult"]][["processingStatus"]])) {
            if (parsed[["exportResult"]][["processingStatus"]] != "NotReady")
              break
          }
          print("Query data")
          Sys.sleep(10)
        }
        
        
        table <- data.frame()
            for (k in 1:length(parsed[["exportResult"]][["urls"]])) {
              urls <- parsed[["exportResult"]][["urls"]][[k]]
              data_temp <- data.table::fread( urls,
                                              stringsAsFactors = FALSE,
                                              sep = ";",
                                              encoding = "UTF-8")
              table <- rbind(table, data_temp)
            }
        
        #Транспонируем таблицу, чтобы из 30+ столбцов оставить 3
        x <- as.data.table(table)
        z <- melt(x, id = c("CustomerIdsMindboxId"), variable.name = "Segment", value.name = "Status")
        
        
        #Отбираем только уников
        uniques <- z[z$Status %in% c('Pv Email Contactable DB', 'Pv WA Contactable DB')]
        
        uniques <- subset(uniques, select = -c(Segment, Status))
        
        uniques$Segment <- as.character('CustomerSegmentationPvUnique')
        uniques$Status <- as.character('Pv Unique Contactable DB')
        
        uniques <- uniques %>% group_by(Segment, Status) %>%
          summarise(total_count = n_distinct(CustomerIdsMindboxId), .groups = 'drop')
        
        uniques$Date <- as.Date(Sys.Date())

        
        #Группируем всех остальных, добавляем сегодняшнюю дату для истории
        z <- z %>% group_by(Segment,Status) %>%
          summarise(total_count = n_distinct(CustomerIdsMindboxId), .groups = 'drop')
        
        z$Date <- as.Date(Sys.Date())
        
        
        
        segments <- union_all(z, uniques)
        
        colnames(segments)  <- c('Segment', 'Status', 'Quantity', 'Date')
        
        
        
        print("Save to sql-server")
        conn <- connect()
        
        dbAppendTable(conn, table_name , segments, row.names = NULL)
        dbDisconnect(conn)







