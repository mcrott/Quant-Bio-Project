library(tidyverse)


df <- read_csv("/Users/cmdb/Quant_Bio_Project/Quant-Bio-Project/intensity_data.txt")

ggplot(data=df)+
  geom_histogram(aes(x=df$Spacer))