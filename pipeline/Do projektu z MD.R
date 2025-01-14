# Stąd, czyli IMGW
# https://danepubliczne.imgw.pl/pl/datastore?product=Meteo


tabela <- read.table('C:/Users/Lenovo/Desktop/B00300S_2024_01.csv', sep = ";", header = TRUE)
colnames(tabela) <- c('Kod_Stacji', 'Kod_Temperatury', 
                      'Data_i_Godzina', 'Temperatura', 'NA')

tabela_wrocław <- tabela[tabela$Kod_Stacji == 351160425, ]

temperatury_bardzo_zimny_dzień_09_01_2024 <- as.numeric(gsub(",", ".", tabela_wrocław[startsWith(tabela_wrocław$Data_i_Godzina, "2024-01-09"), ]$Temperatura))
temperatury_zimny_dzień_12_01_2024 <- as.numeric(gsub(",", ".", tabela_wrocław[startsWith(tabela_wrocław$Data_i_Godzina, "2024-01-12"), ]$Temperatura))
temperatury_chłodny_dzień_30_01_2024 <- as.numeric(gsub(",", ".", tabela_wrocław[startsWith(tabela_wrocław$Data_i_Godzina, "2024-01-30"), ]$Temperatura))

Srednia_temp_09_01_2024 <- mean(temperatury_bardzo_zimny_dzień_09_01_2024)
Srednia_temp_12_01_2024 <- mean(temperatury_zimny_dzień_12_01_2024)
Srednia_temp_30_01_2024 <- mean(temperatury_chłodny_dzień_30_01_2024)

# Tworzenie wektora godzin
godziny <- seq(from = 0, to = 23, by = 1)  # godziny od 00 do 23
minuty <- seq(from = 0, to = 50, by = 10)  # minuty co 10 minut

# Łączenie godzin i minut, aby stworzyć zakresy czasowe
czasy <- character()  # Tworzymy pusty wektor na zakresy czasowe
for (godzina in godziny) {
  for (minuta in minuty) {
    if(minuta == 50){
      # Tworzymy ciąg "hh:mm - hh:mm"
      poczatek <- sprintf("%02d:%02d", godzina, minuta)
      koniec <- sprintf("%02d:%02d", godzina+1, 0)
      czasy <- c(czasy, paste(poczatek, "-", koniec))
    } else{
      # Tworzymy ciąg "hh:mm - hh:mm"
      poczatek <- sprintf("%02d:%02d", godzina, minuta)
      koniec <- sprintf("%02d:%02d", godzina, minuta + 10)
      czasy <- c(czasy, paste(poczatek, "-", koniec))
    }
  }
}

Outside_temperatures_in_Wroclaw <- data.frame(czasy, temperatury_bardzo_zimny_dzień_09_01_2024,
                                              temperatury_zimny_dzień_12_01_2024, temperatury_chłodny_dzień_30_01_2024)
colnames(Outside_temperatures_in_Wroclaw) <- c('Czas', 'Bardzo zimny dzień 09.01.2024', 'Zimny dzień 12.01.2024', 'Chłodny dzień 30.01.2024')

# Zapisanie tabeli do pliku CSV
write.csv(Outside_temperatures_in_Wroclaw, "C:/Users/Lenovo/Desktop/Outside temperatures in Wroclaw (3 types of days).csv", row.names = FALSE)