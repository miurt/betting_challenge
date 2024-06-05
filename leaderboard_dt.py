import flet as ft
import pandas as pd

class LeaderboardDataTable(ft.UserControl):

    def __init__(self, dataframe : pd.DataFrame, com: str, user: str):
            super().__init__()
            self.elevation = 5
            self.df = dataframe
            self.rows_indicies = []
            self.top_index = 0
            self.down_index = len(dataframe.index)
            self.user_index = 0
            self.title = com
            self.user = user
            self.set_up_indices()
    
    def headers(self, df : pd.DataFrame) -> list:
        return [ft.DataColumn(ft.Text(header)) for header in df.columns]

    def rows(self, df : pd.DataFrame) -> list:
        rows = []
        for index, row in df.iterrows():
            rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(row[header])) for header in df.columns]))
        return rows
    
    def set_up_indices(self):
        self.user_index = self.df[self.df['User'] == self.user].index[0]
        
        if len(self.df.index) <= 6:
            for index in self.df.index:
                self.rows_indicies.append(index)
        
        if len(self.df.index) > 6:
            #TOP 3
            self.rows_indicies.append(0, 1, 2)
            self.top_index = 2
            #adding logged user if it is NOT on top and NOT last
            if not (self.user_index == 0 | 1 | 2) and not (self.user_index == len(self.df.index)-1):
                self.down_index = self.user_index
                self.rows_indicies.append(self.user_index)
            #last user
            self.rows_indicies.append(len(self.df.index)-1)
            
    def update_indices(self, top: bool):
        if self.top_index >= self.down_index - 1:
            return
            
        if top:
            index = self.top_index
            new_indices = (index + 1, index + 11)
            ind = self.top_index + 1
            for i in new_indices:
                self.rows_indicies.insert(ind, i) 
                ind += 1
            self.top_index += 10
            
        else:
            index = self.down_index
            new_indices = (index - 11, index - 1)
            ind = self.top_index + 1
            for i in new_indices:
                self.rows_indicies.insert(ind, i) 
            self.down_index -= 10
        self.refresh_data()
    
    def build_new_dt(self):
        #CASE 1: no pagination
        # #list smaller than 6
        if len(self.df.index) == len(self.rows_indicies) or len(self.df.index) < 6:
            print(self.df)
            print(self.headers(self.df), self.rows(self.df))
            return ft.Column(
                [
                    ft.Text(self.title, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.DataTable(columns=self.headers(self.df), rows=self.rows(self.df))
                ],
                scroll=ft.ScrollMode.AUTO,
                alignment = ft.alignment.center
            )
        
        #CASE 2: no pagination
        #no users between logged user and top
        elif self.top_index <= self.down_index-1:
            return ft.Column(
                [
                    ft.Text(self.title, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.DataTable(columns=self.headers(self.df), rows=self.rows(self.df.iloc[self.rows_indicies]))
                ],
                scroll=ft.ScrollMode.AUTO,
                alignment = ft.alignment.center
            )
        
            
        #CASE 3: pagination
        #Building 2 DataTables with 2 arrows in between
        else:
            top_indicies = [self.rows_indicies[:self.top_index]]
            down_indicies = [self.rows_indicies[self.top_index+1:]]

            return ft.Column(
                [
                ft.Text(self.title, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),    
                ft.DataTable(columns=self.headers(self.df), rows=self.rows(self.df.iloc[top_indicies])),
                ft.IconButton(
                    icon=ft.icons.ARROW_DOWNWARD,
                    icon_size=20,
                    on_click=self.update_indices(self, True)
                ),
                ft.IconButton(
                    icon=ft.icons.ARROW_UPWARD,
                    icon_size=20,
                    on_click=self.update_indices(self, False)
                ),
                ft.DataTable(columns=self.headers(self.df), rows=self.rows(self.df.iloc[down_indicies])),
                ],
                scroll=ft.ScrollMode.AUTO,
                alignment = ft.alignment.center
            )
                    
        

    def build(self):
        return  ft.Card(
            ft.Container(
                self.build_new_dt(),
                padding=10,
            )
        )

    def refresh_data(self):
        self.update()

    def did_mount(self):
        self.refresh_data()