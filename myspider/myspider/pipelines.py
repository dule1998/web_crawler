# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector


class MyspiderPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='******',
            database='abcd'
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if item is not None:
            self.cursor.execute("""insert into automobili(Stanje, Marka, Model, Godiste, Kilometraza, Karoserija, Gorivo, Kubikaza, Snaga, Menjac, Vrata, Boja, Lokacija, Cena) values 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                item['stanje'],
                item['marka'],
                item['model'],
                item['godiste'],
                item['kilometraza'],
                item['karoserija'],
                item['gorivo'],
                item['kubikaza'],
                item['snaga'],
                item['menjac'],
                item['vrata'],
                item['boja'],
                item['lokacija'],
                item['cena'],
            ))
            self.conn.commit()

        return item
