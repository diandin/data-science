from spyre import server
import pickle
import pandas as pd


class StockExample(server.App):
    title = 'Vegetation Data'

    inputs = [{"type": 'dropdown',
               "label": 'Index',
               "options": [{"label": "VHI", "value": "VHI"},
                           {"label": "TCI", "value": "TCI"},
                           {"label": "VCI", "value": "VCI"}],
               "key": 'index',
               },
              {"type": 'dropdown',
               "label": 'Region',
               "options": [{"label": "Україна", "value": "Україна"},
                           {"label": "Вінницька область", "value": "Вінницька область"},
                           {"label": "Волинська область", "value": "Волинська область"},
                           {"label": "Дніпропетровська область", "value": "Дніпропетровська область"},
                           {"label": "Донецька область", "value": "Донецька область"},
                           {"label": "Житомирська область", "value": "Житомирська область"},
                           {"label": "Закарпатська область", "value": "Закарпатська область"},
                           {"label": "Запорізька область", "value": "Запорізька область"},
                           {"label": "Івано-Франківська область", "value": "Івано-Франківська область"},
                           {"label": "Київська область", "value": "Київська область"},
                           {"label": "Кіровоградська область", "value": "Кіровоградська область"},
                           {"label": "Луганська область", "value": "Луганська область"},
                           {"label": "Львівська область", "value": "Львівська область"},
                           {"label": "Миколаївська область", "value": "Миколаївська область"},
                           {"label": "Одеська область", "value": "Одеська область"},
                           {"label": "Полтавська область", "value": "Полтавська область"},
                           {"label": "Рівенська область", "value": "Рівенська область"},
                           {"label": "Сумська область", "value": "Сумська область"},
                           {"label": "Тернопільська область", "value": "Тернопільська область"},
                           {"label": "Харківська область", "value": "Харківська область"},
                           {"label": "Херсонська область", "value": "Херсонська область"},
                           {"label": "Хмельницька область", "value": "Хмельницька область"},
                           {"label": "Черкаська область", "value": "Черкаська область"},
                           {"label": "Чернівецька область", "value": "Чернівецька область"},
                           {"label": "Чернігівська область", "value": "Чернігівська область"},
                           {"label": "Республіка Крим", "value": "Республіка Крим"}],
               "key": 'region',
               },
              {
                  "type": 'text',
                  "label": 'Weeks more than',
                  "value": '1',
                  "key": 'week1',
                  "action_id": "reload"
              },
              {
                  "type": 'text',
                  "label": 'Weeks less than',
                  "value": '53',
                  "key": 'week2',
                  "action_id": "reload"
              },
              {
                  "type": 'text',
                  "label": 'Years more than',
                  "value": '1992',
                  "key": 'year1',
                  "action_id": "reload"
              },
              {
                  "type": 'text',
                  "label": 'Years less than',
                  "value": '2020',
                  "key": 'year2',
                  "action_id": "reload"
              },
              ]

    controls = [{"type": "hidden",
                 "id": "update_data"},
                {"type": "button",
                 "label": "reload",
                 "id": "update_data"}]

    tabs = ["Table1", "Table2", "Table3", "Plot1", "Plot2", "Plot3", "Plot4"]

    outputs = [{"type": "table",
                "id": "table1",
                "control_id": "update_data",
                "tab": "Table1",
                "on_page_load": False,
                "sortable": True},

               {"type": "table",
                "id": "table2",
                "control_id": "update_data",
                "tab": "Table2",
                "on_page_load": False,
                "sortable": True},

               {"type": "table",
                "id": "table3",
                "control_id": "update_data",
                "tab": "Table3",
                "on_page_load": False,
                "sortable": True},
               {
                   "type": "plot",
                   "id": "plot1",
                   "control_id": "update_data",
                   "tab": "Plot1",
                   "on_page_load": False},
               {
                   "type": "plot",
                   "id": "plot2",
                   "control_id": "update_data",
                   "tab": "Plot2",
                   "on_page_load": False,
               },
               {
                   "type": "plot",
                   "id": "plot3",
                   "control_id": "update_data",
                   "tab": "Plot3",
                   "on_page_load": False,
               },
               { "type": "plot",
                   "id": "plot4",
                   "control_id": "update_data",
                   "tab": "Plot4",
                   "on_page_load": False}
               ]



    def table1(self, params):
        index = str(params['index'])
        region = str(params['region'])
        week_more = float(params['week1'])
        week_less = float(params['week2'])
        print(params['year1'])
        print(params['year2'])
        year_more = (params['year1'])
        year_less = (params['year2'])
        with open('pickledata.p', 'rb') as file:
            df1 = pickle.load(file)
        df = df1[['Year', 'Week', 'Region', 'SMN', 'SMT', f'{index}']]

        if region != 'Україна':
            df = df.loc[(df['Region'] == f'{region}')]

        self.df = df.loc[(df['Week'] > week_more) & (df['Week'] < week_less) &
                         (df['Year'] < year_less) & (df['Year'] > year_more)]
        print("df finished")

        return self.df


    # додаткове завдання 1
    # вивести датафрейм: тиждень (1-52), значення років в яких в цей тиждень vhi min (max)

    def table2(self, params):
        with open('pickledata.p', 'rb') as file:
            df1 = pickle.load(file)

        df2 = df1[['Year', 'Week', 'VHI']]
        idx = df2.groupby(['Week'])['VHI'].transform(max) == df2['VHI']
        idx2 = df2.groupby(['Week'])['VHI'].transform(min) == df2['VHI']

        df3 = df2[idx]
        df4 = df2[idx2]

        df_new = df3.merge(df4, left_on='Week', right_on='Week', how='outer')  # outer - объединение ключей
        df_new = df_new.sort_index().sort_values('Week')

        return df_new

    #Додаткове завдання 2
    #за кожну провінцію вивести перелік в якому тижні якого року значення vhi було найближче до середнього

    def table3(self, params):
        with open('pickledata.p', 'rb') as file:
            df1 = pickle.load(file)

        df = df1[['Year', 'Week', 'VHI', 'Region']]

        df_new = pd.DataFrame()

        for region in df['Region'].unique():
            df_1 = df.loc[(df['Region'] == region)]
            df_1['mean'] = df_1['VHI'].mean()
            df_1['dif'] = (df['VHI'] - df_1['mean']).abs()

            idx = df_1['dif'].min() == df_1['dif']
            df_1 = df_1[idx]

            df_1 = df_1[['Year', 'Week', 'VHI', 'Region', 'dif']]
            df_new = pd.concat([df_new, df_1], ignore_index=True)

        return df_new


    def plot1(self, params):
        index = str(params['index'])
        df = self.table1(params)
        df1 = df[['Year', 'Region', f'{index}']]
        fig = df1.set_index('Year').plot()
        return fig


    def plot2(self, params):
        df = self.table2(params)
        df1 = df[['Year_y', 'VHI_y',]]
        fig = df1.set_index('Year_y').plot()
        return fig

    def plot3(self, params):
        df = self.table2(params)
        df1 = df[['Year_x', 'VHI_x', ]]
        fig = df1.set_index('Year_x').plot()
        return fig



    def plot4(self, params):
        df = self.table3(params)
        df1 = df[['Week', 'VHI', 'Region']]
        fig = df1.plot()
        return fig

app = StockExample()
app.launch(port=9008)
