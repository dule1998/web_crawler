import matplotlib.pyplot as plt
import numpy as np
from db_connection import DB


class Graphs:
    @staticmethod
    def locations_bar():
        conn = DB.get_connection()

        cursor = conn.cursor()

        cursor.execute("""select Lokacija, count(*) as Broj
            from automobili
            group by Lokacija""")

        result = sorted(cursor.fetchall(), key=lambda x: x[1], reverse=True)

        data = dict(result[0:10])

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.barh(np.arange(len(data.keys())), data.values())
        ax.set_yticks(np.arange(len(data.keys())), labels=data.keys())
        ax.invert_yaxis()
        ax.set_xlabel('Broj automobila')
        ax.set_title('Top 10 lokacija po prodaji automobila')
        ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        for i in ax.patches:
            plt.text(i.get_width() + 0.2, i.get_y() + 0.5, str(i.get_width()))

        plt.show()

    @staticmethod
    def year_bar():
        conn = DB.get_connection()

        cursor = conn.cursor()

        cursor.execute("""select case
                when Godiste < 1961 then 'Starije od 1960'
                when Godiste between 1961 and 1970 then '1961-1970'
                when Godiste between 1971 and 1980 then '1971-1980'
                when Godiste between 1981 and 1990 then '1981-1990'
                when Godiste between 1991 and 2000 then '1991-2000'
                when Godiste between 2001 and 2005 then '2001-2005'
                when Godiste between 2006 and 2010 then '2006-2010'
                when Godiste between 2011 and 2015 then '2011-2015'
                when Godiste between 2016 and 2020 then '2016-2020'
                else '2021-2022'   
                end as Period, count(*) as Broj  
            from automobili
            group by Period
            order by Period desc""")

        result = cursor.fetchall()

        result.insert(len(result), result.pop(0))

        data = dict(result)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.barh(np.arange(len(data.keys())), data.values())
        ax.set_yticks(np.arange(len(data.keys())), labels=data.keys())
        ax.invert_yaxis()
        ax.set_xlabel('Broj automobila')
        ax.set_title('Broj automobila po periodu')
        ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        for i in ax.patches:
            plt.text(i.get_width() + 0.2, i.get_y() + 0.5, str(i.get_width()))

        plt.show()

    @staticmethod
    def distance_bar():
        conn = DB.get_connection()

        cursor = conn.cursor()

        cursor.execute("""select case
                when Kilometraza < 50000 then 'Ispod 50 000'
                when Kilometraza between 50000 and 99999 then '50 000 do 99 999'
                when Kilometraza between 100000 and 149999 then '100 000 do 149 999'
                when Kilometraza between 150000 and 199999 then '150 000 do 199 999'
                when Kilometraza between 200000 and 249999 then '200 000 do 249 999'
                when Kilometraza between 250000 and 299999 then '250 000 do 299 999'
                else 'Preko 300 000'   
                end as Distanca, count(*) as Broj
            from automobili
            group by Distanca
            order by Distanca desc""")

        result = cursor.fetchall()

        result.insert(len(result), result.pop(2))
        result.insert(len(result), result.pop(1))

        data = dict(result)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.barh(np.arange(len(data.keys())), data.values())
        ax.set_yticks(np.arange(len(data.keys())), labels=data.keys())
        ax.invert_yaxis()
        ax.set_xlabel('Broj automobila')
        ax.set_title('Broj automobila po pređenoj kilometraži')
        ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        for i in ax.patches:
            plt.text(i.get_width() + 0.2, i.get_y() + 0.5, str(i.get_width()))
            
        plt.tight_layout()

        plt.show()

    @staticmethod
    def gearshift_pie():
        conn = DB.get_connection()

        cursor = conn.cursor()

        cursor.execute("""select case
                when Menjac is null then 'Bez podatka'
                else Menjac
                end as Menjac, count(*) as Broj, count(*) * 100 / sum(count(*)) over() as Procenat
            from automobili
            group by Menjac
            order by Broj desc""")

        result = cursor.fetchall()

        labels = []
        legend_labels = []
        values = []
        for res in result:
            labels.append(res[0])
            legend_labels.append(res[0] + ' - ' + str(res[1]) + ' (' + str(res[2]) + '%)')
            values.append(res[1])

        fig, ax = plt.subplots(2, figsize=(10, 7))

        ax[0].barh(np.arange(len(labels)), values)
        ax[0].set_yticks(np.arange(len(labels)), labels=labels)
        ax[0].invert_yaxis()
        ax[0].set_xlabel('Broj automobila')
        ax[0].set_title('Broj automobila po vrsti menjača')
        ax[0].grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
        ax[0].spines['top'].set_visible(False)
        ax[0].spines['right'].set_visible(False)
        plt.tight_layout()

        for i in ax[0].patches:
            ax[0].text(i.get_width() + 0.2, i.get_y() + 0.5, str(i.get_width()))

        ax[1].pie(values, startangle=90)
        ax[1].set_title('Procenat automobila po vrsti menjača')
        ax[1].axis('equal')
        ax[1].legend(title='Legenda', labels=legend_labels, loc='lower left', bbox_to_anchor=(-0.2, 0.1))

        plt.subplots_adjust(hspace=0.4)

        plt.show()

    @staticmethod
    def price_pie():
        conn = DB.get_connection()

        cursor = conn.cursor()

        cursor.execute("""select case
            when Cena < 2000 then 'Manje od 2 000 €'
            when Cena between 2000 and 4999 then 'Između 2 000 i 4 999 €'
            when Cena between 5000 and 9999 then 'Između 5 000 i 9 999 €'
            when Cena between 10000 and 14999 then 'Između 10 000 i 14 999 €'
            when Cena between 15000 and 19999 then 'Između 15 000 i 19 999 €'
            when Cena between 20000 and 24999 then 'Između 20 000 i 24 999 €'
            when Cena between 25000 and 29999 then 'Između 25 000 i 29 999 €'
            else '30 000 € i više'   
            end as Cene, count(*) as Broj, count(*) * 100 / sum(count(*)) over() as Procenat
        from automobili
        group by Cene
        order by Cene desc""")

        result = cursor.fetchall()

        result.insert(1, result.pop(4))
        result.insert(3, result.pop(len(result) - 2))
        result.insert(4, result.pop(len(result) - 2))
        result.insert(5, result.pop(len(result) - 2))

        labels = []
        legend_labels = []
        values = []
        for res in result:
            labels.append(res[0])
            legend_labels.append(res[0] + ' - ' + str(res[1]) + ' (' + str(res[2]) + '%)')
            values.append(res[1])

        fig, ax = plt.subplots(2, figsize=(10, 7))

        ax[0].barh(np.arange(len(labels)), values)
        ax[0].set_yticks(np.arange(len(labels)), labels=labels)
        ax[0].invert_yaxis()
        ax[0].set_xlabel('Broj automobila')
        ax[0].set_title('Broj automobila po ceni')
        ax[0].grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
        ax[0].spines['top'].set_visible(False)
        ax[0].spines['right'].set_visible(False)

        for i in ax[0].patches:
            ax[0].text(i.get_width() + 0.2, i.get_y() + 0.5, str(i.get_width()))

        ax[1].pie(values, startangle=90)
        ax[1].set_title('Procenat automobila po ceni')
        ax[1].axis('equal')
        ax[1].legend(title='Legenda', labels=legend_labels, loc='lower left', bbox_to_anchor=(-0.2, 0.1))

        plt.tight_layout()
        plt.subplots_adjust(hspace=0.4)

        plt.show()
