import flet as ft
import pandas as pd

class LeaderboardDataTable(ft.UserControl):

    def __init__(self, dataframe : pd.DataFrame, com: str, user: str):
            super().__init__()
            self.df = dataframe
            self.rows_indicies = []
            self.top_index = 0
            self.down_index = len(dataframe.index)
            self.user_index = 0
            self.title = com
            self.user = user
            self.set_up_indices()
            self.dt_column = ft.Column([], scroll=ft.ScrollMode.AUTO,
                alignment = ft.alignment.center)
    
    def headers(self, df : pd.DataFrame) -> list:
        return [ft.DataColumn(ft.Text(header)) for header in df.columns]

    def rows(self, df : pd.DataFrame) -> list:
        rows = []
        for index, row in df.iterrows():
            rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(row[header])) for header in df.columns]))
        return rows
    
    def set_up_indices(self):
        self.user_index = self.df.index.get_loc(self.df[self.df['User'] == self.user].index[0])
        if len(self.df.index) <= 6:
            for index in self.df.index:
                self.rows_indicies.append(index)
        
        if len(self.df.index) > 6:
            #TOP 3
            self.rows_indicies.extend([0, 1, 2])
            self.top_index = 2
            #adding logged user if it is NOT on top and NOT last
            if not (self.user_index in (0, 1, 2)) and not (self.user_index == len(self.df.index)-1):
                self.down_index = self.user_index
                self.rows_indicies.append(self.user_index)
            elif self.user_index in (0, 1, 2):
                self.down_index = len(self.df.index)-1
                self.top_index = 2
            #last user
            self.rows_indicies.append(len(self.df.index)-1)
            
        self.dt_column = self.build_new_dt()
            
    def update_indices(self, top: bool):
        if self.top_index >= self.down_index - 1:
            self.refresh_data()
            return
            
        if top:
            index = self.top_index
            new_indices = range(index + 1, index + 12)
            ind = self.top_index + 1
            for i in new_indices:
                if i < self.down_index:
                    self.rows_indicies.insert(ind, i) 
                    ind += 1
                    self.top_index += 1
                else:
                    break
            
        else:
            index = self.down_index + 1
            print(index)
            new_indices = range(index - 12, index - 1)
            ind = self.top_index + 1
            num_to_substract = 0
            for i in new_indices:
                if i > self.top_index and i < self.down_index:
                    self.rows_indicies.insert(ind, i) 
                    ind += 1
                    num_to_substract += 1
            self.down_index -= num_to_substract
            print(self.top_index, self.down_index)
            
        self.refresh_data()
    
    def build_new_dt(self):
        #CASE 1: no pagination
        # list smaller than 6
        if len(self.df.index) == len(self.rows_indicies) or len(self.df.index) < 6:
            return [
                    ft.Text(self.title, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.DataTable(columns=self.headers(self.df), rows=self.rows(self.df))
                ]
        
        #CASE 2: no pagination
        #no users between logged user and top/down
        elif self.top_index >= self.down_index-1:
            df = self.df.iloc[self.rows_indicies]
            return [
                    ft.Text(self.title, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.DataTable(columns=self.headers(df), rows=self.rows(df))
                ]
        
            
        #CASE 3: pagination
        #Building 2 DataTables with 2 arrows in between
        else:
            top_indicies = self.rows_indicies[:self.top_index + 1]
            down_indicies = self.rows_indicies[self.top_index+1:]
            df1 = self.df.iloc[top_indicies]
            df2 = self.df.iloc[down_indicies]

            return [
                    ft.Text(self.title, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),    
                    ft.DataTable(columns=self.headers(df1), rows=self.rows(df1)),
                    ft.IconButton(
                        icon=ft.icons.ARROW_DOWNWARD,
                        icon_size=20,
                        on_click=lambda _: self.update_indices(top = True)
                    ),
                    ft.IconButton(
                        icon=ft.icons.ARROW_UPWARD,
                        icon_size=20,
                        on_click=lambda _: self.update_indices(top =False)
                    ),
                    ft.DataTable(columns=self.headers(df2), rows=self.rows(df2)),
                ]
                    
        

    def build(self):
        print("BUILDING")
        return  ft.Card(
            ft.Container(
                self.dt_column,
                padding=10,
            ),
        )

    def refresh_data(self):
        self.dt_column.controls.clear()
        self.dt_column.controls.extend(self.build_new_dt())
        
        print("update data")
        self.update()

    def did_mount(self):
        self.refresh_data()