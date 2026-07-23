import scrapy
from ..items import MyspiderItem


class CarsSpider(scrapy.Spider):
    name = "cars"

    numOfCars = 0

    start_urls = [
        'https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=&price_to=&year_from=&year_to=&showOldNew=all&submit_1=&without_price=1'
    ]

    def parse(self, response):
        if self.numOfCars < 20000:
            yield from response.follow_all(xpath='//div[@class="image"]/a', callback=self.parse_car)

            next_link = response.css('a[title="Sledeća stranica"]')[0]
            yield response.follow(next_link, self.parse)

    def parse_car(self, response):
        if self.numOfCars < 20000:
            item = MyspiderItem()

            snaga = response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Snaga motora"]/following-sibling::div/text()').get()

            textcena = None
            cena = 0
            if response.xpath('//span[contains(@class,"priceClassified")]/text()').get() is not None:
                textcena = response.xpath('//span[contains(@class,"priceClassified")]/text()').get()[:-2].replace('.', '')
                if textcena.isnumeric():
                    cena = int(textcena)
            else:
                yield None

            item['stanje'] = response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Stanje:"]/following-sibling::div/text()').get()
            item['marka'] = response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Marka"]/following-sibling::div/text()').get()
            item['model'] = response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Model"]/following-sibling::div/text()').get()
            if response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Godište"]/following-sibling::div/text()').get() is not None:
                item['godiste'] = int(response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Godište"]/following-sibling::div/text()').get().strip('.'))
            else:
                item['godiste'] = None
            if response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Kilometraža"]/following-sibling::div/text()').get() is not None:
                item['kilometraza'] = int(response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Kilometraža"]/following-sibling::div/text()').get().strip(' km').replace('.', ''))
            else:
                item['kilometraza'] = None
            item['karoserija'] = response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Karoserija"]/following-sibling::div/text()').get()
            item['gorivo'] = response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Gorivo"]/following-sibling::div/text()').get()
            if response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Kubikaža"]/following-sibling::div/text()').get() is not None:
                item['kubikaza'] = int(response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Kubikaža"]/following-sibling::div/text()').get().strip(' cm'))
            else:
                item['kubikaza'] = None
            if snaga is not None:
                item['snaga'] = int(snaga[(snaga.index('/') + 1):(snaga.index(' '))])
            else:
                item['snaga'] = None
            if response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Menjač"]/following-sibling::div/text()').get() is not None:
                item['menjac'] = response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Menjač"]/following-sibling::div/text()').get().strip('\n\t ')
            else:
                item['menjac'] = None
            if response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Broj vrata"]/following-sibling::div/text()').get() is not None:
                item['vrata'] = response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Broj vrata"]/following-sibling::div/text()').get().strip('\n\t ')
            else:
                item['vrata'] = None
            if response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Boja"]/following-sibling::div/text()').get() is not None:
                item['boja'] = response.xpath('//div[@class="divider"]/div[@class="uk-grid"]/div[text()="Boja"]/following-sibling::div/text()').get().strip('\n\t ')
            else:
                item['boja'] = None
            if response.xpath('//div[contains(@class, "js-tutorial-contact")]//div[@class="uk-width-1-2"]/text()').get() is not None:
                item['lokacija'] = response.xpath('//div[contains(@class, "js-tutorial-contact")]//div[@class="uk-width-1-2"]/text()').get().strip('\n\t ')
            else:
                item['lokacija'] = None
            item['cena'] = cena

            if item['stanje'] is None \
                    and item['marka'] is None \
                    and item['model'] is None \
                    and item['godiste'] is None \
                    and item['kilometraza'] is None \
                    and item['karoserija'] is None \
                    and item['gorivo'] is None \
                    and item['kubikaza'] is None \
                    and item['snaga'] is None \
                    and item['menjac'] is None \
                    and item['vrata'] is None \
                    and item['boja'] is None \
                    and item['lokacija'] is None:
                yield None

            self.numOfCars += 1

            yield item
