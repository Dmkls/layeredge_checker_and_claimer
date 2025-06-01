# layeredge - checker and claimer

Софт для проверки аллокации и клейма на любую CEX биржу

![image](https://github.com/user-attachments/assets/8b5b4a89-6d84-49bc-beea-2273d7ccb6c7)

**Для запуска:**

1. установить гит - гайд здесь: [клик](https://teletype.in/@magnifier01chin/8iwREMa30Kq)

2. заходим в папку с софтом и запускаем `INSTALL.bat`

3. заполняем данные в файлах в папке data:

       data/proxies.txt - сюда прокси в формате username:password@ip:port

       data/wallets.txt - адреса, елси нужно проврерить размер дропа или приватные ключи, если нужно проверить дроп или заклеймить на биржу

       data/cex_data.txt - адреса для пополнения и id аккаунта биржи, в случае если будет использоваться клеймер, заполняются в формате depositeAddress:userId, биржа выбирается при запуске

 **Использование софта:**

 1. для запуска софта, нужно запустить файл START.bat

 2. в появившимся меню выбрать нужный режим
![image](https://github.com/user-attachments/assets/ef8ff4b5-83a3-47c4-8106-4b97d5e3dbf3)
для чекера достаточно адресов в `data/wallets.txt`, если нужен клеймер, то в файле должны быть приватники

3. в случае клеймера, нужно выбрать биржу
  ![image](https://github.com/user-attachments/assets/ead3836e-7662-48d8-85f2-44caa48b1fb9)

когда софт отработает, он покажет **количество элигабл кошельков** и **суммарное количество монет**, а также сохранит их в папке `results`
также будут выведены и сохранены адреса, на которые получилось заклеймить дроп

---

**мой тг**: [@MagniFier01Chin](https://t.me/MagniFier01Chin) помощь/вопросы

**мой канал**: [@povedalcrypto](https://t.me/povedalcrypto) апдейты/идеи

**EVM**: 0x2E5f5364032292Ce5869Bf5b74e6C388515c7D52

**SOL**: EjGyFeWWx6tFGtKov9r2hyPiiuVnxWR1nyAcLBvRtPCQ
