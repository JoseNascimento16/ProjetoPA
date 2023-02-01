<h1 align="center">SIPA</h1>

## About ![pin-img](https://user-images.githubusercontent.com/110631271/215866770-755c96a6-17fa-4a7c-9c05-23693843f01c.png)

The SIPA - Sistema de Planos de Ação, was developed to improve communication between schools and the state department regarding the creation and approval of specific documents related to schools expenses.

## Used technologies ![pin-img](https://user-images.githubusercontent.com/110631271/215866770-755c96a6-17fa-4a7c-9c05-23693843f01c.png)
<li>Python 3.9</li>
<li>Django 4.1</li>
<li>Javacript</li>
<li>HTML and CSS</li>
<li>Bootstrap</li>
<li>PostgreSQL</li>

## Python/Django features ![pin-img](https://user-images.githubusercontent.com/110631271/215866770-755c96a6-17fa-4a7c-9c05-23693843f01c.png)
<li>Signals</li>
<li>middlewares</li>
<li>Unit test (Pytest)</li>
<li>Template simple tags</li>
<li>Modelforms</li>
<li>JSONparse script tag</li>

## Overall features ![pin-img](https://user-images.githubusercontent.com/110631271/215866770-755c96a6-17fa-4a7c-9c05-23693843f01c.png)
<li>Modals</li>
<li>Tooltips</li>
<li>Searchbar</li>
<li>Emails sending</li>
<li>Digital signature</li>
<li>canvas</li>
<li>Encoded email activation system</li>
<li>Encoded password change</li>
<li>Event logs</li>
<li>Document print</li>

## Functionalities ![pin-img](https://user-images.githubusercontent.com/110631271/215866770-755c96a6-17fa-4a7c-9c05-23693843f01c.png)
**<li>Users and schools registration</li>**
6 user types are allowed to be registered. From schools directors and its employees to the state department director, managers and technicians.
Schools can be registered as well, but only by some allowed state department employees.

<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215905665-f31c962a-22bc-4269-8d7d-67d19de58a49.gif">
</p>

**<li>3 different documents</li>**
The web app is able to generate 3 documents dynamically. Each school employee can only access the documents created by the director of his school. 
1. Identificação das Ações
<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215912722-a872f8aa-962a-415d-b40d-036e5f96fb6c.gif">
</p>

2. Detalhamento das Despesas
<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215913589-c2f42ae8-7286-4e9c-a81d-d6858700ddd0.gif">
</p>

3. Formulário de inclusão/alteração de Ações (FIA)
<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215914847-626a9efe-3490-48d7-a07a-1f405fefdff8.gif">
</p>


**<li>Document correction</li>**
After being sent to the state department, the document is analyzed by their employees and sent back approved or with some corrections to be made. This back and forth can be done as many times as necessary until everything is ok.
<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215918750-d498a0c6-9575-4cbc-bbbe-30c231875e1c.gif">
</p>

**<li>Pagination</li>**
The web app have a pagination system to display only a relevant amount of documents per page.
<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215919228-0c9e4366-c6f6-4161-9a91-7a45f3111273.png">
</p>

**<li>Searchbar</li>**
The searchbar allows the user to search for documents by: Its name, the school name, the school director name, the document status.
<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215919623-81429b25-2c05-4cb2-b0db-a8247742781e.gif">
</p>

**<li>Custom signature</li>**
The user may choose to use an automatic generated sign, or to drawn his own signature on a canvas.
<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215920263-5d0ec7a0-6a69-4252-95c0-6b3e91f390e1.gif">
</p>

**<li>Event logs</li>**
The most important information and the documents status changes are stored on a log system and are accessible to the users.
<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215920663-73060695-d200-467a-8f09-654ce036caf0.gif">
</p>

**<li>Password change</li>**
The web app uses the Django class based passwordresetview to offer a secure way to change your password.

**<li>Print functionality</li>**
The print functionality was developed to satisfy some bussiness rules where some part of the document couldn't be apart from others. This feature deals with it by integrating with the brownser print feature.
<p align="center">
  <img src="https://user-images.githubusercontent.com/110631271/215921785-cd772387-8180-43ec-8b31-9d1615b1a270.gif">
</p>
