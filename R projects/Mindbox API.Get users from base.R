# package on
library(dplyr)
library(httr)
library(DBI)
library(odbc)
library(googlesheets4)
#*******************************************************************************
#                              data of query - edit!
#*******************************************************************************


Client <- ''   # customer name as in the checklist
Scrypt <- 'Base'   # script name as in the checklist

setwd("") # set directory for log-files

# parameters for sql-server
sql_server <- '' # addres sql_server
database_name <- ''       # database name
table_name <- 'Base_expanded'

sql_login <- ''             # login to sql-server
sql_pass <- ''      # password to sql-server

# parameters for mindbox
endpoint_Id <- ''
ApiKey <- 'Mindbox secretKey=""'
operation <- 'AdvancedExportForPowerBI'


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
        
        colnames(table)  <- c('CustomerId', 'FirstName', 'MiddleName', 'LastName', 'BirthDate', 'Gender', 'LastChangedUtc', 'TimeZone', 'TimeZoneSource', 'IsEmailInvalid', 'IsPhoneInvalid', 'Email', 'MobilePhone', 'SmsSubscribed', 'EmailSubscribed', 'ViberSubscribed', 'MobilePushSubscribed', 'WebPushSubscribed', 'City', 'Organization', 'Speciality', 'SpecialityOther')
        
        print("Save to sql-server")
        conn <- connect()
        

        dbWriteTable(conn, table_name, table, overwrite = TRUE)
        dbDisconnect(conn)







