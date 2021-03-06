# Eth Contract Test Task

## Тестовое задание

Сервис проводит операции операции с NFT-токеном, используя REST API, взаимодействует со следующим [смарт-контрактом](https://rinkeby.etherscan.io/address/0x92e098def0ca9577bd50ca61b90b9a46ec1f2040). 
В сервисе реализована функция для получения информации из блокчейна и функция для изменения состояния смарт-контракта. 


### Представления API (Views)
1. `/tokens/create`  - принимает media_url, owner. Генерирует случайную строку длиной в 
20 символов и обращается к смарт-контракту токена. Вызывает функцию mint() у смарт
контракта, подписывает транзакцию ключом приватным ключом и отправляет подписанную
транзакцию в сеть. Идентификатор транзакции сохраняется в поле tx_hash объекта Token.
После успешного выполнения транзакции возвращает репрезентацию объекта Token.
2. `/tokens/list` - обращается к базе данных и возвращается список всех объектов модели Token
3. `/tokens/total_supply` - обращается к контракту в блокчейне и возвращает информацию о
текущем количестве находящихся в сети токенов. 

### Конфигурации сервиса
Конфигурации сервиса хранятся в приватном файле `.env`, который имеет следующую структуру. 

```code
SECRET_KEY = ''
INFURA_KEY = ''

CONTRACT_ADRESS = '0x92e098deF0CA9577BD50ca61B90b9A46EC1F2040'
CONTRACT_ABI = 'contract_abi.json'

ACCOUNT = ''
PRIVATE_KEY = ''
```

CONTRACT_ADRESS и CONTRACT_ABI взяты со страницы смарт-контракта по следующей [ссылке](https://rinkeby.etherscan.io/address/0x92e098def0ca9577bd50ca61b90b9a46ec1f2040)

CONTRACT_ABI - это файл в формате JSON, который считывается сервисом. Далее эта информация используется
для взаимодействия со смарт-контрактом.

### Сеть 
Сервис использует для работы тестовую сеть `Ethereum Rinkeby Testnet`
