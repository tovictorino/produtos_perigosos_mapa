library(rgdal)
library(mapview)
library(leaflet)
library(RColorBrewer)
library(dplyr)
library(sf)

####################### AJUSTE DAS CAMADAS DO SHAPEFILE #######################

# Leitura das bases georreferenciadas
## myshp = linhas. myshp3 = estações
myshp <- readOGR(dsn=path.expand("shp_atualizado"),
                 layer="dbo_tblLinhaEstacao_spatial_linestring", stringsAsFactors = FALSE)


# Substituição do CodigoFerr, antes numérico, agora string, com o nome das estações
tblFerrovia <- readxl::read_excel("Dados/tblFerrovia.xlsx")
tblFerrovia$CodigoFerr <- tblFerrovia$CodigoFerrovia
myshp@data <- plyr::join(myshp@data,
                         tblFerrovia,
                         by='CodigoFerr')

# Substituição dos códigos de linha pelo nome completo
tblLinha <- readxl::read_excel("Dados/tblLinha.xlsx")
tblLinha$CodigoLi00 <- tblLinha$CodigoLinha
myshp@data <- plyr::join(myshp@data,
                  tblLinha,
                  by='CodigoLi00')

# Substituição dos códigos de estação pelo código de três letras
tblEstacao <- readxl::read_excel("Dados/tblEstacao.xlsx")
tblEstacao$CodigoEsta <- tblEstacao$CodigoEstacao
myshp@data <- plyr::join(myshp@data,
                         tblEstacao,
                         by='CodigoEsta')
DR_2020 <- readxl::read_excel("Dados/dr2020_original.xlsx")
DR_2020$linesta <- paste(DR_2020$Linha, DR_2020$B, sep='!')
myshp@data$linesta <- paste(myshp@data$NomeLinha, myshp@data$CodigoTresLetrasEstacao, sep='!')
myshp@data <- plyr::join(myshp@data,
                         DR_2020,
                         by='linesta')


# Substituição dos códigos de bitola pela sua classificação real
{myshp@data[myshp@data[["CodigoBito"]] == '1', 'CodigoBito'] <- 'Métrica'
  myshp@data[myshp@data[["CodigoBito"]] == '3', 'CodigoBito'] <- 'Larga'
  myshp@data[myshp@data[["CodigoBito"]] == '5', 'CodigoBito'] <- 'Mista'}


# Colocando a TU
DR_TU <- read.table("Dados/perigoso_2019.csv",
                    sep=';', dec=',', header=TRUE)
DR_TU$AB <- NA
DR_TU$AB <- paste(DR_TU$A, DR_TU$B, sep=" - ")


myshp@data$AB <- NA
myshp@data$AB <- paste(myshp@data$A,
                       myshp@data$B, sep=" - ")

myshp@data <- plyr::join(myshp@data,
                         DR_TU,
                         by='AB',
                         match="first")

red = colorRampPalette(c('green', 'yellow', 'red'))

myshp@data$TU2019 <- ifelse(myshp@data$TU2019 == 0, NA, myshp@data$TU2019)
myshp@data$TU2018 <- ifelse(myshp@data$TU2018 == 0, NA, myshp@data$TU2018)
myshp@data$TU2017 <- ifelse(myshp@data$TU2017 == 0, NA, myshp@data$TU2017)
myshp@data$TU2016 <- ifelse(myshp@data$TU2016 == 0, NA, myshp@data$TU2016)
myshp@data$TU2015 <- ifelse(myshp@data$TU2015 == 0, NA, myshp@data$TU2015)

# Drop das colunas desnecessarias
myshp@data <- myshp@data[ , !names(myshp@data) %in% c("CodigoLinh", "CodigoLi00",
                                                      "CodigoEsta", "CodigoBito",
                                                      "NumeroSequ", "IndicadorC",
                                                      "IndicadorE", "CodigoLinha",
                                                      "CodigoEstacao", "CodigoTresC",
                                                      "CodigoLinh", "CodigoLi00",
                                                      "CodigoEsta", "CodigoFerr",
                                                      "CodigoFerrovia", "SiglaFerrovia",
                                                      "LogotipoFerrovia", "DataExclusao",
                                                      "IndicadorObrigatorioDesempenhoProducao",
                                                      "CodigoLinha", "CodigoEstacao",
                                                      "linesta", "Ferrovia", "Linha",
                                                      "X", "Ferrovia", "Linha", "A", "B",
                                                      "x", "CodigoTresLetrasEstacao",
                                                      "ExtensÃ.o..km.")]

colnames(myshp@data)[which(names(myshp@data) == "NumeroQuil")] <- "Marco Quilométrico"
colnames(myshp@data)[which(names(myshp@data) == "NumeroExte")] <- "Extensão do Entre Pátio (km)"
colnames(myshp@data)[which(names(myshp@data) == "NomeFerrovia")] <- "Ferrovia"
colnames(myshp@data)[which(names(myshp@data) == "NomeReduzidoFerrovia")] <- "Sigla-Ferrovia"
colnames(myshp@data)[which(names(myshp@data) == "NomeLinha")] <- "Linha"

####################### CRIAÇÃO DO MAPA #######################

img <- "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Logo_ANTT.svg/1200px-Logo_ANTT.svg.png"

m3 <- mapview(myshp, zcol = "TU2019",
              legend = FALSE,
              layer.name = "2019",
              color = red) +
  mapview(myshp, zcol = "TU2018",
          legend = FALSE,
          layer.name = "2018",
          color = red) +
  mapview(myshp, zcol = "TU2017",
          legend = FALSE,
          layer.name = "2017",
          color = red) +
  mapview(myshp, zcol = "TU2016",
          legend = FALSE,
          layer.name = "2016",
          color = red)+
  mapview(myshp, zcol = "TU2015",
          legend = FALSE,
          layer.name = "2015",
          color = red)

m3 <- m3@map %>% addLayersControl(baseGroups = c("2019", "2018", "2017", "2016", "2015"),
                                  position = "topleft",
                                  options = layersControlOptions(collapsed = FALSE))
  
m3 <- m3 %>% leafem::addLogo(img, width = 120, height = 60, url = "http://www.antt.gov.br/", position="topleft")

mapshot(m3, url = "mapa_SFF.html", selfcontained = FALSE)

